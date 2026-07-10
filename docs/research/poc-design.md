# POC Design: Protected Skill

**สิ่งที่ต้องทำก่อนเขียนโค้ด**

---

# Goal

พิสูจน์ว่า Protected Skill สามารถทำงานได้ โดยไม่เปิดเผย Implementation

---

# Scope

- 1 Skill (hardcode) — เลือกจาก `internal-document-review` หรือ `internal-score`
- Hardcode ทุกอย่าง — ไม่มี dynamic registry
- No Marketplace, No Permission UI, No Billing (เพิ่มทีหลังหลัง POC ผ่าน)

**Project Structure**

private-skills-poc/

frontend/
chat.html

gateway/
main.py

protected_skill/
main.py

docs/
poc-design.md

---

# Out of Scope

POC นี้ยังไม่ครอบคลุม

- Authentication
- Marketplace
- Skill Registry
- Database
- Billing
- Multiple Skills
- Deployment

---

# Architecture

User
│
▼
Chat Engine
│
▼
Skill Gateway
│
▼
Protected Skill Server
│
▼
Response

---

# Components

- **Chat Engine** — `frontend/chat.html` จำลอง user ถามคำถามผ่านหน้าแชทได้
- **Skill Gateway** — `gateway/main.py` รับ input จาก user, detect ว่าตรงกับ Protected Skill, ส่งต่อเฉพาะ input ที่จำเป็น
- **Protected Skill Service** — `protected_skill/main.py` เก็บ prompt/logic ลับไว้ รันแล้วส่งกลับเฉพาะผลลัพธ์

---

# Success Criteria

- ✅ User ใช้งานได้ (ถามคำถามธรรมดา ได้ผลลัพธ์กลับมา)
- ✅ Prompt ไม่รั่ว (response ที่ user เห็นไม่มี prompt/logic ลับปนอยู่เลย)
- ✅ Gateway route ถูกต้อง (ส่งไปหา Protected Skill Server ที่ถูกต้อง ไม่ใช่ hardcode ทางลัดใน frontend)

---

# Demo Scenario

1. User ถาม — เช่น "ช่วยประเมิน Resume นี้"
2. Gateway detect — จับได้ว่าคำถามนี้ต้องใช้ Protected Skill
3. Skill execute — Protected Skill Server ใช้ prompt ภายใน ("ใช้เกณฑ์ลับของบริษัท") ประมวลผล
4. Return result — Gateway ส่งเฉพาะผลลัพธ์กลับไปให้ user โดย user ไม่เคยเห็นข้อความ "ใช้เกณฑ์ลับของบริษัท" เลย
