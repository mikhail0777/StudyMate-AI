StudyMate AI
<div align="center">

AI-powered study assistant that summarizes notes, generates practice questions, and creates study plans.

Report Bug
 ·
Request Feature
 ·
View Repository

</div>
Table of Contents

About The Project

Built With

Features

Screenshots

Getting Started

Installation

Usage

Project Structure

Author

License

About The Project

StudyMate AI is a lightweight AI-powered study assistant that helps students process and understand course material more efficiently.

The application allows users to paste lecture notes, textbook content, or study material and automatically generate:

concise summaries

practice questions

contextual answers

structured study plans

The goal of this project is to demonstrate how modern NLP and AI tools can be integrated into a simple web application to improve student learning workflows.

Built With

Python

Flask

Transformers / NLP Models

HTML

CSS

JavaScript

REST APIs

Features
Text Summarization

Convert long lecture notes or study materials into clear and concise summaries for faster review.

Practice Question Generator

Automatically generate review questions from study content to help test understanding.

Context-Based Question Answering

Ask questions about the provided material and receive AI-generated answers based on the input text.

AI Study Plan Generator

Generate structured study plans to organize revision sessions and improve productivity.

Simple Web Interface

A minimal web interface built with Flask templates for easy interaction.

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

Getting Started

To get a local copy up and running follow these steps.

Installation

Clone the repository

git clone https://github.com/mikhail0777/StudyMate-AI.git

Navigate to the project folder

cd StudyMate-AI

Create a virtual environment

python -m venv venv

Activate the environment

Windows

venv\Scripts\activate

Mac/Linux

source venv/bin/activate

Install dependencies

pip install -r requirements.txt

Run the application

python app.py

Open your browser and go to

http://127.0.0.1:5000
Usage

Example ways StudyMate AI can be used:

Summarizing lecture notes before exams

Generating practice questions for self-testing

Reviewing large blocks of text quickly

Creating structured study schedules

Project Structure
StudyMate-AI
│
├── app.py
├── templates/
├── static/
├── requirements.txt
└── README.md
Author

Mikhail Simanian
Computer Science Student
Carleton University

GitHub:
https://github.com/mikhail0777
