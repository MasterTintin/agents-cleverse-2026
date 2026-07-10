# Solution Proposal: Skill Execution Architecture for AKL

**WHAT — synthesize จาก Research (WHY) + Competitor Analysis (HOW)**

---

## Problem

AKL กำลังขยายจาก RAG-based knowledge assistant ไปสู่ระบบที่รองรับ **Agent Skills** — ความสามารถเฉพาะทางที่ทีมต่างๆ (หรือในอนาคตอาจรวมถึงหน่วยงานภายนอก) แพ็กเป็น workflow แล้วให้ Chat Engine เรียกใช้ได้

ปัญหาคือ AKL ยังไม่มีคำตอบชัดเจนสำหรับคำถามพื้นฐาน 3 ข้อ:

1. **Skill logic ควรรันที่ไหน** — ใน Claude session ตรงๆ, บน server ของเราเอง, หรือในเครื่อง user?
2. **จะปกป้องอะไรบ้าง** — บาง Skill อาจมี business logic ที่เป็นความลับ (เช่น scoring rule ภายใน, prompt ที่ tune มาเฉพาะ) ซึ่งไม่ควรหลุดไปอยู่ในสิ่งที่ระบบส่งให้ Claude อ่านตรงๆ
3. **จะต่อกับสถาปัตยกรรมเดิม (RAG pipeline, Chat Engine, SSE streaming) ยังไงโดยไม่ต้องรื้อของเดิม**

ถ้าไม่ตอบคำถามนี้ก่อน การเพิ่ม Skill ใหม่แต่ละตัวจะกลายเป็นการตัดสินใจเฉพาะหน้า ไม่มี pattern ที่ทำซ้ำได้

---

## Requirements

| #   | Requirement                                                                                    | เหตุผล                                                                                                         |
| --- | ---------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------- |
| R1  | Skill logic ที่เป็นความลับต้องไม่ถูกส่งเป็น plain text ให้ Claude อ่านตรงๆ                     | ตาม Research (Week 5) — Claude อ่านได้แค่ plain text ดังนั้นการซ่อนต้องทำที่ระดับสถาปัตยกรรม ไม่ใช่การเข้ารหัส |
| R2  | User/ทีมที่เรียก Skill ต้องได้ "ผลลัพธ์" โดยไม่จำเป็นต้องเห็น prompt หรือ logic เบื้องหลัง     | ป้องกัน IP รั่วผ่านการอ่าน response โดยตรง                                                                     |
| R3  | ต้องเชื่อมกับ Chat Engine (SSE streaming) เดิมได้ โดยไม่กระทบ flow การ query RAG ปกติ          | ลด engineering cost และความเสี่ยงต่อระบบที่ใช้งานอยู่แล้ว                                                      |
| R4  | รองรับ Skill ที่ "ไม่ลับ" ให้รันแบบเบา (ไม่ต้อง round-trip ไป backend เพิ่ม) ได้ด้วย           | ไม่ใช่ทุก Skill จำเป็นต้องมี overhead ของการปกป้อง IP                                                          |
| R5  | Flow การเพิ่ม Skill ใหม่ ต้องมีขั้นตอนตรวจสอบก่อน deploy (อย่างน้อยคือ secret/credential scan) | ป้องกันความผิดพลาดจากคนเขียน Skill เอง                                                                         |

---

## Research Findings

- Claude เป็นโมเดลภาษา ต้องอ่าน instruction เป็น semantic text ถึงจะเข้าใจและปรับใช้แบบ dynamic ได้ — **เข้ารหัสไฟล์ตรงๆ ใช้ไม่ได้** เพราะ Claude อ่านไม่ออก และถ้าส่ง key ไปด้วยก็ดักจับได้อยู่ดี
- ทางแก้ที่ใช้กันจริงคือ **แยกสถาปัตยกรรม**: เปิดเผยแค่ "หน้าตา + คำอธิบาย" (public interface) ส่วน logic จริงเก็บไว้หลังบ้าน
- มี 3 ทางเลือกสำหรับ "ใครควรรัน Skill": Claude Server (ยืดหยุ่นสุด แต่ต้องเปิด logic), Provider's own server (ปลอดภัยสุด แต่ยืดหยุ่นน้อยลง), Local client (เร็วสุด แต่ logic ที่ส่งลงเครื่องอ่านออกได้)

---

## Competitor Insights

- Capafy พิสูจน์แล้วว่า pattern **"Thin client ในเครื่อง user + logic จริงรันบน cloud ของผู้ให้บริการ"** ใช้งานได้จริงในระดับ product ไม่ใช่แค่ทฤษฎี
- มีขั้นตอน **credential scanning ก่อน publish** เป็นด่านบังคับ ไม่ใช่ทางเลือก
- แยก **draft state ออกจาก published state** ทำให้ flow การเพิ่ม Skill ที่มีหลายขั้นตอน resume ได้เวลาพังกลางทาง
- Pricing/execution mode ผูกกับลักษณะ Skill (subscription vs hourly vs download) — บอกเป็นนัยว่า **ไม่ใช่ทุก Skill ต้องใช้ execution mode เดียวกัน**

---

## Proposed Solution

เสนอโมเดล **"Two-Tier Skill Execution"** สำหรับ AKL — แบ่ง Skill ออกเป็น 2 ระดับตามความอ่อนไหวของ logic แทนที่จะบังคับทุก Skill ใช้ pattern เดียวกัน:

### Tier 1 — Open Skill

Skill ที่ไม่มี business logic ลับ (เช่น format converter, general summarizer) → เขียนเป็น instruction ใน Prompt Builder ตรงๆ ให้ Claude เห็นเต็ม รันใน session ปกติ ไม่ต้อง round-trip เพิ่ม

### Tier 2 — Protected Skill

Skill ที่มี logic ลับ (เช่น internal scoring rule, prompt ที่ tune เฉพาะทีม) → ใช้ pattern แบบ Capafy:

User query (ผ่าน Chat Engine เดิม)
│
▼
Query Rewriter → ตรวจว่า intent ตรงกับ Protected Skill ตัวไหนหรือไม่
│
▼ (ถ้าตรง)
Skill Gateway (ใหม่ — เป็น service เล็กๆ ต่อจาก Chat Engine)
│ ส่งเฉพาะ input ที่จำเป็น ไม่ส่ง prompt ทั้งชุด
▼
Skill Execution Service (server ฝั่งเรา, เก็บ prompt/logic ลับไว้)
│ รันจบ ส่งกลับเฉพาะผลลัพธ์
▼
Chat Engine → stream กลับไปหา user ผ่าน SSE เดิม

**หลักการ:** Skill Gateway ทำหน้าที่เหมือน "Thin Skill" ของ Capafy คือ Claude เห็นแค่ว่า "มี capability นี้อยู่ ใช้งานยังไง" ส่วน logic จริงไม่เคยถูกส่งเข้าไปใน context ของ Claude เลย — execution เกิดที่ server ของเราเท่านั้น

**Registry:** ทุก Skill (ทั้ง Tier 1 และ 2) ลงทะเบียนในตาราง skills (Supabase) พร้อม metadata: tier, description (public), owner, และ — สำหรับ Tier 2 — endpoint ของ Execution Service กับผลจาก credential scan ล่าสุด

---

## Trade-offs

| ประเด็น                | Two-Tier ตามที่เสนอ                                                                                                                                | ทางเลือกอื่นที่พิจารณาแล้วไม่เลือก                                                                                                  |
| ---------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------- |
| Latency                | Tier 2 มี round-trip เพิ่ม 1 ครั้ง (Gateway → Execution Service) ก่อน stream กลับ                                                                  | รันทุกอย่างใน Claude session เดียว (เร็วกว่า) แต่ไม่ปกป้อง logic ลับได้เลย ตัดทิ้งเพราะขัด R1                                       |
| Engineering cost       | ต้องสร้าง Skill Gateway + Execution Service เพิ่ม แต่ Tier 1 (ส่วนใหญ่ในช่วงแรก) ไม่ต้องแตะอะไรเลย                                                 | บังคับทุก Skill เป็น Protected ตั้งแต่แรก (ปลอดภัยสุด) แต่ over-engineer สำหรับ Skill ที่ไม่มีอะไรต้องซ่อน ตัดทิ้งเพราะขัด R4       |
| ความยืดหยุ่นของ Claude | Tier 2 ทำให้ Claude ปรับ output แบบ dynamic ได้น้อยลง เพราะ logic ถูกล็อกไว้ที่ server (เหมือนข้อเสียของโมเดล "Provider's own server" ใน Research) | ให้ Claude Server รันทุกอย่างรวมถึง logic ลับ (ยืดหยุ่นสุด) ตัดทิ้งเพราะขัด R1 โดยตรง                                               |
| ความซับซ้อนของระบบ     | เพิ่ม service ใหม่ 1-2 ตัว ต้องดูแล deployment/monitoring เพิ่ม                                                                                    | ไม่ต้องมี service ใหม่ ถ้ายอมรับความเสี่ยงเรื่อง logic รั่ว — ประเมินแล้วว่าความเสี่ยงสูงเกินไปสำหรับ Skill ที่มี proprietary logic |

**ข้อจำกัดที่ยังไม่ตอบในเอกสารนี้:** วิธี auth ระหว่าง Skill Gateway ↔ Execution Service, รูปแบบ execution ของ Execution Service (persistent service vs on-demand container), และวิธี route แบบ real-time โดยไม่เพิ่ม latency ให้ Query Rewriter มากเกินไป — ต้องตอบให้ชัดตอนทำ POC

---

## Next Step

1. **POC ขนาดเล็ก:** เลือก Skill สมมติ 1 ตัวที่มี logic ที่อยาก "ซ่อน" (เช่น internal scoring) มาสร้าง Tier 2 flow แบบง่ายที่สุด (Skill Gateway + Execution Service แบบ hardcode ก่อน ไม่ต้องมี registry เต็มรูปแบบ) เพื่อวัด latency จริงที่เพิ่มขึ้น
2. **ตอบ Open Questions จาก competitor analysis ที่เกี่ยวข้องโดยตรงกับ POC นี้** โดยเฉพาะ "Cloud Execution เป็น container หรือ persistent service" และ "route อย่างไร" เพราะสองข้อนี้กระทบการออกแบบ Execution Service โดยตรง
3. **เอาผลจาก POC ไป validate กับพี่แปล๊งซ์** ว่า pattern นี้ต่อกับ backend (FastAPI, Conversation Service) ที่ทำอยู่ได้จริงโดยไม่ต้องรื้อโครงสร้างเดิม
4. ถ้า POC ผ่าน → เขียน spec ของ `skills` table + Skill Gateway API contract เป็นเอกสารแยก ก่อนเข้าสู่ Implementation
