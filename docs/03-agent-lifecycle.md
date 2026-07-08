# Chapter 3 — Agent Lifecycle

> "An AI Agent is not a one-time response generator. It is a system that continuously thinks, plans, acts, and learns until its goal is achieved."

---

# บทนำ (Introduction)

ในบทที่ผ่านมา เราได้เรียนรู้ว่า AI Agent ประกอบด้วยหลายองค์ประกอบ เช่น LLM, Planner, Runtime, Memory และ Tools

แต่การรู้ว่า "มีอะไรอยู่ในระบบ" ยังไม่เพียงพอ

สิ่งที่สำคัญกว่าคือ

> **องค์ประกอบเหล่านี้ทำงานร่วมกันอย่างไร?**

คำตอบของคำถามนี้เรียกว่า **Agent Lifecycle**

Lifecycle คือ "วงจรการทำงาน" ของ Agent ตั้งแต่ผู้ใช้ส่งคำสั่งเข้ามา จนกระทั่ง Agent ส่งผลลัพธ์กลับออกไป

ความเข้าใจเรื่อง Lifecycle จะเป็นพื้นฐานสำคัญของหัวข้อ Runtime, Tool Calling และ Private Skills ในบทต่อ ๆ ไป

---

# Learning Objectives

หลังจากอ่านบทนี้ เราควรสามารถ

- อธิบายวงจรการทำงานของ AI Agent ได้
- เข้าใจว่าแต่ละ Component ทำงานในขั้นตอนไหน
- เข้าใจว่าทำไม Agent ต้องทำงานเป็น Loop
- มองเห็นภาพการทำงานตั้งแต่ต้นจนจบ

---

# 1. Lifecycle คืออะไร?

Lifecycle คือ

> ลำดับขั้นตอนทั้งหมดที่ Agent ใช้ในการทำงานเพื่อให้บรรลุเป้าหมาย

ต่างจากโปรแกรมทั่วไปที่ทำงานเพียงครั้งเดียว

Agent จะทำงานเป็น "วงจร"

Goal
↓
Think
↓
Plan
↓
Act
↓
Observe
↓
Goal สำเร็จหรือยัง?
├── ยัง → ทำต่อ
└── สำเร็จ → จบ

วงจรนี้เรียกว่า

**Agent Loop**

---

# 2. ขั้นตอนที่ 1 — Receive Goal

ทุกอย่างเริ่มจาก

"เป้าหมาย"

ตัวอย่าง

ผู้ใช้

> ช่วยสรุปไฟล์ report.pdf

หรือ

> ส่งอีเมลหาหัวหน้าพร้อมแนบรายงาน

สิ่งสำคัญคือ

Agent ไม่ได้คิดแค่ "จะตอบอะไร"

แต่มันคิดว่า

> "ต้องทำอะไร"

---

# 3. ขั้นตอนที่ 2 — Reason

เมื่อได้รับ Goal

LLM จะเริ่มวิเคราะห์

ตัวอย่าง

Goal
↓
ผู้ใช้ต้องการสรุป PDF
↓
ต้องหาไฟล์ก่อน

Reasoning คือการคิด
ไม่ใช่การลงมือทำ

---

# 4. ขั้นตอนที่ 3 — Planning

เมื่อรู้ว่าต้องทำอะไร

Planner จะสร้างลำดับงาน

ตัวอย่าง

ค้นหาไฟล์
↓
เปิดไฟล์
↓
อ่านข้อความ
↓
สรุป
↓
ส่งคำตอบ

Goal ใหญ่
จะถูกแบ่งเป็น
หลาย Goal ย่อย

---

# 5. ขั้นตอนที่ 4 — Tool Selection

เมื่อรู้ขั้นตอนแล้ว
Agent จะเลือก Tool

ตัวอย่าง

ค้นหาไฟล์
↓
File Tool
อ่านข้อความจากภาพ
↓
OCR Tool
ค้นหาข้อมูลบนเว็บ
↓
Search Tool
LLM ไม่ได้ทำเอง

แต่เป็นผู้เลือกว่าจะใช้ Tool ไหน

---

# 6. ขั้นตอนที่ 5 — Execute

Runtime จะเรียก Tool

ตัวอย่าง

File Tool
↓
เปิด report.pdf
↓
อ่านข้อความ
หรือ
Database Tool
↓
SELECT ...
↓
Result

ขั้นตอนนี้คือ
"การลงมือทำ"

---

# 7. ขั้นตอนที่ 6 — Observe

หลังจาก Tool ทำงานเสร็จ
Agent จะตรวจสอบผล

ตัวอย่าง

เปิดไฟล์สำเร็จ
↓
อ่านข้อความต่อ
หรือ
ไม่พบไฟล์
↓
ลองค้นหาใหม่

Agent ไม่ได้เชื่อผลลัพธ์ทันที
แต่มันตรวจสอบก่อนเสมอ

---

# 8. ขั้นตอนที่ 7 — Decide

หลังจาก Observe

Agent ต้องตัดสินใจ
Goal สำเร็จหรือยัง?

ถ้ายัง
กลับไป
Planning
หรือ
Tool Selection
อีกครั้ง

นี่คือเหตุผลที่ Agent ทำงานเป็น Loop

---

# 9. ขั้นตอนที่ 8 — Finish

เมื่อ Goal สำเร็จ

Runtime จะ

- สรุปผล
- บันทึก Memory
- ส่งคำตอบกลับผู้ใช้

จึงถือว่าภารกิจเสร็จสมบูรณ์

---

# 10. Agent Loop

ภาพรวมของ Lifecycle

Receive Goal
↓
Reason
↓
Plan
↓
Choose Tool
↓
Execute
↓
Observe
↓
Goal Completed?
├── No
│
└──────────────┐
│
▼
Plan Again

Yes
↓
Finish

นี่คือรูปแบบการทำงานของ AI Agent ส่วนใหญ่

---

# 11. ตัวอย่างการทำงานจริง

ผู้ใช้

> ช่วยสรุป invoice.pdf

Agent จะทำงาน

Goal
↓
Reason
↓
Locate invoice.pdf
↓
File Tool
↓
OCR
↓
LLM Summary
↓
Return Answer

อีกตัวอย่าง

ผู้ใช้

> ส่ง Email พร้อมแนบไฟล์ report.pdf

Agent

Goal
↓
Locate report.pdf
↓
Email Tool
↓
Attach File
↓
Send Email
↓
Success

จะเห็นว่า
Agent ไม่ได้มีเพียงการ "ตอบ"
แต่มีการ "ลงมือทำ"

---

# 12. ทำไม Agent ต้องเป็น Loop?

ถ้า Agent ทำงานเพียงครั้งเดียว

เมื่อเกิด Error

ระบบจะล้มเหลวทันที

แต่เมื่อ Agent ทำงานเป็น Loop

มันสามารถ

- Retry
- เปลี่ยนแผน
- เลือก Tool ใหม่
- ทดลองอีกครั้ง

จนกว่าจะสำเร็จ

นี่คือเหตุผลที่ Agent มีความยืดหยุ่นมากกว่าโปรแกรมทั่วไป

---

# Key Takeaways

หลังจากอ่านบทนี้ เราควรเข้าใจว่า

- Agent ทำงานเป็นวงจร (Loop)
- Agent ไม่ได้ตอบทันที แต่คิดก่อน
- Runtime เป็นผู้ควบคุมวงจรทั้งหมด
- Planner ใช้วางแผน
- Tool ใช้ลงมือทำ
- Observation ใช้ตรวจสอบผลลัพธ์
- หาก Goal ยังไม่สำเร็จ Agent จะทำงานต่อ

---

# Summary

AI Agent ไม่ใช่ระบบที่ทำงานเพียงครั้งเดียวแล้วจบ

แต่เป็นระบบที่สามารถ

- คิด
- วางแผน
- ลงมือทำ
- ตรวจสอบผลลัพธ์
- ปรับแผน

วนซ้ำไปเรื่อย ๆ จนกว่าจะบรรลุเป้าหมาย

การเข้าใจ Lifecycle จะช่วยให้เราเข้าใจการออกแบบ Runtime, Tool Calling และ Agent Framework ต่าง ๆ ได้ง่ายขึ้น

---

# Cleverse Connection

หัวข้อนี้เชื่อมโยงกับงานในโปรเจกต์โดยตรง

- **Runtime/Harness** → ควบคุม Agent Loop ทั้งหมด
- **Tooling/Skills** → ขั้นตอน Choose Tool และ Execute
- **State/Database** → ใช้เก็บสถานะและข้อมูลระหว่างการทำงาน
- **Private Skills** → เป็นความสามารถเฉพาะที่ Agent เรียกใช้ในขั้น Execute

เมื่อเข้าใจ Lifecycle แล้ว เราจะเห็นภาพว่าทุกหัวข้อในโปรเจกต์ไม่ได้แยกจากกัน แต่เป็นส่วนหนึ่งของวงจรการทำงานเดียวกัน

---
