# Skill Gateway

Proxy กลางระหว่าง Frontend กับ Protected Skill Service — รับ request
จาก user, forward เฉพาะ input ที่จำเป็นไปยัง Protected Skill Service,
แล้วส่ง `instructions` (edit instructions แบบ structured) กลับ

Gateway **ไม่มีทางเห็นหรือเก็บ prompt/business logic ลับเลย** จะอยู่ใน
อยู่ใน `protected_skill_service/prompt.py` เท่านั้น — Gateway เห็นแค่
`old_str`/`new_str`/`reason` ที่ Protected Skill ตัดสินใจส่งกลับมาแล้ว
ไม่เห็นว่า Claude คิดยังไงถึงได้คำตอบนี้ — ดูภาพรวมทั้งระบบที่
[`../README.md`]

---

## Role ในระบบ

```
User
   │
   ▼
Gateway   <── อยู่ตรงนี้
   │
   ▼
Protected Skill Service
   │
   ▼
OpenRouter → Claude
```

Gateway ทำหน้าที่แค่ **route + forward** เท่านั้น ไม่ตีความเนื้อหาของ
request ว่าเป็น resume, invoice หรือ document ประเภทไหน — การตีความ
ความหมายเป็นหน้าที่ของ Protected Skill Service เพียงผู้เดียว
(Separation of Concerns)

---

## Endpoints

| Method | Path      | Body                 | Response                                                    |
| ------ | --------- | -------------------- | ----------------------------------------------------------- |
| `GET`  | `/health` | -                    | `{"status": "ok"}`                                          |
| `POST` | `/chat`   | `{"message": "..."}` | `{"instructions": [{"old_str", "new_str", "reason"}, ...]}` |

`/chat` คือ endpoint เดียวที่ frontend เรียก — ข้างในจะ forward ไปยัง
`POST {SKILL_SERVICE_URL}/execute` ของ Protected Skill Service ต่อ

---

## Run

### 1. ติดตั้ง dependencies

```bash
cd gateway
pip install -r requirements.txt
```

### 2. ตั้งค่า environment variables

```bash
cp .env.example .env
```

| ตัวแปร              | ค่า default             | ใช้ทำอะไร                                        |
| ------------------- | ----------------------- | ------------------------------------------------ |
| `GATEWAY_PORT`      | `8000`                  | port ที่ gateway รัน                             |
| `SKILL_SERVICE_URL` | `http://127.0.0.1:8002` | URL ของ Protected Skill Service ที่จะ forward ไป |

### 3. รัน server

**ต้องรัน `protected_skill_service` ให้ขึ้นก่อน** (default ที่ port
`8002`) แล้วค่อยรัน gateway:

```bash
uvicorn main:app --reload --port 8000
```

Server จะขึ้นที่ `http://127.0.0.1:8000`

---

## Test

**Health check:**

```bash
curl http://127.0.0.1:8000/health
```

**เรียกผ่าน gateway (ต้องมี `protected_skill_service` รันอยู่ก่อน พร้อม
`OPENROUTER_API_KEY` จริงใน `.env` ของมัน):**

```bash
curl -X POST http://127.0.0.1:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "John is a software enginer. He have 3 years experiance."}'
```

ควรได้ `{"instructions": [...]}` กลับมา — response ไม่มีทางมี prompt
จาก `protected_skill_service/prompt.py` ปนออกมาเลย

| กรณี                                                                      | คาดว่าจะได้                                   |
| ------------------------------------------------------------------------- | --------------------------------------------- |
| `message` ว่าง                                                            | `400`                                         |
| `protected_skill_service` ยังไม่ได้รัน / ต่อไม่ติด                        | `502`                                         |
| `protected_skill_service` ตอบ error (เช่นไม่ได้ตั้ง `OPENROUTER_API_KEY`) | `502`                                         |
| เอกสารไม่มีจุดต้องแก้                                                     | `200` พร้อม `instructions: []`                |
| สำเร็จ                                                                    | `200` พร้อม `instructions` อย่างน้อย 1 รายการ |

---

## Out of Scope (ส่วน Gateway)

- **Skill Registry / หลาย Skill** — `is_protected_skill_request()` ตอนนี้
  hardcode ว่า route ทุก request ไปที่ Protected Skill เดียวเสมอ ยังไม่มี
  intent detection จริง (ดู Open Questions ที่
  `../docs/research/capafy-competitor-analysis.md`)
- **Authentication** — ยังไม่มีการตรวจสอบตัวตนของ user เลย
- **CORS จำกัด origin** — ตอนนี้เปิดกว้าง (`allow_origins=["*"]`) สำหรับ
  POC เท่านั้น ของจริงต้องจำกัดให้แคบกว่านี้
- **การเขียนไฟล์จริง** — Gateway/Frontend ยังไม่ apply instructions ลง
  ไฟล์บนดิสก์จริง (Phase 2 ใน `../docs/research/file-edit-approach.md`
  ทำแค่ apply กับ text ใน browser memory เท่านั้น)
