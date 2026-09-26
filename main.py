from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field
from core.config import DISCLAIMER_TEXT
from core.gemini_service import analyze_document, compare_documents, ask_question
import os
import traceback

app = FastAPI(title="LexiClear API", version="1.0.0")

# Schemas
class AnalyzeRequest(BaseModel):
    document_text: str = Field(..., min_length=20)

class CompareRequest(BaseModel):
    doc_a: str = Field(..., min_length=10)
    doc_b: str = Field(..., min_length=10)

class QuestionRequest(BaseModel):
    document_text: str = Field(..., min_length=10)
    question: str = Field(..., min_length=3)

@app.get("/api/health")
def health_check():
    return {"status": "ok", "service": "LexiClear", "disclaimer": DISCLAIMER_TEXT}

@app.post("/api/analyze")
def handle_analyze(req: AnalyzeRequest):
    try:
        data = analyze_document(req.document_text)
        return {"status": "success", "disclaimer": DISCLAIMER_TEXT, "data": data}
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/compare")
def handle_compare(req: CompareRequest):
    try:
        data = compare_documents(req.doc_a, req.doc_b)
        return {"status": "success", "disclaimer": DISCLAIMER_TEXT, "data": data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/ask")
def handle_ask(req: QuestionRequest):
    try:
        answer = ask_question(req.document_text, req.question)
        return {"status": "success", "disclaimer": DISCLAIMER_TEXT, "answer": answer}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Static UI serving
if os.path.exists("static/index.html"):
    @app.get("/", response_class=HTMLResponse)
    def serve_home():
        with open("static/index.html", "r", encoding="utf-8") as f:
            return f.read()