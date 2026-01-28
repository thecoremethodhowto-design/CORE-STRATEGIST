import os
import httpx
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="The Core Strategist - Protocol v6.0")

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

    system_rules = (
        f"IDENTITY: Senior Strategic Auditor (@THECOREMETHOD). LENS: {request.expert_role}. "
        "PROTOCOL: Detect input language. Respond ONLY in that language. No polite fillers. "
        "MANDATE: If input focus is 'views/clicks', flag as 'VANITY TRAP'. "
        "BANNED: 'quality content', 'engagement', 'SEO', 'consistency', 'community'. "
        "REQUIRED: 'Hourglass Leak', 'Logic Gate Friction', 'Data Moat', 'Signal-to-Noise'. "
        "FORMAT: "
        "### [SYSTEM DECISION: ACTION / ELIMINATED]\n"
        "**TARGET ALIGNMENT:** [%]\n\n"
        "--- \n"
        "### 🧭 COMPASS AUDIT\n[3 cold technical paragraphs.]\n\n"
        "### 🛠 EXECUTION ROADMAP\n[3 system-building steps.]\n\n"
        "### 💎 INNOVATION SPARK\n[1 technical pivot.]\n\n"
        "**FINAL VERDICT:** [One command.]"
    )

    payload = {
        "model": "llama-3.3-70b-versatile",
        "messages": [
            {"role": "system", "content": system_rules},
            {"role": "user", "content": request.user_input}
        ],
        "temperature": 0.0,
        "top_p": 0.01,
        "max_tokens": 1000
    }

    try:
        async with httpx.AsyncClient(timeout=120.0) as client:
            response = await client.post(GROQ_API_URL, json=payload, headers={"Authorization": f"Bearer {GROQ_API_KEY}", "Content-Type": "application/json"})
            return {"response": response.json()['choices'][0]['message']['content']}
    except:
        return {"response": "🔴 GATE ERROR: Recalibrating logic nodes..."}
