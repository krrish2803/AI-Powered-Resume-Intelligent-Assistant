# app.py
import streamlit as st
import requests
import json

st.set_page_config(page_title="AI Resume & Interview Assistant", layout="wide")
st.markdown("""
    <style>
        .title { font-size: 36px; font-weight: 700; color: #1f2937; margin-bottom: 10px; }
        .subtitle { font-size: 20px; color: #4b5563; }
        .card { background-color: #f9fafb; padding: 20px; border-radius: 12px; box-shadow: 0 2px 8px rgba(0,0,0,0.05); margin-bottom: 20px; }
        .button { background-color: #3b82f6; color: white; padding: 10px 20px; border: none; border-radius: 8px; cursor: pointer; }
        .button:hover { background-color: #2563eb; }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="title">📄 AI-Powered Resume & Interview Assistant</div>', unsafe_allow_html=True)
st.sidebar.title("Navigation")
task = st.sidebar.radio("Select Feature", ["Generate Resume", "Generate Cover Letter", "Mock Interview", "Job Fit Analyzer"])

API_URL = "http://localhost:8000"

if task == "Generate Resume":
    st.markdown('<div class="subtitle">✍️ Resume Generator</div>', unsafe_allow_html=True)
    with st.container():
        name = st.text_input("Full Name")
        email = st.text_input("Email")
        phone = st.text_input("Phone")
        education = st.text_area("Education (degree|institution|year per line)")
        skills = st.text_area("Skills (comma-separated)")
        experience = st.text_area("Experience (title|company|year per line)")
        projects = st.text_area("Projects (title|description per line)")

        if st.button("Generate Resume", type="primary"):
            edu_list = [dict(zip(["degree", "institution", "year"], e.split("|"))) for e in education.splitlines() if "|" in e]
            exp_list = [dict(zip(["title", "company", "year"], e.split("|"))) for e in experience.splitlines() if "|" in e]
            proj_list = [dict(zip(["title", "description"], p.split("|"))) for p in projects.splitlines() if "|" in p]
            payload = {
                "name": name,
                "email": email,
                "phone": phone,
                "education": edu_list,
                "skills": [s.strip() for s in skills.split(",")],
                "experience": exp_list,
                "projects": proj_list
            }
            res = requests.post(f"{API_URL}/generate_resume", json=payload)
            if res.status_code == 200:
                with open("resume.docx", "wb") as f:
                    f.write(res.content)
                st.success("Resume generated successfully!")
                st.download_button("📄 Download Resume", data=res.content, file_name="Resume.docx")
            else:
                st.error("Error generating resume. Please check your input.")

elif task == "Generate Cover Letter":
    st.markdown('<div class="subtitle">📨 Cover Letter Generator</div>', unsafe_allow_html=True)
    with st.container():
        name = st.text_input("Your Name")
        email = st.text_input("Email")
        phone = st.text_input("Phone")
        job_title = st.text_input("Job Title")
        company = st.text_input("Company Name")
        summary = st.text_area("Short Summary from Resume")

        if st.button("Generate Cover Letter"):
            payload = {
                "name": name,
                "email": email,
                "phone": phone,
                "job_title": job_title,
                "company": company,
                "summary": summary
            }
            res = requests.post(f"{API_URL}/generate_cover_letter", json=payload)
            if res.status_code == 200:
                with open("cover_letter.docx", "wb") as f:
                    f.write(res.content)
                st.success("Cover Letter generated!")
                st.download_button("📄 Download Cover Letter", data=res.content, file_name="Cover_Letter.docx")
            else:
                st.error("Error generating cover letter.")

elif task == "Mock Interview":
    st.markdown('<div class="subtitle">🧠 Mock Interview Coach</div>', unsafe_allow_html=True)
    with st.container():
        role = st.text_input("Target Role")
        skills = st.text_area("Skills (comma-separated)")

        if st.button("Start Interview"):
            payload = {"role": role, "skills": [s.strip() for s in skills.split(",")], "answers": []}
            qres = requests.post(f"{API_URL}/mock_interview", json=payload).json()
            st.session_state["questions"] = qres.get("questions", [])

        if "questions" in st.session_state:
            answers = []
            for idx, q in enumerate(st.session_state["questions"]):
                ans = st.text_area(f"{idx+1}. {q}", key=f"answer_{idx}")
                answers.append(ans)

            if st.button("Submit Answers & Get Feedback"):
                payload = {
                    "role": role,
                    "skills": [s.strip() for s in skills.split(",")],
                    "answers": answers
                }
                result = requests.post(f"{API_URL}/mock_interview", json=payload).json()
                for fb in result.get("feedback", []):
                    st.markdown(f"**Q:** {fb['question']}")
                    st.markdown(f"**Your Answer:** {fb['answer']}")
                    st.info(f"**Feedback:** {fb['feedback']}")

elif task == "Job Fit Analyzer":
    st.markdown('<div class="subtitle">📊 Job Fit Analyzer</div>', unsafe_allow_html=True)
    with st.container():
        resume_text = st.text_area("Paste Your Resume Text")
        job_description = st.text_area("Paste Job Description")

        if st.button("Analyze Fit"):
            payload = {"resume_text": resume_text, "job_description": job_description}
            result = requests.post(f"{API_URL}/analyze_job_fit", json=payload).json()
            st.write("### 🔍 Analysis Result")
            st.write(result.get("job_fit_analysis", "No insights returned."))
