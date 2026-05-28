import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

def get_model(model_name: str, temperature: float):
    """Factory to instantiate the cloud LLM runtime client layer securely."""
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError("CRITICAL CONFIGURATION ERROR: 'GROQ_API_KEY' is not populated in the active environment.")
        
    return ChatGroq(
        groq_api_key=api_key,
        model_name=model_name,
        temperature=temperature
    )

PROMPT = ChatPromptTemplate.from_template(
    """
You are an expert career advisor. 
Write a concise, friendly, and professional cold email for a job application based on the profile context detailed below.

- Name: {name}
- Role: {role}
- Company: {company}
- Portfolio/Link: {portfolio_link}
- Resume Text: {resume_text}
- Job Description: {job_description}

Requirements:
1) Suggest an attention-grabbing, relevant subject line at the start.
2) Deeply personalize to the target role/company profile context provided.
3) Smoothly integrate 2–3 key skills/achievements matching the job description parameters.
4) Maintain strict word count constraints: 120–160 words.
5) Output ONLY the finalized email text body. Do not include introductory notes or systemic pleasantries outside the email context.

Best regards, {name}
"""
)

def generate_cold_email(
    name: str,
    role: str,
    company: str,
    portfolio_link: str,
    resume_text: str,
    job_description: str,
    model_name: str,
    temperature: float
) -> str:
    """Invokes the LangChain Expression Language (LCEL) runtime execution pipeline."""
    llm = get_model(model_name, temperature)
    chain = PROMPT | llm | StrOutputParser()

    return chain.invoke({
        "name": name or "Candidate",
        "role": role or "the open position",
        "company": company or "your company",
        "portfolio_link": portfolio_link or "Not provided",
        "resume_text": resume_text or "Not provided",
        "job_description": job_description or "Not provided"
    })