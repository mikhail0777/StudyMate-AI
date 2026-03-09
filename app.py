from flask import Flask, render_template, request
from google import genai
from dotenv import load_dotenv
import os
import re

load_dotenv()

app = Flask(__name__)

api_key = os.getenv("GEMINI_API_KEY")

client = None
if api_key:
    client = genai.Client(api_key=api_key)

MODEL_NAME = "gemini-2.5-flash"


def require_client():
    if client is None:
        raise ValueError(
            "Gemini API key not found. Add GEMINI_API_KEY to your .env file."
        )


def basic_summary(text: str) -> str:
    cleaned_text = re.sub(r"\s+", " ", text).strip()
    sentences = [s.strip() for s in re.split(r"(?<=[.!?])\s+", cleaned_text) if s.strip()]
    if not sentences:
        return "No summary could be generated."
    return " ".join(sentences[:3])


def clean_ai_text(text: str) -> str:
    cleaned = text.strip()

    cleaned = re.sub(r"^```[a-zA-Z]*\n?", "", cleaned)
    cleaned = re.sub(r"\n?```$", "", cleaned)

    cleaned = re.sub(r"^#{1,6}\s*", "", cleaned, flags=re.MULTILINE)
    cleaned = re.sub(r"\*\*(.*?)\*\*", r"\1", cleaned)
    cleaned = re.sub(r"\*(.*?)\*", r"\1", cleaned)
    cleaned = re.sub(r"`([^`]*)`", r"\1", cleaned)

    cleaned = re.sub(r"^\s*[-•]\s*", "", cleaned, flags=re.MULTILINE)
    cleaned = re.sub(r"^\s*\d+\.\s*", "", cleaned, flags=re.MULTILINE)

    cleaned = re.sub(r"^\s*Here'?s\s+.*?:\s*", "", cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(r"^\s*Summary:\s*", "", cleaned, flags=re.IGNORECASE)

    cleaned = re.sub(r"\n\s*\n+", "\n\n", cleaned).strip()
    return cleaned


def generate_summary(text: str) -> str:
    try:
        require_client()
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=(
                "Summarize the following study material in 4 to 6 plain, concise sentences. "
                "Do not use headings, bullet points, markdown, bold formatting, or intro phrases. "
                "Return only one clean paragraph written for a student.\n\n"
                f"{text}"
            ),
        )
        if not response.text:
            return basic_summary(text)

        cleaned = clean_ai_text(response.text)
        return cleaned if cleaned else basic_summary(text)

    except Exception as e:
        error_text = str(e)
        if "429" in error_text or "RESOURCE_EXHAUSTED" in error_text:
            return basic_summary(text)
        return f"Error generating summary: {error_text}"


def create_practice_questions(paragraph: str) -> list[str]:
    try:
        require_client()
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=(
                "Generate exactly 5 useful practice questions from the study material below. "
                "Return only the questions, one per line, with no heading or intro text.\n\n"
                f"{paragraph}"
            ),
        )

        raw_text = response.text.strip() if response.text else ""
        lines = [line.strip() for line in raw_text.splitlines() if line.strip()]

        cleaned_questions = []
        for line in lines:
            cleaned = line.lstrip("-•1234567890. ").strip()
            if cleaned:
                cleaned_questions.append(cleaned)

        return cleaned_questions[:5] if cleaned_questions else ["No questions could be generated."]
    except Exception as e:
        error_text = str(e)
        if "429" in error_text or "RESOURCE_EXHAUSTED" in error_text:
            return [
                "What is the main idea of the passage?",
                "What are the most important facts or concepts mentioned?",
                "Which part of the material would require more review?",
                "How would you explain this topic in your own words?",
                "What is one possible test question based on this material?",
            ]
        return [f"Error generating questions: {error_text}"]


def answer_from_context(context: str, question: str) -> str:
    try:
        require_client()
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=(
                "Answer the question using only the provided context. "
                "If the answer is not in the context, clearly say that. "
                "Do not use markdown or bullet points unless necessary.\n\n"
                f"Context:\n{context}\n\n"
                f"Question:\n{question}"
            ),
        )
        return response.text.strip() if response.text else "No answer could be generated."
    except Exception as e:
        error_text = str(e)
        if "429" in error_text or "RESOURCE_EXHAUSTED" in error_text:
            return "The AI service is temporarily unavailable. Please try again later."
        return f"Error generating answer: {error_text}"


def build_study_plan(syllabus: str, topics: str, start_date: str, deadline: str) -> str:
    try:
        require_client()
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=(
                "Create a realistic study plan for a student.\n\n"
                f"Syllabus:\n{syllabus}\n\n"
                f"Topics to focus on:\n{topics}\n\n"
                f"Start date: {start_date}\n"
                f"Deadline: {deadline}\n\n"
                "Format the plan clearly with practical steps and a sensible timeline."
            ),
        )
        return response.text.strip() if response.text else "No study plan could be generated."
    except Exception as e:
        error_text = str(e)
        if "429" in error_text or "RESOURCE_EXHAUSTED" in error_text:
            return (
                f"Study Plan\n\n"
                f"Start Date: {start_date}\n"
                f"Deadline: {deadline}\n\n"
                f"Topics to cover:\n{topics}\n\n"
                f"Use the syllabus below to break the work into smaller sections each day:\n"
                f"{syllabus}"
            )
        return f"Error generating study plan: {error_text}"


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/practice-questions", methods=["GET", "POST"])
def practice_questions():
    if request.method == "GET":
        return render_template("question_generator.html")

    paragraph = request.form.get("paragraph", "").strip()
    if not paragraph:
        return render_template(
            "question_generator.html",
            error="Please enter a paragraph before generating questions."
        )

    questions = create_practice_questions(paragraph)
    return render_template("question_generator_result.html", questions=questions)


@app.route("/summary", methods=["GET", "POST"])
def summary():
    if request.method == "GET":
        return render_template("summarizer.html")

    user_text = request.form.get("user_text", "").strip()
    if not user_text:
        return render_template("summarizer.html", error="Please enter text to summarize.")

    summary_result = generate_summary(user_text)
    return render_template("summarizer_result.html", summary=summary_result)


@app.route("/ask", methods=["GET", "POST"])
def ask():
    if request.method == "GET":
        return render_template("qa.html")

    context = request.form.get("context", "").strip()
    question = request.form.get("question", "").strip()
    if not context or not question:
        return render_template(
            "qa.html",
            error="Please provide both the study material and your question."
        )

    answer = answer_from_context(context, question)
    return render_template("qa_result.html", answer=answer)


@app.route("/study-plan", methods=["GET", "POST"])
def study_plan():
    if request.method == "GET":
        return render_template("study_plan.html")

    syllabus = request.form.get("syllabus", "").strip()
    topics = request.form.get("topics", "").strip()
    start_date = request.form.get("start_date", "").strip()
    deadline = request.form.get("deadline", "").strip()

    if not syllabus or not topics or not start_date or not deadline:
        return render_template(
            "study_plan.html",
            error="Please fill in all fields before generating your study plan."
        )

    generated_plan = build_study_plan(syllabus, topics, start_date, deadline)
    return render_template("study_plan_result.html", study_plan=generated_plan)


if __name__ == "__main__":
    app.run(debug=True)