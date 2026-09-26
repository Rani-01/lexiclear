import hashlib
from collections import OrderedDict
from fastapi import FastAPI, HTTPException, Request, Response
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field
from core.config import DISCLAIMER_TEXT
from core.gemini_service import analyze_document, compare_documents, ask_question
import os

app = FastAPI(title="LexiClear API", version="1.1.0", docs_url=None, redoc_url=None)

# ----------------- Efficiency: Simple LRU Cache -----------------
class SimpleCache:
    def __init__(self, capacity: int = 100):
        self.cache = OrderedDict()
        self.capacity = capacity

    def get(self, key: str):
        if key in self.cache:
            self.cache.move_to_end(key)
            return self.cache[key]
        return None

    def set(self, key: str, value):
        if key in self.cache:
            self.cache.move_to_end(key)
        self.cache[key] = value
        if len(self.cache) > self.capacity:
            self.cache.popitem(last=False)

lru_cache = SimpleCache(capacity=50)

def hash_payload(*args) -> str:
    return hashlib.sha256(":::".join(args).encode("utf-8")).hexdigest()

# ----------------- Security: Headers Middleware -----------------
@app.middleware("http")
async def add_security_headers(request: Request, call_next):
    response: Response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    response.headers["Content-Security-Policy"] = (
        "default-src 'self'; script-src 'self' 'unsafe-inline' https://cdn.tailwindcss.com; "
        "style-src 'self' 'unsafe-inline'; font-src 'self';"
    )
    return response

# ----------------- Request Models with Strict Bounds -----------------
class AnalyzeRequest(BaseModel):
    document_text: str = Field(..., min_length=20, max_length=50000)

class CompareRequest(BaseModel):
    doc_a: str = Field(..., min_length=10, max_length=30000)
    doc_b: str = Field(..., min_length=10, max_length=30000)

class QuestionRequest(BaseModel):
    document_text: str = Field(..., min_length=10, max_length=50000)
    question: str = Field(..., min_length=3, max_length=500)

@app.get("/api/health")
def health_check():
    return {"status": "ok", "service": "LexiClear", "disclaimer": DISCLAIMER_TEXT}

@app.post("/api/analyze")
def handle_analyze(req: AnalyzeRequest):
    cache_key = hash_payload("analyze", req.document_text)
    cached = lru_cache.get(cache_key)
    if cached:
        return {"status": "success", "disclaimer": DISCLAIMER_TEXT, "data": cached, "cached": True}

    try:
        data = analyze_document(req.document_text)
        lru_cache.set(cache_key, data)
        return {"status": "success", "disclaimer": DISCLAIMER_TEXT, "data": data, "cached": False}
    except Exception:
        raise HTTPException(status_code=500, detail="Document analysis processing failed. Please check format.")

@app.post("/api/compare")
def handle_compare(req: CompareRequest):
    cache_key = hash_payload("compare", req.doc_a, req.doc_b)
    cached = lru_cache.get(cache_key)
    if cached:
        return {"status": "success", "disclaimer": DISCLAIMER_TEXT, "data": cached, "cached": True}

    try:
        data = compare_documents(req.doc_a, req.doc_b)
        lru_cache.set(cache_key, data)
        return {"status": "success", "disclaimer": DISCLAIMER_TEXT, "data": data, "cached": False}
    except Exception:
        raise HTTPException(status_code=500, detail="Contract comparison processing failed.")

@app.post("/api/ask")
def handle_ask(req: QuestionRequest):
    cache_key = hash_payload("ask", req.document_text, req.question)
    cached = lru_cache.get(cache_key)
    if cached:
        return {"status": "success", "disclaimer": DISCLAIMER_TEXT, "answer": cached, "cached": True}

    try:
        answer = ask_question(req.document_text, req.question)
        lru_cache.set(cache_key, answer)
        return {"status": "success", "disclaimer": DISCLAIMER_TEXT, "answer": answer, "cached": False}
    except Exception:
        raise HTTPException(status_code=500, detail="Document Q&A query failed.")

@app.get("/", response_class=HTMLResponse)
def serve_home():
    if os.path.exists("static/index.html"):
        with open("static/index.html", "r", encoding="utf-8") as f:
            return f.read()
    return HTMLResponse(content="<h1>LexiClear Service Active</h1>", status_code=200)