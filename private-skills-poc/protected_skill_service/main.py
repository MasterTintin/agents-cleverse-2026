"""
Protected Skill Service
========================
หัวใจของ POC: พิสูจน์ว่า Secret Logic (prompt/เกณฑ์การประเมินภายในองค์กร)
สามารถอยู่เบื้องหลัง service นี้ได้ โดยที่ input/output ที่ผ่าน API ไม่มี
วันมี prompt ลับหลุดออกไป

Skill นี้คือ "Internal Document Edit Skill" — รับ "เอกสาร" แล้ววิเคราะห์
ตามเกณฑ์ภายในองค์กร แล้วคืนเป็นคำสั่งแก้ไข (ไม่ใช่ข้อความประเมินอิสระ)

เรียก Claude ผ่าน OpenRouter's Anthropic-compatible endpoint (ไม่ใช่
Anthropic API ตรงๆ) — ใช้ Anthropic SDK เดิม แค่เปลี่ยน base_url/auth:
  - base_url ต้องเป็น "https://openrouter.ai/api" (ไม่มี /v1 ต่อท้าย
    เพราะ SDK จะเติม "/v1/messages" ให้เองอัตโนมัติ)
  - ต้องใช้ auth_token= (ส่ง Authorization: Bearer) ไม่ใช่ api_key=
    (ส่ง x-api-key) เพราะ OpenRouter authenticate ด้วย Bearer token
    เท่านั้น

Endpoint เดียว: POST /execute
Input:  {"document": "..."}
Output: {"instructions": [{"old_str": "...", "new_str": "...", "reason": "..."}, ...]}
"""


import json
import os
import traceback
 
from anthropic import Anthropic
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
 
from prompt import SECRET_SYSTEM_PROMPT
 
load_dotenv()
 
# manifest.json คือ "public description" ของ Skill นี้ — สิ่งที่ Client
# ต้องรู้เพื่อจะเรียกใช้ (name, description, input/output shape) แยก
# ไฟล์จาก prompt.py (secret) โดยเจตนา ตาม Public vs Private breakdown
# ใน docs/research/agents-research.md
with open(os.path.join(os.path.dirname(__file__), "manifest.json")) as f:
    SKILL_MANIFEST = json.load(f)
 
SKILL_PORT = int(os.getenv("SKILL_PORT", "8001"))
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_BASE_URL = "https://openrouter.ai/api"
MODEL_NAME = "anthropic/claude-sonnet-4"
MAX_TOKENS = 1500
 
# ชื่อ tool ที่บังคับให้ Claude ต้องเรียกเพื่อตอบกลับ — การบังคับผ่าน
# tool_choice ทำให้ response เป็น JSON ตาม schema นี้เสมอ 
SUBMIT_INSTRUCTIONS_TOOL = {
    "name": "submit_edit_instructions",
    "description": (
        "ส่งรายการคำสั่งแก้ไขเอกสาร แต่ละคำสั่งระบุ exact substring ที่จะ "
        "หา (old_str) และข้อความที่จะแทนที่ (new_str)"
    ),
    "input_schema": {
        "type": "object",
        "properties": {
            "instructions": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "old_str": {
                            "type": "string",
                            "description": "exact substring เดิมในเอกสาร ต้อง unique",
                        },
                        "new_str": {
                            "type": "string",
                            "description": "ข้อความที่จะแทนที่ old_str",
                        },
                        "reason": {
                            "type": "string",
                            "description": "คำอธิบายสั้นๆ ว่าทำไมถึงแก้ตรงนี้ (โชว์ให้ user เห็น)",
                        },
                    },
                    "required": ["old_str", "new_str", "reason"],
                },
            },
        },
        "required": ["instructions"],
    },
}
 
app = FastAPI(title="Protected Skill Service - Instruction-based Editing")
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
 
 
class Instruction(BaseModel):
    old_str: str
    new_str: str
    reason: str
 
 
class ExecuteResponse(BaseModel):
    instructions: list[Instruction]
 
 
def extract_instructions(message) -> list[dict]:
    """
    ดึง instructions ออกจาก tool_use block ของ Claude response
 
    แยกออกมาเป็นฟังก์ชันเดี่ยวๆ ไม่ผูกกับ client.messages.create() เลย
    เพื่อให้ unit test ได้ตรงๆ โดยจำลอง message.content เป็น object ปลอม
    โดยไม่ต้องเรียก API จริง
    """
    for block in message.content:
        if block.type == "tool_use" and block.name == "submit_edit_instructions":
            return block.input.get("instructions", [])
    raise RuntimeError("Claude ไม่ได้เรียก submit_edit_instructions tool กลับมา")
 
 
def run_skill(document: str) -> list[dict]:
    """
    Business logic ล้วนๆ: รับเอกสาร -> เรียก Claude (ผ่าน OpenRouter) ด้วย
    secret prompt พร้อมบังคับ tool_use -> คืน list ของ edit instructions
    (ไม่ผูกกับ FastAPI/HTTP เลย ทำให้ unit test ตรงๆ ได้โดยไม่ต้องยิง
    request ผ่าน endpoint)
    """
    if client is None:
        raise RuntimeError("OPENROUTER_API_KEY ยังไม่ได้ตั้งค่า (ดู .env.example)")
 
    try:
        message = client.messages.create(
            model=MODEL_NAME,
            max_tokens=MAX_TOKENS,
            system=SECRET_SYSTEM_PROMPT,
            messages=[{"role": "user", "content": document}],
            tools=[SUBMIT_INSTRUCTIONS_TOOL],
            tool_choice={"type": "tool", "name": "submit_edit_instructions"},
        )
    except Exception as exc:  # เช่น API ล่ม, rate limit, network error
        # DEBUG: พิมพ์ full traceback ออกที่ terminal ฝั่ง server เท่านั้น
        # เพื่อดู exception type จริง
        traceback.print_exc()
        raise RuntimeError(f"เรียก Claude ไม่สำเร็จ: {exc}") from exc
 
    return extract_instructions(message)
 
 
@app.get("/health")
def health():
    return {"status": "ok"}
 
 
@app.get("/skills")
def skills():
    """
    Capability discovery — บอก client ว่า Skill นี้ทำอะไรได้ โดยไม่ต้อง
    เปิดเผย prompt หรือ implementation เลย คืนเป็น list
    """
    return [SKILL_MANIFEST]
 
 
@app.post("/execute", response_model=ExecuteResponse)
def execute(payload: ExecuteRequest):
    """
    Endpoint: validate เบื้องต้น -> เรียก run_skill -> ออกมาเป็น response
    """
    if not payload.document.strip():
        raise HTTPException(status_code=400, detail="document ต้องไม่ว่างเปล่า")
 
    try:
        instructions = run_skill(payload.document)
    except RuntimeError as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc
 
    return ExecuteResponse(instructions=instructions)
 
 
if __name__ == "__main__":
    import uvicorn
 
    uvicorn.run(app, host="0.0.0.0", port=SKILL_PORT)