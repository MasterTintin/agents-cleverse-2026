# Competitor Analysis: Capafy

**Skill-based Agent Marketplace**

---

## Capafy คืออะไร (สั้นๆ)

Capafy เป็น marketplace สำหรับ "Skill-based Agent" — ผู้เชี่ยวชาญแต่ละสาย pack workflow ของตัวเอง (ทำ resume, เขียน cold email, ตัดต่อวิดีโอ ฯลฯ) เป็น Skill แล้วเอามาขาย ผู้ใช้เรียก Skill นั้นมาใช้ผ่าน Claude Code, Codex หรือ OpenClaw ได้ทันที โดยไม่เห็นโค้ด/prompt เบื้องหลังเลย

---

## Capafy แก้ปัญหาอะไร

ปัญหาหลักที่ Capafy ระบุไว้ชัดคือ **"know-how ที่ควรค่าจะขาย แต่ไม่มีทางปกป้อง"**

- Generic AI ทำงานได้ "เฉลี่ย" เพราะออกแบบมาสำหรับทุกคน แต่ไม่มีความเชี่ยวชาญเฉพาะทางจริง
- คนที่มี know-how จริง (ครีเอเตอร์ที่ยอดวิวเป็นร้อยล้าน, recruiter ที่คัด resume มาเยอะมาก) มักไม่กล้าปล่อย Skill ที่ตัวเองสร้างออกสู่สาธารณะ เพราะระบบ open-source ecosystem เดิม (เช่น GitHub, marketplace อื่นๆ) ใครก็ fork/copy โค้ดไปได้ฟรี ทำให้ไม่มีทางได้ค่าตอบแทนหรือปกป้อง IP ของตัวเอง
- ผลคือ Skill ที่ดีที่สุดมักถูกเก็บไว้ใช้เองอย่างเดียว ไม่เคยถูกแชร์หรือ monetize

**ทางแก้ของ Capafy:** ให้ Skill รันแบบ **closed-source บนคลาวด์ของ Capafy เอง** — ผู้ใช้ได้แค่ "ผลลัพธ์" ไม่ได้เห็นไฟล์ โค้ด หรือ logic เบื้องหลัง ส่วนคนสร้างได้เงินทุกครั้งที่มีคนรัน โมเดลนี้จับคู่ปัญหา "อยากแชร์ความรู้" กับ "ไม่อยากเสีย IP" เข้าด้วยกันพอดี — ตรงกับสิ่งที่เจอใน research สัปดาห์ก่อน (Q3-Q9 เรื่อง IP protection)

---

## Publisher Workflow (ฝั่งคนขาย Skill)

ใช้ Skill ชื่อ `capafy-publisher ติดตั้งเข้า agent client แล้วทำงานผ่าน 4 คำสั่ง + 3 จุด checkpoint บนเว็บ:

1. **Log in** — ผูก token ไว้กับเครื่อง
2. **`publish-init`** — สแกน workspace หา Skill ที่ publish ได้ (โฟลเดอร์ที่มี `SKILL.md` + scripts + config) → **Web Checkpoint 1**: ยืนยันไฟล์ + เลือกโหมดขาย (Run Online / Download)
3. **`publish-configure`** — สแกนหา credentials/secrets ที่หลุดอยู่ในโค้ด (มีโหมด `--deep-scan` ให้สแกนละเอียดขึ้น) → ถ้าเลือก Run Online จะมี **Web Checkpoint 2**: map credential เข้ากับระบบของ Capafy
4. **`publish-ship`** — validate, แพ็กไฟล์, อัปโหลด → **Web Checkpoint 3**: ตรวจสอบครั้งสุดท้ายแล้วกด Submit

**จุดที่น่าสนใจ:** ระบบสแกน credentials อัตโนมัติก่อนเผยแพร่ทุกครั้ง (ป้องกันไม่ให้ publisher เผลอหลุด API key ของตัวเองไปด้วย) และการแยก "draft state" ออกจาก "Agent บน platform" ทำให้แก้ไข/ทำใหม่ระหว่างทางได้โดยไม่ต้องเริ่มนับหนึ่งใหม่

---

## User Workflow (ฝั่งคนใช้ Skill)

ใช้ Skill ชื่อ `capafy-user`:

1. **ค้นหา** — พิมพ์บอกสิ่งที่ต้องการ (เช่น "หา Agent ที่สรุป PDF ได้") ในแชทปกติ ระบบค้นจาก catalog ให้
2. **สั่งซื้อ** — เลือก Agent แล้วยืนยัน billing plan จ่ายด้วย credit (ในแชท) หรือบัตร (ผ่านลิงก์ Stripe)
3. **ติดตั้ง & ใช้งาน** — ถ้าเป็นโหมด Run Online จะติดตั้งแค่ **"Thin Skill"** (ตัว router เล็กๆ) ไว้ในเครื่อง เวลาผู้ใช้พิมพ์งานที่ตรงกับ Agent นั้น ระบบจะ route ไปรันที่ cloud ของ Capafy อัตโนมัติ ถ้าเป็นโหมด Download จะได้ไฟล์ Skill เต็มมารันเอง
4. **Resume/renew** — กลับมาใช้ instance เดิมได้ (ประหยัดกว่าสร้างใหม่ เพราะ instance เก่ามี context/history อยู่แล้ว), ต่ออายุ storage ก่อนถูกลบถาวร

**จุดที่น่าสนใจ:** แนวคิด "Thin Skill" คือสิ่งที่ทำให้ user experience ลื่นไหล — ผู้ใช้ไม่ต้องสลับไปเปิดเว็บทุกครั้ง เพียงคุยในแชทตามปกติ ระบบ route ให้เองว่าโจทย์นี้ควรส่งไปที่ Agent ไหน

---

## Business Model

| Sale Mode                     | ผู้ใช้จ่ายยังไง      | รันที่ไหน           | Source Code              |
| ----------------------------- | -------------------- | ------------------- | ------------------------ |
| **Run Online – Subscription** | รายเดือน/รายปี       | Cloud ของ Capafy    | ปิด (closed)             |
| **Run Online – Hourly**       | จ่ายตามชั่วโมงที่ใช้ | Cloud ของ Capafy    | ปิด (closed)             |
| **Download**                  | จ่ายครั้งเดียว       | เครื่องผู้ใช้เอง    | เปิด (ผู้ใช้ได้ไฟล์เต็ม) |
| **Free**                      | ไม่จ่าย              | ตามรูปแบบที่ตั้งไว้ | ตามโหมดนั้น              |

- รายได้หลักของ Capafy คือ **ส่วนแบ่งจากทุกธุรกรรม** (revenue share ระหว่าง creator กับ platform)
- Publisher เลือกราคาเองได้ ("set their own prices")
- โมเดล **"Run Online" คือหัวใจของธุรกิจ** เพราะเป็นโหมดเดียวที่ปกป้อง IP ได้จริง (โหมด Download คือทางเลือกสำหรับ Skill ที่ไม่ได้พึ่งความลับอะไรมาก)
- มีระบบ **Credit** (เติมเงินซื้อ credit ไว้ใช้ในแชทได้เลย ไม่ต้องออกไปกรอกบัตรทุกครั้ง) ควบคู่กับจ่ายผ่านบัตรตรงสำหรับเคสพิเศษ (renew, insufficient credits)

---

## สิ่งที่เราเรียนรู้

1. **"Thin client / Thin Skill" คือรูปแบบที่ทำให้ IP-protected marketplace ใช้งานได้ลื่น** — สิ่งที่อยู่บนเครื่องผู้ใช้มีแค่ตัว router บางๆ ส่วน logic จริงอยู่บน cloud ทั้งหมด ตรงกับแนวคิด "public interface vs private backend" ที่สรุปไว้ใน research สัปดาห์ที่แล้ว (Week 5) แบบเป๊ะๆ — Capafy คือ "ของจริง" ที่เอาแนวคิดนั้นไปทำเป็น product แล้ว
2. **Credential/secret scanning เป็นขั้นตอนบังคับก่อน publish** ไม่ใช่แค่ปกป้อง IP ของแพลตฟอร์ม แต่ปกป้อง publisher เองจากความผิดพลาดของตัวเอง (ลืมลบ API key ในโค้ด)
3. **Draft state แยกจาก platform state** ทำให้ workflow ที่มีหลาย manual checkpoint (ต้องเปิดเว็บ 3 รอบ) ไม่รู้สึกเปราะบาง — พังกลางทางแล้วกลับมาทำต่อได้โดยไม่ต้องเริ่มใหม่ เป็น UX pattern ที่ดีสำหรับ flow ที่มีขั้นตอนเยอะ
4. **Pricing ผูกกับ "usage shape" ไม่ใช่ผูกกับ Skill ทุกตัวเท่ากัน** — งานที่ปริมาณงานต่อ user จำกัด เหมาะกับ hourly, งานที่ใช้สม่ำเสมอเหมาะกับ subscription นี่คือมุมมองการตั้งราคาที่ AKL อาจเอามาคิดเผื่อถ้ามี tiering ในอนาคต
5. **Marketplace ecosystem นี้กำลังโตเร็ว** — บทความระบุว่ามี agent skill marketplace แบบเปิด (public/forkable) อยู่แล้วหลายเจ้า (Agensi, SkillsMP, ClawHub, skills.sh) แต่ Capafy เป็นเจ้าแรกๆ ที่โฟกัส "closed-source distribution" โดยเฉพาะ — แปลว่าตลาดกำลังแบ่งเป็น 2 ฝั่งชัดเจน: เปิด (community-driven) กับ ปิด (monetization-driven)

---

## Potential Design Implications

- **Skill-as-a-service pattern:** ถ้าในอนาคตมีแผนให้ทีมอื่น หรือแม้แต่หน่วยงานภายนอก "เสียบ" ความรู้เฉพาะทาง (เช่น skill สำหรับ legal review, HR screening) เข้ามาใน knowledge layer ได้ รูปแบบ **Thin Skill + Cloud execution** ของ Capafy เป็น pattern ที่ใช้อ้างอิงได้ตรง — เก็บ prompt/logic ไว้ที่ server ฝั่งเรา ส่งแค่ผลลัพธ์กลับไปให้ frontend/ผู้ใช้
- **Pre-publish credential scanning:** การสแกนหา secret/API key หลุดก่อน deploy เป็นแนวทางที่นำไปใช้กับ pipeline ทั่วไปได้เลย ไม่ว่าจะเกี่ยวกับ marketplace หรือไม่ — เช่นตั้ง pre-commit hook หรือ CI step ก่อน merge เข้า repo ใดๆ
- **Resumable multi-step flow:** แนวคิด "draft state แยกจาก platform state" เอาไปปรับใช้กับ flow ที่มีหลายขั้นตอนได้ เช่น อัปโหลดเอกสาร → chunk → embed ถ้า flow ไหนพังกลางทาง ควรออกแบบให้ resume ต่อจากจุดเดิมได้ ไม่ต้องเริ่ม pipeline ใหม่ทั้งหมด
- **Usage-based monetization model:** โมเดล subscription/hourly + credit system ของ Capafy เป็นตัวอย่างที่จับต้องได้ของการทำ monetization บน AI agent — เป็น reference point ที่ใช้เทียบเคียงได้เวลาต้องออกแบบ pricing tier ให้ระบบที่มี usage-based cost (เช่น token/compute)

---

## Architecture Hypothesis

โครงสร้างที่น่าจะอยู่เบื้องหลัง Capafy (อนุมานจาก workflow ที่สังเกตได้ ยังไม่ยืนยัน):

Capafy

Publisher
│
│ Upload
▼
Cloud Storage
│
▼
Execution Service
│
▼
Thin Skill
│
▼
User

---

## Open Questions

ประเด็นที่ยังไม่มีคำตอบชัดเจนจากข้อมูลสาธารณะ ต้อง research ต่อ:

- Thin Skill มีอะไรอยู่ข้างใน?
- Route อย่างไร?
- Auth ยังไง?
- ใช้ MCP หรือเปล่า?
- Cloud Execution เป็น Container หรือ LLM Session?
- Publisher Upload อะไรจริงๆ?
