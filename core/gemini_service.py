import json
from google import genai
from google.genai import types
from core.config import GEMINI_API_KEY, MODEL_NAME
from core.prompts import SYSTEM_GUARDRAIL, ANALYSIS_PROMPT, COMPARISON_PROMPT, QA_PROMPT

client = None
if GEMINI_API_KEY:
    client = genai.Client(api_key=GEMINI_API_KEY)

def get_client() -> genai.Client:
    global client
    if not client:
        api_key = GEMINI_API_KEY
        if not api_key:
            raise ValueError("GEMINI_API_KEY is not configured.")
        client = genai.Client(api_key=api_key)
    return client

def analyze_document(text: str) -> dict:
    ai = get_client()
    prompt = ANALYSIS_PROMPT.format(document_text=text)
    
    response = ai.models.generate_content(
        model=MODEL_NAME,
        contents=prompt,
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM_GUARDRAIL,
            response_mime_type="application/json",
            temperature=0.2,
            max_output_tokens=1500
        )
    )
    return json.loads(response.text)

def compare_documents(doc_a: str, doc_b: str) -> dict:
    ai = get_client()
    prompt = COMPARISON_PROMPT.format(doc_a=doc_a, doc_b=doc_b)
    
    response = ai.models.generate_content(
        model=MODEL_NAME,
        contents=prompt,
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM_GUARDRAIL,
            response_mime_type="application/json",
            temperature=0.2,
            max_output_tokens=1500
        )
    )
    return json.loads(response.text)

def ask_question(doc_text: str, question: str) -> str:
    ai = get_client()
    prompt = QA_PROMPT.format(document_text=doc_text, question=question)
    
    response = ai.models.generate_content(
        model=MODEL_NAME,
        contents=prompt,
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM_GUARDRAIL,
            temperature=0.2,
            max_output_tokens=1500
        )
    )
    return response.text