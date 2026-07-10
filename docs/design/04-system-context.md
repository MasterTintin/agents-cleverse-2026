# 04 - System Context

# Overview

เอกสารนี้อธิบาย **System Context** ของ Private Skills Platform

จุดประสงค์ของเอกสารนี้คือการแสดงให้เห็นว่า

- ระบบของเราคืออะไร
- ระบบของเราอยู่ตรงไหน
- ใครเป็นผู้ใช้งานระบบ
- ระบบของเราสื่อสารกับระบบภายนอกอย่างไร

เอกสารนี้ **ยังไม่กล่าวถึงรายละเอียดภายในของระบบ**
เช่น Runtime, Database, API หรือ Deployment ซึ่งจะกล่าวถึงในเอกสารถัดไป

---

# System Vision

Private Skills Platform เป็นระบบที่ช่วยให้ Client
สามารถนำ **Private Skills** ไปใช้งานร่วมกับ
Large Language Models (LLMs)
ของตนเองได้

ตัวอย่างเช่น

- Claude
- ChatGPT
- Codex

โดยที่ Client สามารถเรียกใช้งาน Skill ได้
แต่ไม่สามารถเข้าถึงรายละเอียดภายในของ Skill เช่น

- Source Code
- Prompt
- Workflow
- Business Logic

---

# Stakeholders

| Stakeholder                 | Description                                        |
| --------------------------- | -------------------------------------------------- |
| **End User**                | ผู้ใช้งานที่ส่งคำสั่งผ่าน LLM                      |
| **Client**                  | องค์กรหรือผู้ใช้งานที่ต้องการใช้งาน Private Skills |
| **LLM Provider**            | ผู้ให้บริการ LLM เช่น Claude, ChatGPT หรือ Codex   |
| **Private Skills Platform** | ระบบที่รับคำขอและ Execute Private Skills           |
| **Skill Creator**           | ผู้พัฒนาและดูแล Private Skills                     |

---

# System Context Diagram

                    ┌──────────────────────┐
                    │      End User        │
                    └──────────┬───────────┘
                               │
                               │ Prompt
                               ▼
                 ┌────────────────────────────┐
                 │ Claude / ChatGPT / Codex   │
                 └──────────┬─────────────────┘
                            │
                            │ Execute Skill
                            ▼
          ╔══════════════════════════════════════╗
          ║      Private Skills Platform        ║
          ╚══════════════════════════════════════╝
                            │
                            │ Execute
                            ▼
                ┌────────────────────────┐
                │     Private Skills     │
                └────────────────────────┘

---

# Component Responsibilities

## End User

ผู้ใช้งานปลายทาง

หน้าที่

- ส่ง Prompt
- รับผลลัพธ์จาก LLM

---

## Claude / ChatGPT / Codex

Large Language Model (LLM)

หน้าที่

- วิเคราะห์ Prompt
- ตัดสินใจว่าควรเรียกใช้ Skill หรือไม่
- ส่งคำขอไปยัง Private Skills Platform
- สร้างคำตอบสุดท้ายให้ผู้ใช้

---

## Private Skills Platform

Platform ทำหน้าที่เป็นตัวกลางระหว่าง LLM และ Private Skills

หน้าที่หลัก ได้แก่

- รับคำขอ Execute Skill
- เรียกใช้งาน Private Skills
- ส่งผลลัพธ์กลับไปยัง LLM
- ปกป้องรายละเอียดภายในของ Skills

Platform ไม่มีหน้าที่เป็น LLM
แต่เป็นระบบที่ให้บริการ Private Skills

---

## Private Skills

Private Skills คือความสามารถเฉพาะด้าน
ที่ถูกพัฒนาโดย Skill Creator

ตัวอย่างเช่น

- OCR
- Invoice Processing
- Financial Analysis
- Knowledge Search

รายละเอียดการทำงานของ Skill
จะไม่ถูกเปิดเผยให้ Client เห็น

---

# Interaction Flow

ภาพรวมของการทำงานของระบบ

End User
↓
Claude / ChatGPT / Codex
↓
Private Skills Platform
↓
Private Skill
↓
Execution Result
↓
Claude / ChatGPT / Codex
↓
End User

Platform ทำหน้าที่เป็นตัวกลางในการ Execute Skills
โดยไม่เปิดเผยรายละเอียดภายในของ Skill

---

# System Boundary

ภายในขอบเขตของระบบ (In Scope)

- Private Skills Platform
- Private Skills

ภายนอกขอบเขตของระบบ (External Systems)

- End User
- Claude
- ChatGPT
- Codex

---

# Assumptions

เอกสารฉบับนี้จัดทำขึ้นจากข้อมูลที่มีในปัจจุบัน
และตั้งอยู่บนสมมติฐานดังต่อไปนี้

- Client มี LLM ของตนเอง
- LLM สามารถเรียกใช้งาน Platform ได้
- Private Skills ทำงานภายใน Platform
- Client ไม่สามารถเข้าถึง Implementation ของ Skill

สมมติฐานเหล่านี้อาจเปลี่ยนแปลงได้
เมื่อได้รับ Requirement เพิ่มเติมจากทีม

---

# Out of Scope

เอกสารนี้ยังไม่ครอบคลุมหัวข้อดังต่อไปนี้

- Internal Architecture
- Runtime Design
- API Design
- Authentication
- Authorization
- Database Design
- Deployment
- Marketplace
- Payment System

หัวข้อเหล่านี้จะกล่าวถึงในเอกสารถัดไป

---

# Summary

Private Skills Platform เป็นตัวกลางที่ช่วยให้
Client สามารถใช้งาน Private Skills
ผ่าน LLM ของตนเองได้

Platform มีหน้าที่รับคำขอ Execute Skills
และส่งผลลัพธ์กลับไปยัง LLM
โดยไม่เปิดเผยรายละเอียดภายในของ Skill

System Context นี้เป็นภาพรวมระดับสูง
เพื่อใช้เป็นพื้นฐานสำหรับการออกแบบ
Architecture ของระบบในลำดับถัดไป
