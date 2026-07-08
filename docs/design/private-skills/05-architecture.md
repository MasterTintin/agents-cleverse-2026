# 05 - Architecture v1

---

# Overview

เอกสารนี้นำเสนอ Architecture ระดับแนวคิด (Conceptual Architecture)
ของ Private Skills Platform

Architecture นี้มีจุดประสงค์เพื่ออธิบาย
ภาพรวมของระบบ
โดยยังไม่ลงรายละเอียดด้านเทคโนโลยี
หรือการติดตั้งระบบ

---

# Design Principles

Architecture ฉบับนี้ยึดหลักการดังต่อไปนี้

- แยกการใช้งาน Skill ออกจาก LLM
- ปกป้อง Implementation ของ Skill
- รองรับ LLM หลายผู้ให้บริการ
- สามารถเพิ่ม Skills ใหม่ได้ง่าย

---

# High-Level Architecture

                    Client
                       │
                       ▼
             Claude / ChatGPT / Codex
                       │
                       ▼
      ┌────────────────────────────────┐
      │   Private Skills Platform      │
      │                                │
      │  • Skill Interface             │
      │  • Skill Manager               │
      │  • Skill Executor              │
      └────────────────────────────────┘
                       │
                       ▼
             Private Skills Repository

---

# Components

## Skill Interface

จุดรับคำขอจาก Client

รับข้อมูลที่จำเป็นสำหรับการ Execute Skill

โดยไม่เปิดเผยรายละเอียดภายในของระบบ

---

## Skill Manager

รับผิดชอบการเลือก Skill
ที่เหมาะสมกับคำขอ

รวมถึงจัดการการเรียกใช้งาน Skill

---

## Skill Executor

ทำหน้าที่ Execute Private Skill
และรับผลลัพธ์กลับมา

Skill Executor ไม่จำเป็นต้องทราบว่า
Client ใช้ LLM ใด

---

## Private Skills Repository

พื้นที่เก็บ Private Skills

Platform เป็นผู้เข้าถึง Repository

Client ไม่สามารถเข้าถึงได้โดยตรง

---

# Architecture Flow

Client
↓
LLM
↓
Skill Interface
↓
Skill Manager
↓
Skill Executor
↓
Private Skill
↓
Result
↓
LLM
↓
Client

---

# Design Decisions

Architecture ฉบับนี้เลือกแยก

- Interface
- Skill Management
- Skill Execution

ออกจากกัน

เพื่อให้

- เพิ่ม Skills ใหม่ได้ง่าย
- เปลี่ยนวิธี Execute ได้
- รองรับ LLM หลายประเภท
- ลดการเชื่อมโยงกันของแต่ละ Component

---

# Future Extensions

Architecture นี้สามารถขยายต่อได้ในอนาคต

เช่น

- Authentication
- Authorization
- Logging
- Monitoring
- Versioning
- Marketplace

โดยไม่กระทบกับโครงสร้างหลักของระบบ

---

# Summary

Architecture v1
มุ่งเน้นการสร้าง Platform
ที่สามารถ Execute Private Skills
ผ่าน LLM หลายผู้ให้บริการ

โดยยังคงปกป้อง
Implementation ภายในของ Skill
และสามารถขยายระบบได้ในอนาคต
