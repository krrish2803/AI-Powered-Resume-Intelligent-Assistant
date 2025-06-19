import os
from fastapi.responses import FileResponse
from groq import Groq
from dotenv import load_dotenv
load_dotenv()

api_key = os.getenv("GROQ_API_KEY")
client = Groq(api_key=api_key)

def analyse_job(data):
    resume = data.get("resume","")
    job_description = data.get("job_description","")

    prompt = (
        "Given the following resume and job description, analyze how well the candidate fits the job. "
        "Rate the fit on a scale of 1-10, list matching qualifications, and suggest improvements.\n"
        f"Resume:\n{resume}\n\nJob Description:\n{job_description}"
    )

    response = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=[{"role": "user", "content": prompt}]
    )

    analysis = response.choices[0].message.content
    return {"job_fit_analysis": analysis}
