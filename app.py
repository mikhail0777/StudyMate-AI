from flask import Flask, render_template, request
from transformers import pipeline
import google.generativeai as genai
from config import GEMINI_API_KEY
import textwrap

app = Flask(__name__)

genai.configure(api_key=GEMINI_API_KEY)

# NLP pipelines
practice_question_generator = pipeline(
    "text2text-generation",
    model="valhalla/t5-base-qg-hl"
)

text_summarizer = pipeline(
    "summarization",
    model="facebook/bart-large-cnn"
)

context_qa_model = pipeline(
    "question-answering",
    model="distilbert-base-uncased-distilled-squad"
)


def split_text_into_chunks(text: str, width: int = 300) -> list[str]:
    """Split long input text into smaller chunks for processing."""
    return textwrap.wrap(text, width=width)


def create_practice_questions(paragraph: str) -> list[str]:
    """Generate practice questions from a paragraph of text."""
    text_chunks = split_text_into_chunks(paragraph)
    generated_questions = []

    for chunk in text_chunks:
        prompt = f"generate questions: {chunk}"
        results = practice_question_generator(
            prompt,
            max_length=50,
            num_return_sequences=5,
            num_beams=5
        )
        generated_questions.extend(item["generated_text"] for item in results)

    return generated_questions


def generate_summary(user_text: str) -> str:
    """Generate a concise summary from user-provided text."""
    words = user_text.split()

    if len(words) > 500:
        user_text = " ".join(words[:500])

    result = text_summarizer(
        user_text,
        max_length=300,
        min_length=100,
        do_sample=False
    )

    return result[0]["summary_text"]


def answer_from_context(context: str, question: str) -> str:
    """Answer a question using the provided context."""
    result = context_qa_model(question=question, context=context)
    return result["answer"]


def build_study_plan(syllabus: str, topics: str, start_date: str, deadline: str) -> str:
    """Generate a structured study plan using Gemini."""
    prompt = f"""
Create a realistic and structured study plan for a student.

Syllabus:
{syllabus}

Topics to focus on:
{topics}

Start date:
{start_date}

Deadline:
{deadline}

Requirements:
- Break the plan into weekly goals
- Include daily study tasks
- Keep the workload realistic and balanced
- Prioritize the most important topics first
- Present the final response clearly
"""

    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(prompt)
    return response.text


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
        return render_template(
            "summarizer.html",
            error="Please enter text to summarize."
        )

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
