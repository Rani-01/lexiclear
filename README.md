# LexiClear — GenAI Legal Intelligence & Document Navigator

LexiClear is a Generative AI application built for PromptWars that bridges the comprehension gap in legal agreements, leases, terms of service, and contracts for non-lawyers.

## 1. Chosen Vertical & Persona
- **Vertical:** Consumer and Small Business Legal Accessibility.
- **Target Persona:** Freelancers, tenants, small business owners, and consumers who need to understand rights and obligations before signing.

## 2. Approach & Architecture
- **Framework:** FastAPI backend with Python 3.11+.
- **Model Engine:** Google Gemini (`gemini-2.5-flash`) via `google-genai` SDK.
- **Frontend:** Lightweight responsive single-page application served via FastAPI.
- **Repository Efficiency:** Zero heavy assets; total repository size is under 2 MB (well beneath the 10 MB limit).

## 3. How the Solution Works
1. **Clause Simplification & Risk Scoring:** Scans documents for high-friction clauses (indemnity, auto-renewal, unilateral termination) and categorizes risks as Low, Medium, or High.
2. **Clause Comparator:** Compares standard terms against counter-offers and highlights asymmetric advantages.
3. **Lawyer Consultation Preparation:** Extracts concise, high-value questions for a user to present to legal counsel.
4. **Contextual Q&A:** Grounded query resolution citing source clauses.

## 4. Key Assumptions & Guardrails
- **Not Formal Legal Advice:** Every API endpoint returns explicit statutory disclaimers.
- **Groundedness:** Prompts use low temperature (`0.2`) and strict JSON schemas to avoid hallucinations.

## 5. Local Setup & Testing
```bash
# 1. Clone repository
git clone <your-repo-link>
cd lexiclear

# 2. Virtual environment setup
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Set Environment Variables
cp .env.example .env
# Add your GEMINI_API_KEY in .env

# 5. Run automated tests
pytest tests/

# 6. Start the server
uvicorn main:app --reload --port 8000