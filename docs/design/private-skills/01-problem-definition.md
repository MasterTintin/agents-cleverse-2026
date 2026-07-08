# Private Skills Platform

## Background

ปัจจุบัน Large Language Models (LLMs) เช่น Claude, ChatGPT และ Codex
ถูกนำมาใช้งานอย่างแพร่หลาย ทั้งในงานด้านเอกสาร การวิเคราะห์ข้อมูล
และระบบอัตโนมัติ

หลายองค์กรเริ่มพัฒนา AI Skills ของตนเอง
เพื่อแก้ปัญหาเฉพาะด้าน เช่น

- OCR
- Invoice Processing
- Financial Analysis
- Internal Knowledge Search

อย่างไรก็ตาม Skills เหล่านี้ถือเป็นทรัพย์สินทางปัญญา (Intellectual Property)

เจ้าของ Skills ไม่ต้องการเปิดเผย

- Source Code
- Prompt
- Workflow
- Business Logic

ให้กับลูกค้าโดยตรง

ในขณะเดียวกัน ลูกค้าก็ยังต้องการนำ Skills เหล่านี้
ไปใช้งานร่วมกับ LLM ที่ตนเองเลือก
เช่น Claude, ChatGPT หรือ Codex

## Problem Statement

องค์กรต้องการระบบที่ช่วยให้ลูกค้าสามารถใช้งาน
Private AI Skills ผ่าน Large Language Models (LLMs)
ของตนเองได้

โดยระบบต้องสามารถ

- Execute Skills
- ปกป้อง Implementation ภายใน
- ไม่เปิดเผย Prompt หรือ Business Logic
- รองรับ LLM หลายผู้ให้บริการ
- ขยายระบบได้ในอนาคต

โจทย์สำคัญของระบบจึงไม่ใช่
"การสร้าง AI"

แต่เป็น

"การออกแบบ Platform ที่ทำให้ AI Skills สามารถถูกใช้งานได้อย่างปลอดภัย"

## Why is this problem challenging?

การออกแบบระบบนี้มีความท้าทายหลายด้าน

1.  Client ต้องสามารถใช้งาน Skill ได้
    แต่ต้องไม่เห็น Implementation ภายใน

2.  ระบบต้องรองรับ LLM หลายประเภท
    โดยไม่ผูกกับผู้ให้บริการรายใดรายหนึ่ง

3.  Skill อาจประกอบด้วยหลายขั้นตอน
    เช่น OCR → Data Extraction → Analysis

4.  ระบบต้องสามารถขยายจำนวน Skills
    ได้ในอนาคต

## Goals

ระบบควรสามารถ

- Execute Private Skills
- Protect Intellectual Property
- Support Multiple LLM Providers
- Scale for Future Marketplace
- Provide Secure Access

## Out of Scope

งานใน Phase นี้จะยังไม่รวม

- Skills Marketplace UI
- Payment System
- Billing
- Recommendation System
