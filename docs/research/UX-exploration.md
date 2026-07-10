# UX Exploration: How Users Trigger Skills in AKL

**Research| สำรวจ UX pattern สำหรับการเรียกใช้ Skill**

---

## บริบท

solution-proposal.md ตอบคำถามเรื่อง**สถาปัตยกรรม** (Skill รันที่ไหน ปกป้อง logic ยังไง) แต่ยังไม่ได้ตอบคำถามฝั่ง **UX**: user จะรู้ได้ยังไงว่ามี Skill ให้ใช้ และจะสั่งเรียกมันยังไง เอกสารนี้สำรวจ 4 ทางเลือกที่เป็นไปได้ ก่อนเลือกไปทำ POC ต่อ

---

## Option A — Automatic

User
│
▼
Chat
│
▼
Auto Detect
│
▼
Skill

User พิมพ์คำถามในแชทตามปกติ ระบบ (Query Rewriter) วิเคราะห์ intent แล้ว**ตัดสินใจเองทันที**ว่าควร route ไป Skill ตัวไหน โดยไม่ถามยืนยัน — Skill ทำงานแล้ว stream ผลลัพธ์กลับมาเนียนไปกับ conversation ปกติ

---

## Option B — Marketplace

User
│
▼
Browse
│
▼
Install
│
▼
Use

User เข้าหน้า "Skill Catalog" แยกต่างหาก (คล้าย Capafy) เลือกดู Skill ที่มี, กด "ติดตั้ง/เปิดใช้" ให้ตัวเองหรือทีมก่อน แล้วค่อยกลับมาเรียกใช้ในแชท — เป็น flow ที่ user รู้ตัวชัดเจนว่ากำลังเพิ่ม capability ใหม่

---

## Option C — Permission

User
│
▼
Ask
│
▼
Approve
│
▼
Execute

User พิมพ์คำขอในแชท ระบบ detect ว่าตรงกับ Skill ตัวไหน แต่**หยุดรอ confirm ก่อนรัน** ("จะเรียก Skill X เพื่อทำสิ่งนี้ ยืนยันไหม?") — คล้าย Option A แต่เพิ่ม checkpoint ก่อน execute

---

## Option D — Invisible

User
│
▼
Chat
│
▼
AI
│
▼
Choose Skill

User คุยกับ AI เหมือนเดิมทุกอย่าง โดย**ไม่รู้เลยด้วยซ้ำว่ามีสิ่งที่เรียกว่า "Skill" อยู่** — AI (ไม่ใช่ rule-based router แบบ Option A) เป็นคนตัดสินใจเลือก Skill เองระหว่างการ reasoning ปกติ เหมือน Skill เป็นแค่ "เครื่องมือในกล่องเครื่องมือ" ของ AI ไม่ใช่ feature ที่ user ต้อง aware

> **ข้อแตกต่างจาก Option A:** A คือ "ระบบ detect แล้วเรียก Skill แบบมี process ที่ observe ได้" (log ได้ชัดว่า detect ยังไง เรียกอะไร) ส่วน D คือ "AI ตัดสินใจเองในการ reasoning" ซึ่ง transparency ต่ำกว่าและ debug ยากกว่า แม้ user experience จะดูคล้ายกัน

---

## Comparison

|                | **A. Automatic**                                                                                                   | **B. Marketplace**                                                                           | **C. Permission**                                                                                               | **D. Invisible**                                                                                                            |
| -------------- | ------------------------------------------------------------------------------------------------------------------ | -------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------- |
| **UX**         | ลื่นไหลสุด ไม่ขัดจังหวะการคุย แต่ user อาจงงถ้า Skill ทำงานผิดจุด เพราะไม่รู้ตัวว่ามันถูกเรียก                     | ชัดเจน user คุมได้เต็มที่ว่าจะเปิด Skill ไหนใช้ แต่มี friction ต้องออกจากแชทไป browse ก่อน   | กลางๆ — user รู้สึกอุ่นใจว่าคุมได้ แต่ถ้า Skill ถูกเรียกบ่อย การ confirm ทุกครั้งจะเริ่มน่ารำคาญ                | ลื่นไหลสุดในทางทฤษฎี (ไม่มี UI แทรกเลย) แต่ถ้า AI เลือกผิด user จะงงมากกว่า A เพราะไม่มี log/step ให้ตรวจสอบย้อนหลังง่ายๆ   |
| **Latency**    | มี overhead จาก Query Rewriter ตรวจ intent ก่อน แต่เป็น step เดียว เร็วสุดในบรรดาที่ต้อง detect                    | ไม่มี latency เพิ่มตอนคุย (install เสร็จแล้วเรียกตรง) แต่มี upfront cost ตอน browse/install  | ช้าสุด เพราะมี round-trip รอ user ตอบ approve ก่อนถึงจะ execute ต่อ                                             | พอๆ กับ A หรืออาจช้ากว่าเล็กน้อย เพราะให้ AI ตัดสินใจกลางการ reasoning (ไม่ใช่ rule-based matching ที่เร็วกว่า)             |
| **Security**   | เสี่ยงสุด — ไม่มี human-in-the-loop เลย ถ้า Skill รันผิด (เช่นดันไปเรียก Skill ที่แก้ไขข้อมูล) ไม่มีจุดให้สกัดก่อน | ปลอดภัยระดับหนึ่ง เพราะ install เป็น explicit action ที่ track ได้ว่าใครเปิด Skill ไหนไว้    | ปลอดภัยสุด เพราะมี human approval ก่อน execute ทุกครั้ง เหมาะกับ Skill ที่มีผลกระทบสูง (write ข้อมูล, ส่งอีเมล) | เสี่ยงสุดในบรรดาทั้งหมด เพราะแม้แต่ _ทำไม_ ถึงเลือก Skill นี้ก็ debug ยาก ไม่มี explicit checkpoint ให้ตรวจสอบเลย           |
| **Complexity** | ปานกลาง — ต้องมี intent detection ที่แม่นยำพอสมควร (ผูกกับ Query Rewriter ที่มีอยู่แล้ว)                           | สูง — ต้องสร้าง catalog UI, install flow, state ว่าใคร install อะไรไว้ ทั้งหมดนี้เป็นของใหม่ | ปานกลาง-สูง — ต้องมี UI สำหรับ confirm/reject กลางแชท และจัดการ state ระหว่างรอ user ตอบ                        | ต่ำสุดในแง่ engineering (ไม่ต้องสร้าง UI ใหม่เลย) แต่สูงสุดในแง่ "ควบคุมพฤติกรรม AI ให้เลือกถูก" ซึ่งยากกว่า rule-based มาก |

---

## ข้อสังเกต

- **A กับ D ดูคล้ายกันจาก diagram แต่ต่างกันที่ "ใครตัดสินใจ"** — A ใช้ระบบที่ deterministic กว่า (matching/rule) ส่วน D ปล่อยให้ AI ตัดสินใจเอง ซึ่งกระทบ Security และ debuggability มากกว่าที่ diagram แสดงให้เห็น
- **ไม่จำเป็นต้องเลือกทางเดียวสำหรับทุก Skill** — สอดคล้องกับแนวคิด Two-Tier ใน `08-solution-proposal.md`: Skill ที่ผลกระทบต่ำ (อ่านอย่างเดียว, Tier 1) ใช้ Option A ได้สบาย ส่วน Skill ที่ผลกระทบสูงหรือเป็น Tier 2 (มี logic ลับ/แก้ไขข้อมูล) ควรบังคับผ่าน Option C เพื่อมี human-in-the-loop
- **Option B ไม่จำเป็นต้องขัดกับ A/C** — อาจใช้ B เป็นเลเยอร์ "เปิดสิทธิ์ระดับทีม/องค์กร" (admin เลือกว่า Skill ไหนเปิดให้ทีมไหนใช้ได้) แล้วให้ A หรือ C เป็นเลเยอร์ "เรียกใช้จริงระหว่างแชท" — คล้ายกับที่ Anthropic เองใช้ระดับ Org (เปิด Skill จากส่วนกลาง) ผสมกับระดับ user (auto-invoke ระหว่างคุย) ตามที่เจอใน Research ชุดแรก

---

## Unified Flow

                User

                  │

          Ask Question

                  │

         Query Rewriter

                  │

          Is Protected?

          ┌───────┴────────┐

          │                │

         No               Yes

          │                │

      Tier 1          Tier 2

(Open Skill) (Protected Skill)

          │                │

Automatic Ask Permission

          │                │

      Claude       Skill Gateway

          │                │

       Result     Execution Service

ภาพนี้รวม 2 การตัดสินใจที่เอกสารนี้และ `08-solution-proposal.md` คุยแยกกันไว้ ให้เห็นเป็นเส้นเดียว: **Tier (จาก Solution Proposal)** เป็นตัวกำหนดว่า Skill นั้นควรจับคู่กับ **UX Option ไหน (จากเอกสารนี้)** — Query Rewriter เป็นจุดตัดสินใจ (`Is Protected?`) ที่มีอยู่แล้วในสถาปัตยกรรมเดิม ทำให้ไม่ต้องสร้าง component ใหม่แค่เพื่อ route ระหว่าง Tier

---

## Recommendation (สำหรับ POC)

เป้าหมายของ POC ไม่ใช่การพิสูจน์ UX ทุกแบบ แต่เป็นการพิสูจน์ว่า Protected Skill สามารถทำงานร่วมกับ Chat Engine โดยไม่เปิดเผย Implementation ได้

ดังนั้น POC รอบแรกควรเลือก UX ที่เรียบง่ายที่สุด แต่ยังสะท้อนแนวคิด Two-Tier ได้ครบ

จากการเปรียบเทียบทั้งหมด POC รอบแรกควรใช้:

- **Tier 1 → Option A (Automatic)**
- **Tier 2 → Option C (Permission)**

เหตุผล:

- ใช้ประโยชน์จาก Query Rewriter ที่มีอยู่แล้ว
- เพิ่ม Human-in-the-loop สำหรับ Protected Skill
- ไม่ต้องสร้าง Marketplace เต็มรูปแบบ
- สามารถพิสูจน์ Architecture ได้เร็วที่สุด
