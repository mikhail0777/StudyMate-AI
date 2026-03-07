StudyMate AI is a lightweight AI-powered study assistant designed to help students process, organize, and understand course material more efficiently.

The application allows users to paste lecture notes, textbook content, or study material and instantly generate:

concise summaries

practice questions

contextual answers

structured study plans

This project demonstrates how modern NLP and AI tools can be integrated into a simple web application to improve student learning workflows.

Features
📄 Text Summarization

Convert long lecture notes or study materials into clear and concise summaries for faster review.

❓ Practice Question Generator

Automatically generate review questions from study content to help test understanding and retention.

💬 Context-Based Question Answering

Ask questions about the provided material and receive AI-generated answers based on the input text.

🧠 AI Study Plan Generator

Create structured study schedules to organize revision sessions and improve productivity.

🌐 Simple Web Interface

A minimal and clean UI built with Flask templates for quick interaction and fast experimentation.

Tech Stack
Technology	Purpose
Python	Core backend language
Flask	Web application framework
Transformers / NLP models	Text processing and AI features
HTML / CSS / JavaScript	Frontend interface
REST APIs	AI service integration
Project Structure
StudyMate-AI
│
├── app.py                # Main Flask application
├── templates/            # HTML page templates
├── static/               # CSS and JavaScript files
├── requirements.txt      # Python dependencies
└── README.md
Installation
1️⃣ Clone the repository
git clone https://github.com/mikhail0777/StudyMate-AI.git
cd StudyMate-AI
2️⃣ Create a virtual environment
python -m venv venv
3️⃣ Activate the virtual environment

Windows

venv\Scripts\activate

Mac / Linux

source venv/bin/activate
4️⃣ Install dependencies
pip install -r requirements.txt
5️⃣ Run the application
python app.py

Open your browser and navigate to:

http://127.0.0.1:5000
Example Use Cases

StudyMate AI can assist students in multiple ways:

Summarizing lecture notes before exams

Generating practice questions for self-testing

Quickly reviewing large blocks of text

Creating structured study schedules

Improving understanding of complex course material

---
## 🖼️ Screenshots

🔹 **Home Page**  
![Home Page](./images/home.png)

🔹 **Question Generator**  
![Question Generator](./images/1.png)

🔹 **Summariezer Context** 
![Summariezer Context](./images/2.png)

🔹 **Question Answering** 
![Question Answering](./images/3.png)

🔹 **Study Plan Generator** 
![Study Plan Generator](./images/4.png)

---

## Author

Mikhail Simanian

Computer Science Student
Carleton University

---

## Disclaimer

This project is a personal educational project created to explore AI-powered learning tools and web application development.



