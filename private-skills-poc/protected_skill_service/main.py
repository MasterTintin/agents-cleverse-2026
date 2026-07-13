"""
Protected Skill Service
========================
หัวใจของ POC: พิสูจน์ว่า Secret Logic (prompt/เกณฑ์การประเมินภายในองค์กร)
สามารถอยู่เบื้องหลัง service นี้ได้ โดยที่ input/output ที่ผ่าน API ไม่มี
วันมี prompt ลับหลุดออกไป

Skill นี้คือ "Internal Document Review Skill" — รับ "เอกสาร" แล้วประเมิน
ตามเกณฑ์ภายในองค์กร
"""

import os

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# TODO:
# Re-enable when switching from mock to Claude.
# from prompt import SECRET_SYSTEM_PROMPT

load_dotenv()

SKILL_PORT = int(os.getenv("SKILL_PORT", "8001"))

# TODO:
# Replace mock implementation with Anthropic client
# after architecture validation.

app = FastAPI(title="Protected Skill Service - Internal Document Review")


class ExecuteRequest(BaseModel):
    document: str


class ExecuteResponse(BaseModel):
    result: str


def run_skill(document: str) -> str:
    """
    Mock implementation for POC.

    In the production system this function will call
    Claude (or another execution engine).
    """

    return (
        "Overall Assessment: Suitable\n\n"
        "Reasons:\n"
        "- Relevant to the requested task\n"
        "- Well-structured\n"
        "- Sufficient information provided\n\n"
        "Suggestions:\n"
        "- Improve formatting\n"
        "- Add more project details"
    )


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/execute", response_model=ExecuteResponse)
def execute(payload: ExecuteRequest):
    """
    Endpoint บางๆ: validate เบื้องต้น -> เรียก run_skill -> ห่อเป็น response
    ไม่มี logic ของ Claude/prompt ปนอยู่ในนี้เลย
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