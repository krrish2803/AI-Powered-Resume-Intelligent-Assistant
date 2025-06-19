# main.py

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from resume import generate_resume
from cover_letter import generate_cover_letter
from mock import mock_interview
from job_fit import analyse_job

app = FastAPI(title="AI-Powered Resume & Interview Assistant")

# CORS for frontend (optional)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "AI Resume & Interview Assistant API is running."}

@app.post("/generate_resume")
async def resume_endpoint(request: Request):
    data = await request.json()
    return generate_resume(data)

@app.post("/generate_cover_letter")
async def cover_letter_endpoint(request: Request):
    data = await request.json()
    return generate_cover_letter(data)

@app.post("/mock_interview")
async def interview_endpoint(request: Request):
    data = await request.json()
    return JSONResponse(content=mock_interview(data))

@app.post("/analyze_job")
async def job_fit_endpoint(request: Request):
    data = await request.json()
    return JSONResponse(content=analyse_job(data))
