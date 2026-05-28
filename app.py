import os
import re
import PyPDF2
import streamlit as st
import requests
from dotenv import load_dotenv

# ---------- Setup & Configuration ----------
load_dotenv()
st.set_page_config(page_title="AI Cold Email Assistant", page_icon="📧", layout="centered")

# Your production cloud URL from your Hugging Face Docker deployment
API_URL = "https://fassiurrehman-ai-cold-email-backend.hf.space/api/v1/generate-email"

# Ensure static directory exists for secure file processing buffers
if not os.path.exists("static"):
    os.makedirs("static")

# ---------- UI Header ----------
st.title("📧 AI Cold Email Assistant")
st.markdown("""
    Generate high-converting cold emails for your job hunt. 
    *Fill in the details below to get started.*
""")

# ---------- Input Section ----------
with st.container():
    col_a, col_b = st.columns(2)
    with col_a:
        name = st.text_input("Your Name", placeholder="e.g. John Doe")
        company = st.text_input("Target Company", placeholder="e.g. Google")
    with col_b:
        role = st.text_input("Target Role", placeholder="e.g. Software Engineer")
        portfolio_link = st.text_input("Portfolio / LinkedIn Link", placeholder="https://...")

# Content Sources
st.divider()
col1, col2 = st.columns(2)
with col1:
    resume_file = st.file_uploader("Upload Resume (PDF or TXT)", type=["pdf", "txt"])

with col2:
    job_description = st.text_area("Paste Job Description (Optional)", height=150)

# ---------- Sidebar Settings ----------
with st.sidebar:
    st.header("⚙️ Model Settings")
    model_name = st.selectbox(
        "Select Model",
        ["llama-3.3-70b-versatile", "llama-3.1-8b-instant", "gemma2-9b-it"],
        help="Llama-3.3 is usually the most balanced for writing tasks."
    )
    
    temperature = st.slider("Creativity Level", 0.0, 1.0, 0.7, 0.1)
    show_debug = st.checkbox("Show Debug Details")

# ---------- Logic Functions ----------
def extract_resume_text(uploaded_file):
    """Extracts text from uploaded PDF or TXT."""
    if uploaded_file is None:
        return ""
    
    try:
        if uploaded_file.name.endswith(".txt"):
            return uploaded_file.read().decode("utf-8")
        
        elif uploaded_file.name.endswith(".pdf"):
            pdf_reader = PyPDF2.PdfReader(uploaded_file)
            text = "".join([page.extract_text() or "" for page in pdf_reader.pages])
            return re.sub(r"\n{3,}", "\n\n", text.strip())
    except Exception as e:
        st.error(f"Error reading file: {e}")
        return ""

# ---------- Action & API Integration ----------
if st.button("Generate Cold Email ✨", type="primary", use_container_width=True):
    resume_text = extract_resume_text(resume_file)
    
    # Validation check
    if not (resume_text or job_description or portfolio_link):
        st.error("⚠️ Please provide at least a Resume, Job Description, or Portfolio link.")
    else:
        try:
            with st.spinner("🤖 AI is drafting your email via live production API..."):
                
                # 1. Structure the JSON payload exactly matching your FastAPI Pydantic schema
                payload = {
                    "name": name.strip(),
                    "role": role.strip(),
                    "company": company.strip(),
                    "portfolio_link": portfolio_link.strip(),
                    "resume_text": resume_text,
                    "job_description": job_description.strip(),
                    "model_name": model_name,
                    "temperature": temperature
                }
                
                # 2. Transmit HTTP POST request across the network with an explicit timeout safety barrier
                response = requests.post(API_URL, json=payload, timeout=60)
                
                # 3. Intercept HTTP response status metrics
                if response.status_code == 200:
                    result_data = response.json()
                    # Safely reference the dictionary key your FastAPI backend returns
                    email_text = result_data.get("email", "No text returned from API server.")
                    
                    st.success("Email Generated via Live Cloud API!")
                    
                    if show_debug:
                        st.write(f"**Debug Info:** HTTP Status: {response.status_code} | Target Gateway: {API_URL}")

                    st.subheader("Your Draft")
                    st.code(email_text, language="text")
                    st.info("💡 Tip: Review and personalize the brackets before sending!")
                
                else:
                    st.error(f"Backend API Error ({response.status_code}): {response.text}")

        except requests.exceptions.Timeout:
            st.error("⚠️ The connection to your cloud API timed out. Your model may still be processing the heavy generation layer.")
        except Exception as e:
            st.error(f"Failed to establish a pipeline to the remote API service: {str(e)}")