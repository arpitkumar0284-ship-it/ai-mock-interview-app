import os

import requests
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

URL = (
    "https://generativelanguage.googleapis.com/v1beta/models/"
    f"gemini-flash-lite-latest:generateContent?key={api_key}"
)


def ask_gemini(prompt):
    payload = {"contents": [{"parts": [{"text": prompt}]}]}
    response = requests.post(URL, json=payload)
    data = response.json()
    if "candidates" in data:
        return data["candidates"][0]["content"]["parts"][0]["text"]
    return f"Error: {data}"


def generate_question(role, interview_type):
    prompt = (
        f"You are an interviewer conducting a {interview_type} interview "
        f"for the role of {role}. Ask exactly one interview question. "
        f"Do not include any greeting, numbering, or explanation. "
        f"Just output the question itself."
    )
    return ask_gemini(prompt)


def evaluate_answer(role, question, answer):
    prompt = (
        f"You are an interview coach evaluating a candidate for the role of {role}.\n"
        f"Question: {question}\n"
        f"Candidate's answer: {answer}\n\n"
        f"Give a score out of 10, then 2-3 lines of feedback: what was good, "
        f"and what could be improved. Format exactly like this:\n"
        f"Score: X/10\n"
        f"Feedback: ..."
    )
    return ask_gemini(prompt)


if __name__ == "__main__":
    role = input("Job role (e.g. Data Analyst): ")
    interview_type = input("Interview type (Technical / HR): ")

    question = generate_question(role, interview_type)
    print("\nInterview Question:")
    print(question)

    answer = input("\nYour answer: ")

    result = evaluate_answer(role, question, answer)
    print("\nEvaluation:")
    print(result)