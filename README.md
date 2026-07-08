# Learning OS Starter Kit 🧠

นี่คือโค้ดเริ่มต้นสำหรับสร้าง "ระบบเรียนรู้อัตโนมัติ" (Learning OS) บน GitHub ของคุณเอง พร้อมระบบส่งสรุปข่าวประจำวันไปที่ LINE กลุ่ม

## ฟีเจอร์หลัก
- 📰 **กวาดข่าว (Sweep):** ดึงข่าวจาก RSS feed อัตโนมัติ
- 🤖 **AI สรุปข่าว:** ใช้ Gemini AI สรุปข่าวเป็นภาษาไทย อ่านง่าย
- 🗄️ **คลังความรู้ (Vault):** บันทึกเป็นไฟล์ Markdown (`.md`) เข้า GitHub ของคุณ (ในโฟลเดอร์ `vault/inbox/`)
- ⏰ **อัตโนมัติ (Automated):** ทำงานทุกเช้าเวลา 07:00 น. (เวลาไทย) ด้วย GitHub Actions
- 📲 **แจ้งเตือน LINE:** ส่งข้อความเข้า LINE เมื่อทำงานเสร็จ

## วิธีติดตั้ง (Setup Guide)

### 1. นำโค้ดนี้ขึ้น GitHub ของคุณ
สร้าง Repository ใหม่ใน GitHub (ตั้งเป็น Private หรือ Public ก็ได้) แล้ว Push ไฟล์ทั้งหมดในโฟลเดอร์นี้ขึ้นไป

### 2. ตั้งค่า API Keys ใน GitHub Secrets
ไปที่ Repository ของคุณบน GitHub > **Settings** > **Secrets and variables** > **Actions** > สร้าง **New repository secret**:
* `GEMINI_API_KEY`: ใส่ API Key ของ Gemini (รับฟรีได้ที่ [Google AI Studio](https://aistudio.google.com/))
* `LINE_NOTIFY_TOKEN`: ใส่ Token ของ LINE Notify (ออก Token ได้ที่ [LINE Notify](https://notify-bot.line.me/my/))

### 3. (Optional) ตั้งค่าแหล่งข่าว
คุณสามารถเข้าไปแก้ไฟล์ `config.json` เพื่อเพิ่มหรือลดแหล่งข่าว RSS (เช่น ข่าวเทคโนโลยี, บล็อกของบริษัทที่คุณติดตาม) ได้ตามต้องการ

### 4. ทดสอบรันครั้งแรก
ไปที่แท็บ **Actions** บน GitHub ของคุณ > เลือก **Daily Learning OS Sweep** ด้านซ้ายมือ > กดปุ่ม **Run workflow**
*รอประมาณ 1-2 นาที คุณจะได้ไฟล์ Markdown ใหม่ในโฟลเดอร์ `vault/inbox/` และได้รับข้อความเตือนใน LINE!*

---
**💡 Tips:** คุณสามารถนำ Repository นี้ไปเชื่อมกับ Vercel หรือ Next.js เพื่อทำเป็นเว็บไซต์ได้เลย ไฟล์เนื้อหาจะอยู่ใน `vault/inbox/`
