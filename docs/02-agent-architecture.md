# Chapter 2 — Agent Architecture

> "An AI Agent is not a single model. It is a system composed of multiple components working together."

---

# 📖 บทนำ (Introduction)

ในบทก่อน เราได้เรียนรู้ว่า AI Agent คือระบบที่สามารถคิด วางแผน และลงมือทำงานเพื่อให้บรรลุเป้าหมาย

แต่คำถามที่สำคัญกว่านั้นคือ

> **AI Agent ภายในประกอบด้วยอะไรบ้าง?**

หลายคนเข้าใจว่า

User
↓
LLM
↓
Answer

คือ AI Agent

แต่ในความเป็นจริง
LLM เป็นเพียง "หนึ่งในหลายองค์ประกอบ" ของ Agent เท่านั้น
Agent ที่ใช้งานจริงประกอบด้วยระบบย่อยหลายส่วนที่ทำงานร่วมกัน เช่น Memory, Runtime, Planner และ Tools
การเข้าใจ Architecture เหล่านี้ จะทำให้เราเข้าใจ Framework ต่าง ๆ เช่น LangGraph, OpenAI Agents SDK หรือ MCP ได้ง่ายขึ้นในอนาคต

---

# Learning Objectives

หลังจากอ่านบทนี้ เราควรสามารถ

- อธิบายองค์ประกอบหลักของ AI Agent ได้
- เข้าใจหน้าที่ของแต่ละ Component
- เข้าใจข้อมูลไหลผ่านระบบอย่างไร
- มองเห็นภาพรวมของการทำงานทั้งระบบ

---

# 1. AI Agent คือ "ระบบ" ไม่ใช่ "โมเดล"

หลายคนคิดว่า

AI Agent = GPT

แต่จริง ๆ แล้ว

AI Agent ≠ LLM

LLM เป็นเพียงส่วนที่ใช้วิเคราะห์ภาษาและให้เหตุผล

Agent คือระบบทั้งหมด

                   AI Agent
                       │
      ┌────────────────┼────────────────┐
      │                │                │
     LLM            Memory          Runtime
      │                                 │
      └────────────────┬────────────────┘
                       │
                 Tool Manager
                       │
        ┌──────────────┼──────────────┐
        ▼              ▼              ▼
    File Tool      OCR Tool      Search Tool

---

# 2. High-Level Architecture

ภาพรวมของ Agent สามารถแบ่งออกเป็น 6 ส่วนหลัก

| Component | หน้าที่               |
| --------- | --------------------- |
| LLM       | วิเคราะห์และให้เหตุผล |
| Planner   | วางแผนการทำงาน        |
| Runtime   | ควบคุมลำดับการทำงาน   |
| Memory    | จดจำข้อมูล            |
| Tools     | ติดต่อระบบภายนอก      |
| Skills    | ความสามารถเฉพาะด้าน   |

ทุกส่วนทำงานร่วมกัน

ไม่มีส่วนใดทำงานเพียงลำพัง

---

# 3. LLM (Brain)

LLM เปรียบเสมือน "สมอง"

หน้าที่ของมันคือ

- เข้าใจภาษา
- วิเคราะห์คำถาม
- ให้เหตุผล
- สร้างข้อความ

LLM **ไม่สามารถ**

- เปิดไฟล์
- เขียนไฟล์
- เรียก Database
- ค้นหาเว็บ
- รัน Terminal

ด้วยตัวเอง

ดังนั้น

LLM จึงต้องทำงานร่วมกับส่วนอื่นของ Agent

---

# 4. Planner

Planner คือส่วนที่เปลี่ยน

"เป้าหมาย"

ให้กลายเป็น

"ลำดับขั้นตอน"

ตัวอย่าง

ผู้ใช้

> สรุป PDF ทั้งโฟลเดอร์ แล้วสร้าง Excel

Planner อาจแบ่งงานเป็น

ค้นหาไฟล์
↓
เปิดไฟล์
↓
อ่านข้อความ
↓
สรุป
↓
สร้าง Excel
↓
บันทึกไฟล์

Planner ไม่ได้ลงมือทำเอง

แต่เป็นผู้วางแผน

---

# 5. Runtime

Runtime คือหัวใจของระบบ

ถ้าเปรียบ Agent เป็นบริษัท

Runtime คือ "Project Manager"

หน้าที่ของ Runtime ได้แก่

- เรียกใช้ LLM
- เรียกใช้ Tool
- เก็บ State
- จัดการ Error
- Retry
- ควบคุมลำดับการทำงาน

Runtime ไม่ได้คิด

แต่เป็นคนประสานงาน

---

# 6. Memory

Memory ทำหน้าที่เก็บข้อมูล

ตัวอย่าง

ผู้ใช้

> ผมชื่อ Tintin

อีก 20 นาที

> ผมชื่ออะไร

Memory จะช่วยให้ Agent ตอบได้ว่า

> คุณชื่อ Tintin

Memory อาจเก็บ

- Conversation
- User Preference
- History
- Context

---

# 7. Tools

Tools คือความสามารถที่ทำให้ Agent ติดต่อโลกภายนอกได้

ตัวอย่าง

- File System
- Database
- Browser
- OCR
- REST API
- Email
- Calendar

LLM จะเป็นผู้ตัดสินใจ

ส่วน Tool เป็นผู้ลงมือทำ

---

# 8. Skills

Skill คือการรวม Tool หลายตัวเข้าด้วยกัน

ตัวอย่าง

Invoice Skill
↓
ค้นหาไฟล์
↓
OCR
↓
Extract Table
↓
Export Excel

Skill คือความสามารถเฉพาะทางของ Agent

ซึ่งมักถูกออกแบบให้สามารถนำกลับมาใช้ซ้ำได้

---

# 9. Data Flow

เมื่อผู้ใช้ส่งคำสั่งเข้ามา

ข้อมูลจะไหลผ่านระบบประมาณนี้

User
↓
Runtime
↓
LLM
↓
Planner
↓
Tool Manager
↓
Skills
↓
External Systems
↓
Result
↓
LLM
↓
Runtime
↓
User

นี่คือ Flow พื้นฐานของ Agent ส่วนใหญ่ในปัจจุบัน

---

# 10. End-to-End Example

ผู้ใช้

> ช่วยสรุปไฟล์ invoice.pdf

Agent จะทำงานดังนี้

Goal
↓
Planner
↓
Locate invoice.pdf
↓
File Tool
↓
OCR Tool
↓
LLM Summary
↓
Return Answer

ทุก Component มีหน้าที่ของตัวเอง

จึงทำให้ระบบสามารถทำงานที่ซับซ้อนได้

---

# Mental Model

> **LLM is the Brain. Runtime is the Manager. Tools are the Hands. Memory is the Experience. Planner is the Strategist.**

ถ้าขาดส่วนใดส่วนหนึ่ง

Agent จะทำงานได้ไม่สมบูรณ์

---

# Key Takeaways

หลังจากอ่านบทนี้ เราควรเข้าใจว่า

- AI Agent คือระบบที่ประกอบด้วยหลาย Component
- LLM ไม่ใช่ทั้งระบบ
- Runtime เป็นตัวควบคุมการทำงานทั้งหมด
- Planner ใช้วางแผน
- Memory ใช้จดจำข้อมูล
- Tools ใช้ลงมือทำ
- Skills คือความสามารถเฉพาะด้านที่สร้างจาก Tools

---

# Summary

Architecture คือหัวใจของการออกแบบ AI Agent
เมื่อเข้าใจว่าแต่ละ Component มีหน้าที่อะไร เราจะสามารถออกแบบระบบที่มีความยืดหยุ่น ขยายต่อได้ง่าย และบำรุงรักษาได้ในระยะยาว
ในบทถัดไป เราจะศึกษาการทำงานของ Agent อย่างละเอียด ตั้งแต่เริ่มรับคำสั่ง ไปจนถึงการตัดสินใจและจบงาน ผ่านสิ่งที่เรียกว่า **Agent Lifecycle**

---
