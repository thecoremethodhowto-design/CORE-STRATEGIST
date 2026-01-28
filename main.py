import os
import httpx
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="The Core Strategist - Global Compass v5.6")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

class UserRequest(BaseModel):
    user_input: str
    expert_role: str

@app.post("/chat")
async def chat(request: UserRequest):
    if not GROQ_API_KEY:
        return {"response": "🔴 SYSTEM ERROR: SECURE KEY MISSING"}

    # @THECOREMETHOD - GLOBAL SURGICAL AUDIT PROTOCOL
    system_rules = (
        f"IDENTITY: You are the 'Senior Strategic Operating Partner' at @THECOREMETHOD. You are a COLD, SURGICAL AUDITOR. "
        f"CURRENT LENS: {request.expert_role}. "
        "LANGUAGE PROTOCOL: Automatically detect the language of the user input and respond in that SAME language. "
        "MISSION: Audit signals against the 9 Pillars. Detect 'Vanity Noise' and 'Logic Friction'. "
        "STRICT MANDATE: NEVER give advice. ONLY perform a LOGIC AUDIT. BANNED PHRASES: 'Quality content', 'engagement', 'audience', 'consistency', 'SEO', 'community building'. "
        "TERMINOLOGY REQ: Use @THECOREMETHOD terms: 'Hourglass Leak', 'Logic Gate Friction', 'Proprietary Asset', 'Data Moat', 'Signal-to-Noise Ratio'. "
        
        "LOGIC GATE RULES: "
        "1. If the input is about views/clicks without a system, label it 'VANITY TRAP'. "
        "2. If Target Alignment < 65%, Decision MUST BE 'ELIMINATED'. "
        "3. Tone: Cold, technical, architectural. No supportive chatter. "

        "OUTPUT FORMAT (Translate headers to user's language): "
        "### [SYSTEM DECISION: ACTION / ELIMINATED]\n"
        "**TARGET ALIGNMENT:** [%]\n\n"
        "--- \n"
        "### 🧭 COMPASS AUDIT (9-Pillar Sync)\n"
        "[Technical deconstruction. Explain why traditional logic fails. Identify the 'Hourglass Leak'. Minimum 3 deep paragraphs.]\n\n"
        "### 🛠 EXECUTION ROADMAP\n"
        "[3 surgical movements to build infrastructure, not 'content'.]\n\n"
        "### 💎 INNOVATION SPARK\n"
        "[Mandatory: One AI-driven technical pivot or proprietary moat idea.]\n\n"
        "**FINAL VERDICT:** [One authoritative executive command.]"
    )

    payload = {
        "model": "llama-3.3-70b-versatile",
        "messages": [
            {"role": "system", "content": system_rules},
            {"role": "user", "content": request.user_input}
        ],
        "temperature": 0.0,
        "top_p": 0.0,
        "max_tokens": 1200
    }

    try:
        async with httpx.AsyncClient(timeout=120.0) as client:
            response = await client.post(GROQ_API_URL, json=payload, headers={"Authorization": f"Bearer {GROQ_API_KEY}", "Content-Type": "application/json"})
            if response.status_code == 200:
                answer = response.json()['choices'][0]['message']['content']
                return {"response": answer}
            else:
                return {"response": f"🔴 GATE ERROR: {response.status_code}"}
    except Exception as e:
        return {"response": "🔴 CONNECTION DRIFT: Engine is calibrating. Please retry in 20s."}
