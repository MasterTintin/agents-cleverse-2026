"""
Skill Gateway
=============
ตัวกลางระหว่าง Frontend กับ Protected Skill Service

หน้าที่ : รับ request จาก user, forward เฉพาะ input ที่จำเป็นไปยัง
Protected Skill Service, แล้วส่ง result กลับ - 
Gateway ไม่มีการเก็บ ประมวลผล หรือเข้าถึง Business Logic ภายในของ Skill โดยตรง

สำหรับ POC นี้ (Out of Scope: Registry) Gateway hardcode ไว้เลยว่า
ทุก request ที่เข้ามาคือ Protected Skill เดียว
ไม่มี logic ตรวจจับ/เลือก skill หลายตัว
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

# เปิด CORS แบบกว้างสำหรับ POC เท่านั้น (frontend/chat.html เป็น static file ที่เปิดจากเครื่อง local)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class ChatRequest(BaseModel):
    message: str


class ChatResponse(BaseModel):
    result: str


def is_protected_skill_request(message: str) -> bool:
    """
    Detect ว่า request นี้ควร route ไป Protected Skill หรือไม่

    POC นี้มี Skill เดียวและ hardcode ไว้ว่า route ทุกครั้ง (ตาม
    Out of Scope: ไม่มี Registry/หลาย Skill) — ฟังก์ชันนี้แยกออกมา
    ต่างหากเพื่อให้เห็นชัดว่า "จุดตัดสินใจ" อยู่ตรงไหน เผื่อขยายเป็น
    intent detection จริงในอนาคต
    """
    return bool(message.strip())


def call_protected_skill(message: str) -> str:
    """
    ยิง request ไปยัง Protected Skill Service แล้วคืนแค่ผลลัพธ์

    รับ parameter ชื่อ `message` เพราะในมุมของ Gateway มันคือแค่ข้อความ
    ดิบจาก user เท่านั้น — Gateway ไม่มีหน้าที่ตีความว่าข้อความนี้คือ
    resume, invoice หรือ document ประเภทไหน การตีความความหมายเป็นหน้าที่
    ของ Protected Skill Service 
    Gateway ส่งแค่ field ที่ Protected Skill Service คาดหวัง (document)
    เท่านั้น ไม่มีการแนบข้อมูลอื่นที่ไม่เกี่ยวข้อง และไม่มีทางเห็น
    system prompt ที่ใช้ประมวลผลอยู่เบื้องหลัง
    """
    try:
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

    return response.json().get("result", "")


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/chat", response_model=ChatResponse)
def chat(payload: ChatRequest):
    """
    Endpoint ที่ frontend เรียกใช้ — ทำหน้าที่แค่ route + forward
    ไม่มี business logic ของ skill
    """
    if not payload.message.strip():
        raise HTTPException(status_code=400, detail="message ต้องไม่ว่างเปล่า")

    if not is_protected_skill_request(payload.message):
        raise HTTPException(
            status_code=404, detail="ไม่พบ Skill ที่ตรงกับคำขอ"
        )

    try:
        result = call_protected_skill(payload.message)
    except RuntimeError as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc

    return ChatResponse(result=result)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=GATEWAY_PORT)