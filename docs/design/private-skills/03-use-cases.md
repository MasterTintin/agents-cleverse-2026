# 03 - Use Cases

## UC-001 Register Private Skill

Actor

- Skill Creator

Description

- Skill Creator ลงทะเบียน Private Skill เข้าสู่ระบบ

Preconditions

- Skill Creator ได้รับสิทธิ์ใช้งาน

Success

- Skill ถูกลงทะเบียนสำเร็จ

---

## UC-002 Execute Private Skill

Actor

- Client

Description

- Client เรียกใช้งาน Private Skill ผ่าน Platform

Preconditions

- Client มีสิทธิ์ใช้งาน
- Skill พร้อมใช้งาน

Success

- Client ได้ผลลัพธ์จาก Skill

---

## UC-003 Authenticate Client

Actor

- Client

Description

- ระบบตรวจสอบสิทธิ์ก่อน Execute Skill

Success

- อนุญาตหรือปฏิเสธการใช้งาน

---

## UC-004 Return Skill Result

Actor

- Platform

Description

- Platform ส่งผลลัพธ์กลับไปยัง Client

Success

- Client ได้ผลลัพธ์

---

## UC-005 Handle Skill Error

Actor

- Platform

Description

- ระบบจัดการเมื่อ Skill ทำงานผิดพลาด

Success

- Client ได้รับ Error Response

---

## UC-006 Support Multiple LLMs

Actor

- Platform

Description

- ระบบรองรับการเรียกใช้งานจาก Claude, ChatGPT และ Codex

Success

- Execute Skill ได้โดยไม่ขึ้นกับผู้ให้บริการ LLM
