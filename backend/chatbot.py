import os
import json
import asyncio
import logging
from dotenv import load_dotenv
from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from PyPDF2 import PdfReader
from langchain_nvidia_ai_endpoints import ChatNVIDIA

# -------------------------------
# Logging Setup
# -------------------------------
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

# -------------------------------
# Load .env and NVIDIA API Key
# -------------------------------
load_dotenv()
API_KEY = os.getenv("NVIDIA_API_KEY", "")
if not API_KEY.startswith("nvapi-"):
    raise RuntimeError("❌ Invalid NVIDIA_API_KEY")

# -------------------------------
# Resume (Optional for additional context)
# -------------------------------
RESUME_PDF = os.path.join(os.path.dirname(__file__), "D:\Vs_code\portfolio_website\Vishwajit_Resume_250603_101508.pdf")

def load_resume(path: str, max_chars=15000) -> str:
    try:
        reader = PdfReader(path)
        pages, total = [], 0
        for page in reader.pages:
            text = page.extract_text() or ""
            if total + len(text) > max_chars:
                pages.append(text[: max_chars - total])
                break
            pages.append(text)
            total += len(text)
        joined = "\n\n".join(pages)
        return joined + ("\n\n…[truncated]" if total > max_chars else "")
    except Exception as e:
        logger.warning(f"Resume loading failed: {e}")
        return "[Resume could not be loaded]"

logger.info("Loading resume from %s", RESUME_PDF)
RESUME_TEXT = load_resume(RESUME_PDF)

# -------------------------------
# Vishwajit’s Profile Prompt
# -------------------------------
PROFILE_SUMMARY = f"""
You are Vishwajit Singh’s intelligent AI assistant. Below is his professional profile:

**Full Name**: Vishwajit Singh (Age: 23)  
**Location**: West Delhi, New Delhi  
**Email**: vishwajitsingh1304@gmail.com  
**GitHub**: https://github.com/VishuS1304  
**LinkedIn**: https://www.linkedin.com/in/vishwajit-singh-69175319b/

**Education**:  
- B.Tech in Artificial Intelligence and Data Science (Engineering College Bikaner, BTU), 2020–2024, CGPA: 8.41

**Technical Skills**:  
Python, SQL, ML, AI, YOLOv8, DeepSORT, OpenCV, LangChain, LLaMA, RoBERTa, NVIDIA NeMo, FastAPI, Streamlit, Docker, RTSP, TensorFlow, PyTorch

**Soft Skills**:  
Teamwork, Adaptability, Leadership, Communication, Time Management

**Notable Projects**:  
- Real-Time People Tracking with ROI logic using YOLOv8 + DeepSORT  
- AI Email Classifier & Auto-Responder (LLaMA 3 + LangChain + SQL)  
- JD Generator (Google Gen-AI + Streamlit)  
- Resume Evaluator (ATS-checker)

**Experience**:  
- AI Apprentice at CCS Computers (Mar 2025 – Present)  
- Research Intern at IGDTUW (ISEA-III MeitY, Dec 2024 – Feb 2025)

**Certifications & Achievements**:  
- Big Data (CDAC), 365 Days of Code (Scaler), Node.js, Coding Ninjas, Inter-branch Cricket Winner  
- Community Admin – Euphoric Coders Hub

**Career Goals**:  
Vishwajit aims to build production-grade AI systems using LLMs, RAG, and Computer Vision to solve real-world problems.

--- Resume Text ---  
{RESUME_TEXT}
"""

# -------------------------------
# LangChain NVIDIA Chat Client
# -------------------------------
llm = ChatNVIDIA(
    model="meta/llama-3.2-3b-instruct",
    temperature=0.2,
    top_p=0.7,
    streaming=True,
    api_key=API_KEY,
)

# -------------------------------
# FastAPI Setup
# -------------------------------
app = FastAPI(title="Vishwajit Singh Portfolio Chatbot")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For production: restrict to portfolio domain
    allow_methods=["GET"],
    allow_headers=["*"],
)

# -------------------------------
# Chat Streaming Endpoint
# -------------------------------
@app.get("/chat/stream")
async def chat_stream(request: Request):
    user_msg = request.query_params.get("message", "").strip()
    if not user_msg:
        raise HTTPException(400, "Missing 'message' query param")

    logger.info("Chat request: %s", user_msg)

    async def event_generator():
        try:
            messages = [
                {"role": "system", "content": PROFILE_SUMMARY},
                {"role": "user", "content": user_msg}
            ]
            async for chunk in llm.astream(messages):
                if await request.is_disconnected():
                    break
                content = getattr(chunk, "content", None)
                if content:
                    yield f"data: {json.dumps({'reply': content})}\n\n"
                await asyncio.sleep(0.01)
            yield "event: end\ndata: {}\n\n"
        except Exception as e:
            logger.exception("Streaming error")
            yield f"data: {json.dumps({'error': str(e)})}\n\n"

    return StreamingResponse(event_generator(), media_type="text/event-stream")
