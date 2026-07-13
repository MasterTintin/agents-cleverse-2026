"""
Protected Skill Service
========================
หัวใจของ POC: พิสูจน์ว่า Secret Logic (prompt/เกณฑ์การประเมินภายในองค์กร)
สามารถอยู่เบื้องหลัง service นี้ได้ โดยที่ input/output ที่ผ่าน API ไม่มี
วันมี prompt ลับหลุดออกไป

Skill นี้คือ "Internal Document Review Skill" — รับ "เอกสาร" แล้วประเมิน
ตามเกณฑ์ภายในองค์กร

เรียก Claude ผ่าน OpenRouter's Anthropic-compatible endpoint (ไม่ใช่
Anthropic API ตรงๆ) — ใช้ Anthropic SDK เดิม แค่เปลี่ยน base_url/auth:
  - base_url ต้องเป็น "https://openrouter.ai/api" (ไม่มี /v1 ต่อท้าย
    เพราะ SDK จะเติม "/v1/messages" ให้เองอัตโนมัติ)
  - ต้องใช้ auth_token= (ส่ง Authorization: Bearer) ไม่ใช่ api_key=
    (ส่ง x-api-key) เพราะ OpenRouter authenticate ด้วย Bearer token
    เท่านั้น

Endpoint เดียว: POST /execute
Input:  {"document": "..."}
Output: {"result": "..."}
"""

import os
import traceback

from anthropic import Anthropic
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from prompt import SECRET_SYSTEM_PROMPT

load_dotenv()

SKILL_PORT = int(os.getenv("SKILL_PORT", "8001"))
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_BASE_URL = "https://openrouter.ai/api"
MODEL_NAME = "anthropic/claude-sonnet-4"
MAX_TOKENS = 1024

app = FastAPI(title="Protected Skill Service - Internal Document Review")
client = (
    Anthropic(
        auth_token=OPENROUTER_API_KEY,
        base_url=OPENROUTER_BASE_URL,
    )
    if OPENROUTER_API_KEY
    else None
)


class ExecuteRequest(BaseModel):
    document: str


class ExecuteResponse(BaseModel):
    result: str


def run_skill(document: str) -> str:
    """
    Business logic ล้วนๆ: รับเอกสาร -> เรียก Claude (ผ่าน OpenRouter) ด้วย
    secret prompt -> คืนแค่ข้อความผลลัพธ์
    """
    if client is None:
        raise RuntimeError("OPENROUTER_API_KEY")

    try:
        message = client.messages.create(
            model=MODEL_NAME,
            max_tokens=MAX_TOKENS,
            system=SECRET_SYSTEM_PROMPT,
            messages=[{"role": "user", "content": document}],
        )
    except Exception as exc:  # เช่น API ล่ม, rate limit, network error
        # DEBUG: พิมพ์ full traceback ออกที่ terminal ฝั่ง server เท่านั้น
        # เพื่อดู exception type จริง
        traceback.print_exc()
        raise RuntimeError(f"เรียก Claude ไม่สำเร็จ: {exc}") from exc

    return "".join(block.text for block in message.content if block.type == "text")


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/execute", response_model=ExecuteResponse)
def execute(payload: ExecuteRequest):
    """
    Endpoint: validate เบื้องต้น -> เรียก run_skill -> ออกมาเป็น response
    """
    if not payload.document.strip():
        raise HTTPException(status_code=400, detail="document ต้องไม่ว่างเปล่า")

    try:
        result = run_skill(payload.document)
    except RuntimeError as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc

    return ExecuteResponse(result=result)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=SKILL_PORT)