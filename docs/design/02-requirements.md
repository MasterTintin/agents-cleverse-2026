# Functional Requirements

## FR-001 — Execute Private Skills

ระบบต้องอนุญาตให้ Client สามารถเรียกใช้งาน Private Skills ได้ผ่าน Interface ที่กำหนด

โดย Client ไม่จำเป็นต้องทราบรายละเอียดการทำงานภายในของ Skill

## FR-002 — Support Multiple LLM Providers

ระบบต้องสามารถรองรับการทำงานร่วมกับ LLM หลายผู้ให้บริการ

ตัวอย่างเช่น

- Claude
- ChatGPT
- Codex

โดยไม่ผูกกับผู้ให้บริการรายใดรายหนึ่ง

## FR-003 — Protect Skill Implementation

ระบบต้องป้องกันไม่ให้ Client เข้าถึง

- Source Code
- Prompt
- Workflow
- Internal Logic

ของ Private Skills

## FR-004 — Accept Input

ระบบต้องสามารถรับ Input
ที่ส่งมาจาก Client

ตัวอย่าง

- Text
- JSON
- File

## FR-005 — Return Output

ระบบต้องส่งผลลัพธ์กลับไปยัง Client
ในรูปแบบที่สามารถนำไปใช้งานต่อได้

ตัวอย่าง

- JSON
- Markdown
- Text

## FR-006 — Execute Skills Securely

ทุกการเรียกใช้งาน Skill
ต้องผ่านกระบวนการตรวจสอบสิทธิ์
(Authentication และ Authorization)

---

# Non-Functional Requirements

## NFR-001 — Security

ระบบต้องป้องกันการเข้าถึง
Implementation ภายในของ Skill

## NFR-002 — Scalability

ระบบต้องสามารถรองรับ
การเพิ่มจำนวน Skills
และจำนวนผู้ใช้งาน
ได้ในอนาคต

## NFR-003 — Reliability

ระบบควรสามารถ
Execute Skills ได้อย่างต่อเนื่อง

## NFR-004 — Extensibility

ระบบควรสามารถเพิ่ม Skills ใหม่
โดยไม่ต้องแก้ไข Runtime หลัก

## NFR-005 — Compatibility

ระบบควรรองรับ
LLM หลายผู้ให้บริการ

---

# Constraints

ข้อจำกัดของ Phase ปัจจุบัน

- ยังไม่พัฒนา Marketplace
- ยังไม่พัฒนา Payment System
- มุ่งเน้นการ Execute Private Skills
- มุ่งเน้นการซ่อน Implementation

---

# Assumptions

- Client มี LLM ของตนเอง
- Client สามารถเชื่อมต่อกับระบบผ่าน API
- Skills ถูกพัฒนาโดย Skill Creator
- Runtime เป็นผู้ Execute Skills

---

# Open Questions

1.  Skill มีรูปแบบเป็นอะไร

- Python
- Workflow
- Prompt
- MCP Server

2.  Skill จะถูก Deploy อย่างไร

3.  Skill จะถูก Version อย่างไร

4.  Client เรียก Skill ผ่าน Protocol อะไร

5.  ระบบต้องรองรับ Streaming Response หรือไม่

6.  Skill สามารถเรียก Skill อื่นได้หรือไม่
