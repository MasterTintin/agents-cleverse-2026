"""
Skill Gateway
=============
ตัวกลางระหว่าง Frontend กับ Protected Skill Service

หน้าที่: รับ request จาก user, forward เฉพาะ input ที่จำเป็นไปยัง
Protected Skill Service, แล้วส่ง instructions กลับ — Gateway ไม่มีวันเห็น
หรือเก็บ prompt/business logic ลับไว้

Capability Discovery: GET /skills คืนรายการ Skill ทั้งหมดที่ระบบรู้จัก
แบ่งเป็น 2 กลุ่ม — Skill ที่มี service จริงรองรับ (status: available,
relay มาจาก Protected Skill Service ตรงๆ) และ Skill ที่ "วางโครงไว้"
แต่ยังไม่ implement (status: planned, hardcode เป็น stub ใน Gateway
เอง) การแยกแบบนี้ทำให้เห็นว่าระบบขยายเป็นหลาย Skill ได้โดยไม่ต้องรื้อ
API contract แต่ยังไม่ต้องสร้าง Skill Registry เต็มรูปแบบ (DB, admin
UI ฯลฯ) ตอนนี้

รายชื่อ skill ที่ "implement จริง" ไม่ hardcode เป็น set คงที่แล้ว —
ดึงจาก manifest ของ Protected Skill Service ตรงๆ ทุกครั้งที่ /chat ถูก
เรียก (ดู get_implemented_skill_ids) เพื่อให้ manifest.json เป็น single
source of truth จริงๆ แลกกับ network round-trip เพิ่มขึ้น 1 ครั้งต่อ
request — trade-off ที่ยอมรับได้สำหรับ POC

POST /chat รับ {"skill": "...", "input": {...}} — input เป็น dict อิสระ
ที่ Gateway ไม่ต้องรู้ shape ข้างในเลย (แต่ละ Skill ต้องการ input
ต่างกัน) Gateway แค่ forward payload.input ทั้งก้อนไปให้ Protected
Skill Service ตีความเอง
"""

import os
from typing import Literal

import httpx
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

load_dotenv()

GATEWAY_PORT = int(os.getenv("GATEWAY_PORT", "8000"))
SKILL_SERVICE_URL = os.getenv("SKILL_SERVICE_URL", "http://127.0.0.1:8001")
REQUEST_TIMEOUT_SECONDS = 30

# Public contract ที่ client ต้องเรียกจริง — ผ่าน Gateway เท่านั้น
PUBLIC_ENDPOINT = "/chat"
PUBLIC_METHOD = "POST"

# Skill ที่ "วางโครงไว้" ให้เห็นว่าระบบขยายได้ แต่ยังไม่มี service จริง
# หลังบ้าน — hardcode ไว้ใน Gateway ตรงๆ ยังไม่ใช่ Skill Registry เต็ม
# รูปแบบ
PLANNED_SKILLS = [
    {
        "id": "resume-review",
        "name": "Resume Review Skill",
        "version": "v1",
        "status": "planned",
        "provider": "Cleverse",
        "capabilities": ["resume-review"],
        "endpoint": PUBLIC_ENDPOINT,
        "method": PUBLIC_METHOD,
        "description": "Review resumes against internal hiring criteria.",
    },
    {
        "id": "grammar-check",
        "name": "Grammar Check Skill",
        "version": "v1",
        "status": "planned",
        "provider": "Cleverse",
        "capabilities": ["grammar-check"],
        "endpoint": PUBLIC_ENDPOINT,
        "method": PUBLIC_METHOD,
        "description": "Check grammar and style issues in documents.",
    },
    {
        "id": "pii-redaction",
        "name": "PII Redaction Skill",
        "version": "v1",
        "status": "planned",
        "provider": "Cleverse",
        "capabilities": ["pii-redaction"],
        "endpoint": PUBLIC_ENDPOINT,
        "method": PUBLIC_METHOD,
        "description": "Detect and redact PII from documents.",
    },
]

app = FastAPI(title="Skill Gateway")

# เปิด CORS แบบกว้างสำหรับ POC เท่านั้น
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class ChatRequest(BaseModel):
    skill: str = "document-edit"
    input: dict


class Instruction(BaseModel):
    old_str: str
    new_str: str
    reason: str
    priority: Literal["high", "medium", "low"]


class ChatResponse(BaseModel):
    instructions: list[Instruction]


def has_valid_input(input_data: dict) -> bool:
    """
    เช็คระดับ shape เท่านั้น (dict ต้องไม่ว่าง) — Gateway ไม่ตีความว่า
    ข้างในควรมี field อะไรบ้าง เพราะแต่ละ Skill ต้องการ input ต่างกัน
    การตรวจ field ที่จำเป็นจริงๆ เป็นหน้าที่ของ Protected Skill Service
    """
    return bool(input_data)


def get_implemented_skill_ids() -> set[str]:
    """
    ดึงรายชื่อ skill ที่ status == "available" จาก Protected Skill
    Service ตรงๆ แทนการ hardcode set คงที่แบบเดิม — ลด duplication
    ระหว่าง manifest.json (source of truth จริง) กับ Gateway

    หมายเหตุ: เรียก network request ทุกครั้งที่ /chat ถูกยิง ไม่มี cache
    เพื่อความถูกต้องเสมอ (ไม่มี stale state ให้กังวล) แลกกับ latency ที่
    เพิ่มขึ้นเล็กน้อย — trade-off ที่ยอมรับได้สำหรับ POC ขนาดนี้ ถ้า
    traffic สูงขึ้นค่อยเพิ่ม cache/TTL ทีหลัง
    """
    try:
        response = httpx.get(
            f"{SKILL_SERVICE_URL}/skills", timeout=REQUEST_TIMEOUT_SECONDS
        )
        response.raise_for_status()
    except httpx.HTTPStatusError as exc:
        raise RuntimeError(
            f"ดึงรายชื่อ skill ไม่สำเร็จ: {exc.response.status_code}"
        ) from exc
    except httpx.RequestError as exc:
        raise RuntimeError(f"เชื่อมต่อ Protected Skill Service ไม่ได้: {exc}") from exc

    return {s["id"] for s in response.json() if s.get("status") == "available"}


def invoke_skill(skill_id: str, input_data: dict) -> list[dict]:
    """
    เรียก Protected Skill Service แล้วคืนแค่ instructions

    รับ input_data เป็น dict อิสระแล้ว forward ทั้งก้อนไปเป็น JSON body
    ตรงๆ — Gateway ไม่ต้องรู้เลยว่า field ข้างในชื่ออะไรบ้าง (document?
    resume? invoice?) ปล่อยให้ Protected Skill Service ตีความเอง
    (Separation of Concerns) ไม่มีทางเห็น system prompt ที่ใช้ประมวลผล
    อยู่เบื้องหลังเลย — Gateway เห็นแค่ old_str/new_str/reason ที่
    Protected Skill ตัดสินใจส่งกลับมาแล้ว ไม่เห็นว่า Claude คิดยังไงถึง
    ได้คำตอบนี้

    หมายเหตุ: skill_id รับไว้เผื่ออนาคตต้อง route ไปหลาย service ตาม
    skill ที่ขอ (ตอนนี้ยังไม่มี Skill Registry จริง เลย forward ไปที่
    SKILL_SERVICE_URL เดียวเสมอ ไม่ว่า skill_id จะเป็นอะไร)
    """
    try:
        # Gateway forwards only user input.
        # Secret prompt remains inside Protected Skill Service.
        response = httpx.post(
            f"{SKILL_SERVICE_URL}/execute",
            json=input_data,
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


def to_public_manifest(skill: dict) -> dict:
    """
    เขียนทับ endpoint/method ของ manifest ที่ relay มาจาก Protected
    Skill Service ให้เป็น public contract จริง (ผ่าน Gateway) แทนที่
    endpoint ภายในของ service เอง (/execute) — Gateway เป็น trust
    boundary ที่รู้ว่า client ควรเห็นอะไร ไม่ใช่ปล่อยให้ internal
    implementation detail หลุดผ่าน manifest ไปตรงๆ
    """
    public_skill = dict(skill)
    public_skill["endpoint"] = PUBLIC_ENDPOINT
    public_skill["method"] = PUBLIC_METHOD
    return public_skill


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/skills")
def skills():
    """
    Capability discovery — คืนทั้ง Skill ที่ใช้งานได้จริง (relay จาก
    Protected Skill Service) และ Skill ที่วางโครงไว้ (PLANNED_SKILLS)
    รวมกันเป็น list เดียว แต่ละรายการมี "status" บอกชัดว่าอันไหนใช้ได้
    จริง อันไหนยังไม่มี service หลังบ้าน

    endpoint/method ของทุกรายการถูกเขียนทับเป็น public contract
    (ดู to_public_manifest) — ไม่มีทางเห็น /execute ที่เป็น endpoint
    ภายในของ Protected Skill Service เลย
    """
    try:
        response = httpx.get(
            f"{SKILL_SERVICE_URL}/skills", timeout=REQUEST_TIMEOUT_SECONDS
        )
        response.raise_for_status()
    except httpx.HTTPStatusError as exc:
        raise HTTPException(
            status_code=502,
            detail=f"Protected Skill Service ตอบกลับผิดพลาด: {exc.response.status_code}",
        ) from exc
    except httpx.RequestError as exc:
        raise HTTPException(
            status_code=502, detail=f"เชื่อมต่อ Protected Skill Service ไม่ได้: {exc}"
        ) from exc

    real_skills = [to_public_manifest(s) for s in response.json()]
    return real_skills + PLANNED_SKILLS


@app.post("/chat", response_model=ChatResponse)
def chat(payload: ChatRequest):
    """
    Endpoint ที่ frontend เรียก — ทำหน้าที่แค่ route + forward เท่านั้น
    ไม่มี business logic ของ skill ปนอยู่ในนี้เลย

    เช็ค payload.skill ก่อน forward เสมอ โดยดึงรายชื่อ skill ที่
    implement จริงมาจาก manifest สดๆ (ไม่ hardcode) — ถ้าเป็น skill ที่
    ยังไม่มี service จริงรองรับ (status: planned) ต้องตอบ 501 ชัดเจน
    ไม่ใช่พยายาม forward ไปที่ service ที่ไม่มีจริง
    """
    if not has_valid_input(payload.input):
        raise HTTPException(status_code=400, detail="input ต้องไม่ว่างเปล่า")

    try:
        implemented_ids = get_implemented_skill_ids()
    except RuntimeError as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc

    if payload.skill not in implemented_ids:
        raise HTTPException(
            status_code=501,
            detail=f"Skill '{payload.skill}' ยังไม่มี service รองรับ (status: planned)",
        )

    try:
        instructions = invoke_skill(payload.skill, payload.input)
    except RuntimeError as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc

    return ChatResponse(instructions=instructions)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=GATEWAY_PORT)