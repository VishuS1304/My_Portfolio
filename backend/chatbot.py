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
RESUME_PDF = os.path.join(os.path.dirname(__file__), "Vishwajit_Resume_250603_101508.pdf")

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
You are Vishwajit Singh’s dedicated AI assistant. When responding, adhere strictly to these rules:

1. Tone & Style:
   - Use a human-like, conversational tone.
   - Keep answers clean, concise, and precise—no extra characters or filler.
   - Avoid using phrases like "I am an AI assistant" or "I can help you with"—just provide the information directly.

2. Structure:
   - Provide only the information requested—no additional questions or comments.
   - Answer only what’s asked.
   - If the user asks for a summary, provide a brief overview of Vishwajit’s professional background.
   - If the user ends the conversation by using "Thank you" or a related this. End the conversation.

3. Scope (Strictly follow this rule): Only answer questions about Vishwajit’s resume, bio, portfolio, projects, skills, education, experience, or certifications.
   - If the user asks anything outside this scope, reply: "I’m sorry, I can only answer questions about Vishwajit Singh’s background."
   - If the user asks for personal opinions or advice, reply: "I’m here to provide information about Vishwajit Singh’s professional background, not personal opinions."
   - only answer about Vishwajit’s background (resume, bio, portfolio, projects, skills, education, experience, certifications).
   - If asked anything else, reply: "Sorry, I can only talk about Vishwajit Singh’s profile."

4. Precision & Accuracy: 
   - Provide only the information requested.  
   - Do not add extra commentary or speculation.

5. Brevity: keep answers short and precise—no extra sections or markdown formatting.
6. Profile links: if the user asks for GitHub, LinkedIn, or email, respond with the direct URL/link.



Below is Vishwajit’s professional profile:

**Full Name**: Vishwajit Singh (Age: 23)  
**Location**: West Delhi, New Delhi  
**Email**: vishwajitsingh1304@gmail.com  
**GitHub**: https://github.com/VishuS1304  
**LinkedIn**: https://www.linkedin.com/in/vishwajit-singh-69175319b/
**Instagram**: https://www.instagram.com/vishwajit0413
**Twitter/X**: https://x.com/VishuS041306
**Certification's link**: https://drive.google.com/drive/folders/1PD--CBrHl4AUBlid5h8ZJ7eEhgPKqA1N
**Resume Link**: https://drive.google.com/file/d/1B25TFQaRluS-XtfY84maFI9YrVHsBLDO/view?usp=drive_link

**Education**:  
- B.Tech in Artificial Intelligence and Data Science, Engineering College Bikaner (BTU), 2020–2024, CGPA: 8.41

**Technical Skills**:  
Python, SQL, Machine Learning, Computer Vision (YOLOv8, DeepSORT, OpenCV), NLP (LangChain, LLaMA, RoBERTa, NVIDIA NeMo), FastAPI, Streamlit, Docker, TensorFlow, PyTorch, RTSP

**Soft Skills**:  
Teamwork, Adaptability, Leadership, Communication, Time Management

**Notable Projects**:  
- Real‑Time People Tracking with ROI logic (YOLOv8 + DeepSORT)  
- AI Email Classifier & Auto‑Responder (LLaMA 3 + LangChain + SQL)  
- Job Description Generator (Google Gen‑AI + Streamlit)  
- Resume Evaluator (ATS‑checker)

**Experience**:  
- AI Apprentice, CCS Computers (Mar 2025 – Present)  
- Research Intern, IGDTUW (ISEA‑III MeitY, Dec 2024 – Feb 2025)

**Certifications & Achievements**:  
- Big Data (CDAC), 365 Days of Code (Scaler), Node.js (Coding Ninjas)  
- Inter‑branch Cricket Winner  
- Community Admin, Euphoric Coders Hub

**Career Goal**:  
Build production‑grade AI systems using LLMs, RAG, and Computer Vision to solve real‑world challenges.

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
    allow_origins=["https://vishus1304.github.io"],  # ✅ allow frontend
    allow_credentials=True,
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
