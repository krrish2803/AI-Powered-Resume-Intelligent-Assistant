import os
from fastapi.responses import FileResponse
from groq import Groq
from dotenv import load_dotenv
load_dotenv()
import uuid

api_key = os.getenv("GROQ_API_KEY")
client = Groq(api_key=api_key)

def mock_interview(data):
    role = data.get("role","AI Engineer")
    skills = data.get("skills",[])
    user_answers = data.get("answers",[])

    prompt = f"""
    You are an AI Interviewer . Conduct a mock interview for the role of {role}
    Ask 10 specofic questions to the user based on their skills: {','.join(skills)}
    """
    
    completion =client.chat.completions.create(
        model="llama3-70b-8192",
        messages = [
            {"role":"user", "content":prompt},
        ]
    )

    questions_raw = completion.choices[0].message.content
    questions = [q.strip() for q in questions_raw.strip().split("\n") if q.strip()]

    feedback = []
    for i, (q, ans) in enumerate(zip(questions, user_answers)):
        prompts = f"Interview Question: {q}\nUser Answer: {ans}\nProvide feedback on the user's answer."
        fb = client.chat.completions.create(
            model="llama3-70b-8192",
            messages=[{"role": "user", "content": prompts}]
        )
        feedback.append({"question": q, "answer": ans, "feedback": fb.choices[0].message.content})

    return {
        "questions": questions,
        "feedback": feedback
    }

