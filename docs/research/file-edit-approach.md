# File Edit Approach: Server-side vs Instruction-based

---

## Problem

**Requirement:** Client ควรใช้ Skill ได้ โดยไม่เห็น Implementation และต้องรองรับการแก้ไฟล์หลายรอบ (Multi-turn) ได้อย่างมีประสิทธิภาพ

POC ปัจจุบัน (`private-skills-poc`) ให้ Protected Skill **review** เอกสารแล้วคืนข้อความผลลัพธ์เท่านั้น ยังไม่เคย **แก้ไฟล์จริง** ให้ user

ถ้า Protected Skill ต้องขยับไปทำงานแบบ "แก้ไฟล์ให้" (เช่น แก้โค้ด, แก้เอกสาร) มี 2 แนวทางที่ต่างกันโดยพื้นฐาน:

1. **Server แก้ไฟล์เอง** แล้วส่งไฟล์ฉบับเต็มที่แก้แล้วกลับมา
2. **Instruction-based** — Server ส่งกลับแค่ "คำสั่งแก้ไข" แล้วให้ Client เป็นคน apply กับไฟล์จริงในเครื่อง

เอกสารนี้เปรียบเทียบทั้ง 2 แนวทาง เพื่อตัดสินใจว่าจะทำ prototype แบบไหนต่อ

---

## Approach A: Server แก้ไฟล์

```
Client → Frontend → Gateway → Protected Skill (ได้ไฟล์เต็ม)
   → Claude regenerate เนื้อหาทั้งไฟล์
   → Protected Skill ส่งไฟล์ฉบับแก้แล้วกลับมาทั้งไฟล์
   → Client save ทับ
```

**ข้อดี**

- ง่ายสุดฝั่ง Client — รับไฟล์มา save ทับตรงๆ ไม่ต้องมี logic เพิ่ม
- Claude คุมผลลัพธ์เต็มที่ ลด edge case เรื่อง merge/conflict
- เหมาะกับงาน generate ใหม่ทั้งไฟล์ (ไม่ใช่แก้ต่อจากของเดิม)

**ข้อเสีย**

| มิติ       | ปัญหา                                                                                                                                |
| ---------- | ------------------------------------------------------------------------------------------------------------------------------------ |
| Bandwidth  | ต้อง round-trip ไฟล์เต็มทุกรอบ แม้แก้แค่บรรทัดเดียว — แพงทั้ง network และ token (Claude ต้อง regenerate ทั้งไฟล์อยู่ใน context)      |
| Multi-turn | แก้ต่อรอบถัดไปต้อง re-upload เวอร์ชันล่าสุดใหม่ทุกครั้ง เสี่ยง state mismatch ถ้า client แก้ไฟล์เพิ่มระหว่างรอ                       |
| UX         | รอนานเพราะต้อง regenerate ทั้งไฟล์, ไม่เห็น diff ว่าเปลี่ยนตรงไหน (ต้อง compare เอง), เสี่ยง Claude hallucinate ไปแก้ส่วนที่ไม่ได้ขอ |

---

## Approach B: Instruction-based

```
Client → Frontend → Gateway → Protected Skill (ได้ไฟล์/context)
   → Claude วิเคราะห์ แล้วส่งกลับเป็น "คำสั่งแก้ไข" (structured)
   → Gateway → Client/Agent เป็นคน apply คำสั่งกับไฟล์จริงในเครื่อง
```

**UX ดีขึ้นชัดเจน:**

- เห็น diff ก่อน apply จริง — เข้ากับ **Option C (Permission)** ใน `10-ux-exploration.md` พอดี (approve ทีละจุดได้)
- payload กลับมาเล็กกว่ามาก เร็วขึ้นเพราะ Claude ไม่ต้อง regenerate ทั้งไฟล์

**ลดการส่งไฟล์ซ้ำได้ไหม?** ได้ — ถ้า client เก็บ state ไฟล์ไว้เอง (ควรเป็นแบบนั้นอยู่แล้ว) รอบถัดไปส่งแค่ diff/context ที่จำเป็น ไม่ต้อง re-upload ทั้งไฟล์

**เหมาะกับ MCP/Claude Code ยังไง?** ตรงเป๊ะ — นี่คือ pattern เดียวกับที่ Claude Code ใช้จริง (`str_replace`, `create_file`) Claude (server-side) ตัดสินใจ "จะแก้อะไร" แต่ execution จริงเกิดที่ local ผ่าน tool call ตรงกับโมเดล MCP ที่ server ส่ง intent กลับมาให้ client execute ไม่ใช่ server เขียนไฟล์เอง

**ข้อเสีย / สิ่งที่ต้องคิดเพิ่ม**

- Client ต้องมี logic apply instruction เอง (parse + replace) — ซับซ้อนขึ้นฝั่ง client
- ถ้า instruction อ้าง state ผิด (เช่น text ที่จะ replace ไม่ unique หรือถูกแก้ไปแล้วโดยคนอื่น) จะ apply ไม่ได้ ต้องมี validation
- ต้องเลือก instruction format (unified diff? JSON patch? หรือแบบง่ายสุด `{old_str, new_str}` เหมือน `str_replace` tool)

---

## Comparison

| มิติ                    | A: Server แก้ไฟล์         | B: Instruction-based                  |
| ----------------------- | ------------------------- | ------------------------------------- |
| Bandwidth               | สูง (round-trip ทั้งไฟล์) | ต่ำ (ส่งแค่ instruction)              |
| Multi-turn              | ยาก เสี่ยง state mismatch | ทำได้ดีกว่า ถ้า client เก็บ state เอง |
| UX                      | ไม่เห็น diff, รอนาน       | เห็น diff, approve ทีละจุดได้         |
| ความซับซ้อนฝั่ง Client  | ต่ำ                       | สูงกว่า (ต้อง apply instruction เอง)  |
| เข้ากับ MCP/Claude Code | ไม่ตรง pattern            | ตรง pattern เป๊ะ                      |

---

## Recommendation

เลือก **Instruction-based (Approach B)** เป็นทิศทางหลัก เพราะตอบโจทย์ 2 เรื่องที่วางไว้ตั้งแต่ `08-solution-proposal.md`:

1. สอดคล้องกับโมเดล Skill Gateway ที่ทำหน้าที่ "route + forward" อยู่แล้ว — ขยายเป็น "route + forward + relay instruction" เป็นธรรมชาติ ไม่ต้องรื้อ architecture
2. ตรงกับทิศทาง MCP/Claude Code integration ที่เป็นเป้าหมายระยะยาวของ Cleverse

ไม่แนะนำให้ทำ prototype คู่ขนานทั้ง 2 แบบ เพราะ Approach A ไม่ตอบโจทย์ MCP/Claude Code ตั้งแต่ต้น การทำ prototype คู่ขนานจะเสียเวลาโดยไม่ได้ข้อมูลใหม่ที่ช่วยตัดสินใจเพิ่ม

**Why not A?**
Although Approach A is simpler to implement, it does not align well with the long-term direction of MCP-style execution and introduces unnecessary bandwidth and UX limitations.

---

## Architecture Sketch

```
Client
   │  ส่งไฟล์ + คำขอ
   ▼
Frontend (chat.html)
   │
   ▼
Gateway
   │  forward เฉพาะ input
   ▼
Protected Skill Service
   │  Claude วิเคราะห์ -> คืน instruction (ไม่ใช่ไฟล์เต็ม)
   ▼
Gateway
   │  relay instruction กลับ (ไม่แตะเนื้อหา)
   ▼
Frontend
   │  แสดง diff ให้ user เห็นก่อน
   ▼
Client apply เอง (เขียนไฟล์จริง)
```

จุดที่ต่างจาก POC เดิมชัดเจนที่สุด: **ผลลัพธ์ที่ Protected Skill คืนกลับมาเปลี่ยนจาก "ข้อความอิสระ" เป็น "structured instruction"** — Gateway/Frontend ไม่ต้องแก้อะไรมากในระดับ role (ยังคง forward-only) แต่ต้อง handle response shape ใหม่

---

## Assumptions

- Client สามารถ execute instruction ได้
- Client ถือ local file ได้
- Protected Skill ไม่มีสิทธิ์แตะ local file โดยตรง
- Gateway ไม่เก็บ business logic

---

## Open Questions

- Instruction format ควรเป็นอะไร — `{old_str, new_str}` แบบง่าย (เหมือน `str_replace`) หรือ unified diff format?
- ถ้า `old_str` ไม่ unique ในไฟล์ (ตรงกันหลายจุด) จะจัดการยังไง — ให้ Claude ต้องระบุ context เพิ่มเสมอ หรือ reject แล้วขอใหม่?
- Frontend จะแสดง diff ยังไงให้ user เห็นก่อน apply (ต้องมี diff viewer component ใหม่)
- ถ้า apply แล้ว fail (state ไม่ตรง) จะแจ้ง error กลับไปให้ Claude retry ยังไง

---

## Next Step

1. เลือก instruction format ที่ง่ายที่สุดก่อน (`{old_str, new_str}`) ไม่ต้องทำ diff parser เต็มรูปแบบตั้งแต่แรก
2. ทำ prototype เล็กๆ ต่อยอดจาก `protected_skill_service` เดิม — เปลี่ยน endpoint ให้คืน `{instructions: [...]}` แทน `{result: "..."}`
3. ทำ Frontend แสดง diff ง่ายๆ (ไม่ต้องสวย) แล้วมีปุ่ม apply/reject ทีละ instruction
4. ทดสอบ multi-turn จริง — แก้ไฟล์ 2 รอบต่อเนื่อง ดูว่า state ไม่ mismatch
