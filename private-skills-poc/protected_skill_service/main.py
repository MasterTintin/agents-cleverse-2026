import os

from anthropic import Anthropic
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from prompt import SECRET_SYSTEM_PROMPT

load_dotenv()

SKILL_PORT = int(os.getenv("SKILL_PORT", "8001"))
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
MODEL_NAME = "claude-sonnet-4-6"
MAX_TOKENS = 500

app = FastAPI(title="Protected Skill Service")
client = Anthropic(api_key=ANTHROPIC_API_KEY) if ANTHROPIC_API_KEY else None

class ExecuteRequest(BaseModel):
    resume: str

class ExecuteResponse(BaseModel):
    result: str

def run_skill(resume: str) -> str:
    """
    Business logic: รับ resume text -> เรียก Claude ด้วย secret prompt
    -> คืนแค่ข้อความผลลัพธ์ (ไม่ผูกกับ FastAPI/HTTP เลย ทำให้ unit test ตรงๆ
    ได้โดยไม่ต้องยิง request ผ่าน endpoint)
    """
    if client is None:
        raise RuntimeError("ANTHROPIC_API_KEY ยังไม่ได้ตั้งค่า")

    try:
        message = client.messages.create(
            model=MODEL_NAME,
            max_tokens=MAX_TOKENS,
            system=SECRET_SYSTEM_PROMPT,
            messages=[{"role": "user", "content": resume}],
        )
    except Exception as exc:
        raise RuntimeError(f"เรียก Claude ไม่สำเร็จ: {exc}") from exc

    return "".join(block.text for block in message.content if block.type == "text")


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/execute", response_model=ExecuteResponse)
def execute(payload: ExecuteRequest):
    """
    Endpoint บางๆ: validate เบื้องต้น -> เรียก run_skill -> ห่อเป็น response
    ไม่มี logic ของ Claude/prompt ปนอยู่ในนี้เลย
    """
    if not payload.resume.strip():
        raise HTTPException(status_code=400, detail="resume ต้องไม่ว่างเปล่า")

    try:
        result = run_skill(payload.resume)
    except RuntimeError as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc

    return ExecuteResponse(result=result)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=SKILL_PORT)