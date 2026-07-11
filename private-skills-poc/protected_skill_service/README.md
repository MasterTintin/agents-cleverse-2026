# Private Skills POC

พิสูจน์ว่า Protected Skill (business logic ที่เป็นความลับ เช่น prompt,
เกณฑ์ประเมิน) สามารถทำงานให้ user ใช้งานได้ **โดยไม่เปิดเผย
implementation**

ดูรายละเอียดการออกแบบได้ที่

- `docs/poc-design.md`
- `docs/research/solution-proposal.md`
- `docs/research/UX-exploration.md`

---

## Architecture

```
User
   │
   ▼
Gateway
   │
   ▼
Protected Skill Service
   │
   ▼
Claude
```

Business logic และ system prompt ถูกเก็บไว้ใน Protected Skill Service
เท่านั้น

---

## Current Status

| ส่วน                                         | สถานะ       |
| -------------------------------------------- | ----------- |
| `protected_skill/` — Protected Skill Service | ✅ ทำแล้ว   |
| `gateway/` — Skill Gateway                   | ❌ ยังไม่ทำ |
| `frontend/` — Chat UI                        | ❌ ยังไม่ทำ |

ตอนนี้ทดสอบได้แค่ยิง request ตรงเข้า `protected_skill` service ผ่าน
`curl`/Postman/`/docs` (Swagger UI ของ FastAPI) — ยังไม่มี Gateway
หรือหน้าแชทให้ใช้งานผ่าน UI

---

## Project Structure

```
private-skills-poc/
│
├── frontend/                  # ❌ ยังไม่ทำ
│   └── chat.html
│
├── gateway/                   # ❌ ยังไม่ทำ
│   └── main.py
│
├── protected_skill/           # ✅ ทำแล้ว
│   ├── main.py                # FastAPI app — endpoint /execute, /health
│   ├── prompt.py              # Secret system prompt
│   ├── requirements.txt
│   └── .env.example
│
└── README.md
```

---

## Run

### 1. ติดตั้ง dependencies

```bash
cd protected_skill
pip install -r requirements.txt
```

### 2. ตั้งค่า environment variables

```bash
cp .env.example .env
```

แล้วแก้ `.env` ใส่ `ANTHROPIC_API_KEY` ของจริง (`SKILL_PORT` ปล่อยเป็น
`8001` ตาม default ได้เลยถ้าไม่ชนกับ service อื่นในเครื่อง)

### 3. รัน server

```bash
uvicorn main:app --reload --port 8001
```

Server จะขึ้นที่ `http://127.0.0.1:8001`

---

## Test

**Health check:**

```bash
curl http://127.0.0.1:8001/health
```

**เรียก Skill จริง:**

```bash
curl -X POST http://127.0.0.1:8001/execute \
  -H "Content-Type: application/json" \
  -d '{"document": "ตัวอย่างเอกสารที่จะให้ Skill ประเมิน..."}'
```

ควรได้ผลลัพธ์กลับมาเป็น `{"result": "..."}` เท่านั้น

The response should contain only the evaluation result. Internal
business logic and system prompt remain inside Protected Skill Service
and are never returned to clients.

หรือเปิด Swagger UI ที่ `http://127.0.0.1:8001/docs` เพื่อลองยิง request
ผ่านหน้าเว็บแทน `curl` ก็ได้

---

## Success Criteria

- [ ] `/health` ตอบ `200 OK`
- [ ] `/execute` ด้วย `document` ว่าง → ตอบ `400`
- [ ] `/execute` ด้วย `document` ปกติ → ตอบ `200` พร้อม `result`
- [ ] Response ไม่มีข้อความจาก `prompt.py` ปนออกมาแม้แต่คำเดียว (รวมถึง
      กรณี error/500 ด้วย)

---

## Out of Scope (ของทั้งโปรเจกต์)

- Authentication
- Marketplace
- Skill Registry
- Database
- Billing
- Multiple Skills
- Deployment
