# backend/chatbot.py

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

# Logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

# Config
load_dotenv()
API_KEY    = os.getenv("NVIDIA_API_KEY", "")
RESUME_PDF = "Vishwajit_Resume_250603_101508.pdf"
if not API_KEY.startswith("nvapi-"):
    raise RuntimeError("Invalid NVIDIA_API_KEY")

# Load resume

def load_resume(path: str, max_chars=15000) -> str:
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

logger.info("Loading resume from %s", RESUME_PDF)
RESUME_TEXT = load_resume(RESUME_PDF)

# LLM client
llm = ChatNVIDIA(
    model="meta/llama-3.3-70b-instruct",
    temperature=0.2,
    top_p=0.7,
    streaming=True,
    api_key=API_KEY,
)

SYSTEM_PROMPT = (
    "You are Vishwajit Singh’s AI portfolio assistant. Use the following resume as context:\n\n"
    f"{RESUME_TEXT}\n\n"
    "Answer clearly and concisely."
)

# FastAPI
app = FastAPI(title="Portfolio Chatbot")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5500"],
    allow_methods=["GET"],
    allow_headers=["*"],
)

@app.get("/chat/stream")
async def chat_stream(request: Request):
    user_msg = request.query_params.get("message", "").strip()
    if not user_msg:
        raise HTTPException(400, "Missing 'message' query param")

    logger.info("Chat request: %s", user_msg)

    async def event_generator():
        try:
            # send system + user
            messages = [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user",   "content": user_msg},
            ]
            # stream tokens
            async for chunk in llm.astream(messages):
                if await request.is_disconnected():
                    break
                content = getattr(chunk, 'content', None)
                if content:
                    yield f"data: {json.dumps({'reply': content})}\n\n"
                await asyncio.sleep(0.01)
            # signal end-of-stream
            yield "event: end\ndata: {}\n\n"
        except Exception as e:
            logger.exception("Streaming error")
            yield f"data: {json.dumps({'error': str(e)})}\n\n"

    return StreamingResponse(event_generator(), media_type="text/event-stream")