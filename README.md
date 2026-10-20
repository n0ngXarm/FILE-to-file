# 📁 FILE-to-file

<p align="center">
  <b>เครื่องมือแปลงไฟล์ความเร็วสูงและอเนกประสงค์สำหรับ Linux (GNOME Nautilus)</b><br>
  <i>Ultra-fast, local, offline file converter suite natively integrated into Linux GNOME Nautilus file manager.</i>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/License-MIT-blue.svg" alt="License: MIT">
  <img src="https://img.shields.io/badge/Python-3.9+-yellow.svg" alt="Python: 3.9+">
  <img src="https://img.shields.io/badge/Platform-Linux%20%2F%20GNOME-orange.svg" alt="Platform: Linux GNOME">
  <a href="https://ko-fi.com/n0ngXarm"><img src="https://img.shields.io/badge/Ko--fi-F16061?style=flat&logo=ko-fi&logoColor=white" alt="Ko-fi"></a>
  <a href="https://buymeacoffee.com/n0ngXarm"><img src="https://img.shields.io/badge/Buy_Me_A_Coffee-FFDD00?style=flat&logo=buy-me-a-coffee&logoColor=black" alt="Buy Me A Coffee"></a>
</p>

---

[ภาษาไทย](#ภาษาไทย) | [English](#english)

---

<a name="ภาษาไทย"></a>
## 🇹🇭 ภาษาไทย

**FILE-to-file** ออกแบบมาเพื่อให้ผู้ใช้งาน Linux สามารถแปลงไฟล์ทุกชนิดได้ง่ายเพียงแค่ **"คลิกขวาแล้วสั่งแปลงไฟล์ได้ทันที"** ในโปรแกรมจัดการไฟล์ (Nautilus) โดยทำงานแบบ **Offline 100%** บนเครื่องของคุณ ไม่มีการอัปโหลดไฟล์ส่วนตัวขึ้น Cloud ปลอดภัย รวดเร็ว และรองรับชื่อไฟล์ภาษาไทย

### 🌟 ฟังก์ชันเด่น
* **⚡ Smart Auto Convert (วิเคราะห์อัจฉริยะ)**: ตรวจจับเนื้อหาไฟล์จริง (MIME Type) แม้ไฟล์จะไม่มีนามสกุล พร้อมเปิดหน้าต่างแนะนำฟอร์แมตที่เหมาะสมให้เลือก
* **🛡️ ปลอดภัย ไม่เขียนทับไฟล์เดิม**: หากมีไฟล์ชื่อซ้ำ ระบบจะเติม `_1`, `_2` ต่อท้ายอัตโนมัติ ข้อมูลไม่มีทางสูญหาย
* **🎨 หน้าต่าง UI ทันสมัย**: ใช้ดีไซน์ **GNOME Libadwaita / GTK4** สวยงาม ขนาดใหญ่ ชัดเจน รองรับทั้ง Dark Mode และ Light Mode
* **🔔 แจ้งเตือนผ่านระบบ**: มี Desktop Notification แจ้งเตือนเมื่อกำลังแปลงและเมื่อเสร็จสิ้น

---

### 📂 หมวดหมู่ที่รองรับ

```text
📁 FILE-to-file (คลิกขวา -> Scripts)
 ├── ⚡ Smart Auto Convert (วิเคราะห์และแปลงอัตโนมัติ)
 ├── 🎬 1_Video_and_Audio/
 ├── 🖼️ 2_Image/
 ├── 📄 3_PDF_and_Documents/
 └── 🎞️ 4_GIF/
```

1. **🎬 Video & Audio**: แปลงวิดีโอ (MP4, MKV, AVI, MOV), ดูดเสียงเป็น MP3, แปลงเสียง Lossless WAV, OGG, MOV to MP4
2. **🖼️ Image**: แปลง PNG, JPG, WebP, ICO, JFIF to PNG, ภาพถ่าย iPhone (HEIC to JPG/PNG), เวกเตอร์ SVG $\leftrightarrow$ PNG
3. **📄 PDF & Documents**: แปลง PDF เป็น Word (.docx) แก้ไขได้, PDF เป็นรูปภาพ, รวมรูปภาพหลายไฟล์เป็น PDF, แปลง Word/Office/Text เป็น PDF, E-book EPUB
4. **🎞️ GIF**: แปลงคลิปวิดีโอเป็นภาพเคลื่อนไหว GIF คมชัดสูง, แปลง GIF กลับเป็นวิดีโอ MP4, รวมภาพนิ่งเป็น GIF, APNG

---

### 🚀 วิธีติดตั้ง (Quick Install)

เปิด Terminal แล้วคัดลอกคำสั่งด้านล่างไปวางเพื่อติดตั้งได้ทันที:

```bash
git clone https://github.com/n0ngXarm/FILE-to-file.git
cd FILE-to-file
./install.sh
```

*(ระบบจะตรวจสอบ dependencies และติดตั้งเมนูคลิกขวาให้ทันที)*

#### คำสั่งติดตั้ง Dependencies ของแต่ละ Distro:
* **Fedora / RHEL:** `sudo dnf install -y ffmpeg poppler-utils libreoffice zenity libnotify`
* **Ubuntu / Debian / Mint:** `sudo apt update && sudo apt install -y ffmpeg poppler-utils libreoffice zenity libnotify-bin`
* **Arch Linux:** `sudo pacman -S --needed ffmpeg poppler libreoffice-fresh zenity libnotify`

---

### 🖱️ วิธีใช้งาน
1. เปิด **Files (Nautilus)**
2. คลิกขวาที่ไฟล์ที่ต้องการ (เลือกไฟล์เดียวหรือหลายไฟล์พร้อมกันก็ได้)
3. เลือก **Scripts** $\rightarrow$ **FILE-to-file** $\rightarrow$ เลือกคำสั่งที่ต้องการ
4. ไฟล์ผลลัพธ์จะถูกสร้างขึ้นในโฟลเดอร์เดียวกันทันที!

---

<a name="english"></a>
## 🇬🇧 English

**FILE-to-file** is an open-source, offline file converter tool tailored for Linux GNOME Nautilus desktop environment. Convert videos, audio, images, PDFs, and documents natively from your right-click context menu.

### 🌟 Key Features
* **⚡ Smart Auto Convert**: Deep MIME inspection detects the actual file type and pops up a modern Libadwaita dialog offering the most sensible target formats.
* **🛡️ Collision-Safe**: Never overwrites existing files; auto-appends `_1`, `_2` cleanly.
* **🔒 100% Offline & Private**: All conversions execute locally on your machine with no third-party cloud uploads.
* **🎨 Modern GNOME UI**: Powered by Libadwaita/GTK4 with adaptive dark/light mode and comfortable typography.

### 🚀 Installation
```bash
git clone https://github.com/n0ngXarm/FILE-to-file.git
cd FILE-to-file
./install.sh
```

---

## ☕ การสนับสนุน / Donation & Sponsorship
โปรเจกต์นี้เปิดให้ทุกคนใช้งานได้ **ฟรี 100% (Free & Open Source)** ภายใต้สัญญาอนุญาต MIT  
หากเครื่องมือนี้ช่วยให้คุณประหยัดเวลาและทำงานสะดวกขึ้น สามารถร่วมสนับสนุนผู้พัฒนาได้ผ่านช่องทางด้านล่างนี้ครับ:

### 🇹🇭 พร้อมเพย์ (PromptPay QR) - สำหรับคนไทย
สแกนผ่านแอปธนาคารไทยได้ทุกธนาคาร เงินเข้าบัญชีผู้พัฒนาโดยตรง (0% ค่าธรรมเนียม):

<p align="left">
  <img src="assets/promptpay.jpeg" alt="PromptPay QR Code" width="240">
</p>

---

### 🌐 สำหรับต่างชาติ (International Supporters)
<p align="left">
  <a href="https://ko-fi.com/n0ngXarm">
    <img src="https://ko-fi.com/img/githubbutton_sm.svg" alt="ko-fi" height="36">
  </a>
  &nbsp;&nbsp;
  <a href="https://buymeacoffee.com/n0ngXarm">
    <img src="https://img.buymeacoffee.com/button-api/?text=Buy me a coffee&emoji=☕&slug=n0ngXarm&button_colour=FFDD00&font_colour=000000&font_family=Cookie&outline_colour=000000&coffee_colour=ffffff" height="36" alt="Buy Me A Coffee" />
  </a>
</p>

* **Ko-fi:** [ko-fi.com/n0ngXarm](https://ko-fi.com/n0ngXarm)
* **Buy Me a Coffee:** [buymeacoffee.com/n0ngXarm](https://buymeacoffee.com/n0ngXarm)
* **GitHub Sponsor:** กดปุ่ม **Sponsor** 💖 ที่ด้านบนของ Repository ได้เลยครับ

---

## 📄 License
This project is licensed under the [MIT License](LICENSE).
