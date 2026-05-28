from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from src.ai_logic import generate_cold_email

app = FastAPI(
    title="AI Cold Email Service API",
    description="A highly scalable, production-grade API for generating context-aware cold emails.",
    version="2.0.0"
)

# CRITICAL FOR PRODUCTION: Allows frontends (React, Webflow, Flutter, etc.) to query your API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, swap "*" for your specific frontend URL to restrict access
    allow_credentials=True,
    allow_methods=["*"],  # Allows GET, POST, OPTIONS, etc.
    allow_headers=["*"],
)

# --- Request & Response Schemas ---
class EmailRequest(BaseModel):
    name: str = Field(default="Candidate", examples=["Muhammad Fassi"])
    role: str = Field(default="", examples=["AI/ML Engineer"])
    company: str = Field(default="", examples=["TechCorp"])
    portfolio_link: str = Field(default="", examples=["https://github.com/username"])
    resume_text: str = Field(default="", examples=["Experienced in building FastAPI backends and deep learning models..."])
    job_description: str = Field(default="", examples=["Looking for an AI Engineer proficient in Python and deployment..."])
    model_name: str = Field(default="llama-3.3-70b-versatile", description="Target Groq model identifier")
    temperature: float = Field(default=0.7, ge=0.0, le=1.0)

class EmailResponse(BaseModel):
    email: str
    status: str = "success"

# --- Endpoints ---
@app.post("/api/v1/generate-email", response_model=EmailResponse)
async def generate_email_endpoint(payload: EmailRequest):
    """
    Accepts candidate parameters and generates a highly targeted professional cold email.
    """
    try:
        email_content = generate_cold_email(
            name=payload.name,
            role=payload.role,
            company=payload.company,
            portfolio_link=payload.portfolio_link,
            resume_text=payload.resume_text,
            job_description=payload.job_description,
            model_name=payload.model_name,
            temperature=payload.temperature
        )
        return {"email": email_content, "status": "success"}

    except Exception as e:
        # Prevent leaking raw backend tracing while reporting processing failure codes
        raise HTTPException(status_code=500, detail=f"Inference failure: {str(e)}")

@app.get("/health")
def health_check():
    """Liveness probe used by automated platform load-balancers to confirm status."""
    return {"status": "alive", "version": "2.0.0"}