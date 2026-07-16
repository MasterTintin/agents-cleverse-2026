"""
Skill Gateway
=============
ตัวกลางระหว่าง Frontend กับ Protected Skill Service

หน้าที่: รับ request จาก user, forward เฉพาะ input ที่จำเป็นไปยัง
Protected Skill Service, แล้วส่ง instructions กลับ — Gateway ไม่มีวันเห็น
หรือเก็บ prompt/business logic ลับไว้เลย (ของแบบนั้นอยู่ใน
protected_skill_service/prompt.py เท่านั้น)

Phase 1 (ดู docs/research/12-file-edit-approach.md) เปลี่ยน response ของ
Protected Skill จาก {"result": str} เป็น
{"instructions": [{old_str, new_str, reason}]} — Gateway แค่ relay shape
ใหม่นี้ต่อไปเฉยๆ ไม่ได้ตีความหรือแตะเนื้อหาข้างใน

สำหรับ POC นี้ (Out of Scope: Registry) Gateway hardcode ไว้เลยว่า
ทุก request ที่เข้ามาคือ Protected Skill เดียว ไม่มี logic ตรวจจับ/
เลือก skill หลายตัว
"""

import os

import httpx
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

load_dotenv()

GATEWAY_PORT = int(os.getenv("GATEWAY_PORT", "8000"))
SKILL_SERVICE_URL = os.getenv("SKILL_SERVICE_URL", "http://127.0.0.1:8001")
REQUEST_TIMEOUT_SECONDS = 30

app = FastAPI(title="Skill Gateway")

# เปิด CORS แบบกว้างสำหรับ POC เท่านั้น — ของจริงต้องจำกัด origin ให้แคบกว่านี้
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class ChatRequest(BaseModel):
    message: str


class Instruction(BaseModel):
    old_str: str
    new_str: str
    reason: str


class ChatResponse(BaseModel):
    instructions: list[Instruction]


def is_protected_skill_request(message: str) -> bool:
    """
    Detect ว่า request นี้ควร route ไป Protected Skill หรือไม่

    POC นี้มี Skill เดียวและ hardcode ไว้ว่า route ทุกครั้ง (ตาม
    Out of Scope: ไม่มี Registry/หลาย Skill) — ฟังก์ชันนี้แยกออกมา
    ต่างหากเพื่อให้เห็นชัดว่า "จุดตัดสินใจ" อยู่ตรงไหน เผื่อขยายเป็น
    intent detection จริงในอนาคต (ดู Architecture Hypothesis ใน
    docs/research/07-capafy-competitor-analysis.md)
    """
    return bool(message.strip())


def call_protected_skill(message: str) -> list[dict]:
    """
    ยิง request ไปยัง Protected Skill Service แล้วคืนแค่ instructions

    รับ parameter ชื่อ `message` เพราะในมุมของ Gateway มันคือแค่ข้อความ
    ดิบจาก user เท่านั้น — Gateway ไม่มีหน้าที่ตีความว่าข้อความนี้คือ
    resume, invoice หรือ document ประเภทไหน การตีความความหมายเป็นหน้าที่
    ของ Protected Skill Service
    Gateway ส่งแค่ field ที่ Protected Skill Service คาดหวัง
    เท่านั้น ไม่มีการแนบข้อมูลอื่นที่ไม่เกี่ยวข้อง และไม่มีทางเห็น
    system prompt ที่ใช้ประมวลผลอยู่เบื้องหลังเลย — Gateway เห็นแค่
    old_str/new_str/reason ที่ Protected Skill ตัดสินใจส่งกลับมาแล้ว
    ไม่เห็นว่า Claude คิดยังไงถึงได้คำตอบนี้
    """
    try:
        # Gateway forwards only user input.
        # Secret prompt remains inside Protected Skill Service.
        response = httpx.post(
            f"{SKILL_SERVICE_URL}/execute",
            json={"document": message},
            timeout=REQUEST_TIMEOUT_SECONDS,
        )
        response.raise_for_status()
    except httpx.HTTPStatusError as exc:
        raise RuntimeError(
            f"Protected Skill Service ตอบกลับผิดพลาด: {exc.response.status_code}"
        ) from exc
    except httpx.RequestError as exc:
        raise RuntimeError(f"เชื่อมต่อ Protected Skill Service ไม่ได้: {exc}") from exc

    return response.json()["instructions"]


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/chat", response_model=ChatResponse)
def chat(payload: ChatRequest):
    """
    Endpoint ที่ frontend เรียก — ทำหน้าที่แค่ route + forward เท่านั้น
    ไม่มี business logic ของ skill อยู่ในนี้
    """
    if not payload.message.strip():
        raise HTTPException(status_code=400, detail="message ต้องไม่ว่างเปล่า")

    if not is_protected_skill_request(payload.message):
        raise HTTPException(
            status_code=404, detail="ไม่พบ Skill ที่ตรงกับคำขอ"
        )

    try:
        instructions = call_protected_skill(payload.message)
    except RuntimeError as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc

    return ChatResponse(instructions=instructions)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=GATEWAY_PORT)