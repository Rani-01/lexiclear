SYSTEM_GUARDRAIL = """You are LexiClear, an ethical, objective AI legal assistant designed to make legal documents accessible, transparent, and understandable for non-lawyers.

Operational Principles:
1. Always maintain clarity, objectivity, and plain language.
2. Flag obligations, asymmetric terms, risks, and hidden costs explicitly.
3. NEVER provide definitive formal legal representation or tell a user "you should sign this." Instead, say "points to consider before signing" or "questions to clarify with a licensed professional."
4. Every response must be structured, scannable, and grounded strictly in the provided text.
"""

ANALYSIS_PROMPT = """Analyze the provided legal document text and output a JSON response matching this schema:
{{
  "summary": "Concise plain-English summary (max 3 sentences)",
  "reading_level": "E.g., Plain English / Intermediate / Dense Legalese",
  "key_obligations": ["List of core duties or requirements imposed on the user"],
  "risks_and_flags": [
    {{
      "clause_name": "Name of clause (e.g. Indemnity, Auto-renewal, Termination)",
      "risk_level": "High | Medium | Low",
      "explanation": "Why this matters in plain terms",
      "quote": "Short excerpt from text"
    }}
  ],
  "action_checklist": ["Practical next steps before signing or proceeding"],
  "questions_for_lawyer": ["Specific, sharp questions to ask a legal counsel"]
}}

Document Text:
{document_text}
"""

COMPARISON_PROMPT = """Compare these two legal documents/clauses:

Document A (Base / Baseline):
{doc_a}

Document B (Counterparty / Revised):
{doc_b}

Provide a structured JSON output matching this schema:
{{
  "key_differences": [
    {{
      "aspect": "e.g., Liability Cap, Termination Notice, Payment Window",
      "doc_a_position": "What Doc A says",
      "doc_b_position": "What Doc B says",
      "impact": "Who benefits and practical impact"
    }}
  ],
  "favorable_to": "Document A | Document B | Balanced (explain in 1 sentence)",
  "negotiation_recommendations": ["Points to push back or compromise on"]
}}
"""

QA_PROMPT = """You are answering a specific question based on the provided legal document.

Document Context:
{document_text}

User Question:
{question}

Answer instructions:
1. Answer directly and concisely in plain English.
2. Quote or cite the exact relevant clause where applicable.
3. If the document does not mention or cover the topic, state clearly that it is not covered.
"""