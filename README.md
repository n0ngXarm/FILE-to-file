# 📁 FILE-to-file

เครื่องมือแปลงไฟล์ความเร็วสูงและอเนกประสงค์สำหรับ Linux (GNOME Nautilus) ออกแบบมาให้ใช้งานง่ายเพียงแค่ **"คลิกขวาแล้วสั่งแปลงไฟล์ได้ทันที"** ทำงานแบบ Offline บนเครื่องของคุณ 100% ปลอดภัย ไม่ต้องอัปโหลดไฟล์ขึ้นระบบคลาวด์ภายนอก

---

## 🌟 ฟังก์ชันที่รองรับ (4 หมวดหมู่หลัก)

```text
📁 FILE-to-file (คลิกขวา -> Scripts)
 ├── 🎬 1_Video_and_Audio/
 ├── 🖼️ 2_Image/
 ├── 📄 3_PDF_and_Documents/
 └── 🎞️ 4_GIF/
```

### 1. 🎬 Video & Audio
* **Video to MP4**: แปลงวิดีโอทั่วไป (MKV, AVI, WebM, FLV) เป็น MP4 (H.264 + AAC)
* **Video to MP3**: แยกเสียงออกจากวิดีโอ บันทึกเป็นไฟล์ MP3 คุณภาพสูง
* **Audio to MP3**: แปลงไฟล์เสียง (WAV, FLAC, M4A, OGG) เป็น MP3
* **Audio to WAV**: แปลงไฟล์เสียงเป็น WAV คุณภาพเสียงไม่สูญเสีย (Lossless)
* **Audio to OGG**: แปลงไฟล์เสียงเป็น OGG Vorbis
* **MOV to MP4**: แปลงวิดีโอจากอุปกรณ์ Apple (MOV) เป็น MP4 มาตรฐาน

### 2. 🖼️ Image
* **Image to PNG**: แปลงภาพทุกฟอร์แมตเป็น PNG
* **Image to JPG**: แปลงภาพเป็น JPG พร้อมปรับแบ็กกราวด์สีขาวอัตโนมัติหากภาพต้นฉบับโปร่งใส
* **Image to WebP**: แปลงภาพเป็น WebP เพื่อประหยัดพื้นที่จัดเก็บและโหลดเร็วขึ้น
* **Image to ICO**: สร้างไฟล์ไอคอน (.ico) รองรับหลายขนาดพร้อมกัน (16x16 ถึง 256x256)
* **WEBP to PNG**: แปลงภาพ WebP ให้กลับเป็น PNG
* **JFIF to PNG**: แก้ปัญหาภาพนามสกุล JFIF ให้เป็น PNG ใช้งานได้ทุกที่
* **HEIC to JPG / PNG**: แปลงไฟล์รูปภาพจาก iPhone (HEIC) เป็น JPG หรือ PNG
* **SVG to PNG**: แปลงเวกเตอร์ SVG เป็นรูปภาพ PNG ความละเอียดสูง
* **PNG to SVG**: แปลงหรือบรรจุรูปภาพ PNG เข้าสู่ไฟล์เวกเตอร์ SVG

### 3. 📄 PDF & Documents
* **PDF to Word (DOCX)**: แปลงเอกสาร PDF เป็นไฟล์ Microsoft Word (.docx) ที่แก้ไขข้อความได้
* **PDF to Images (PNG / JPG)**: เรนเดอร์แยกทุกหน้าของ PDF ออกมาเป็นภาพ
* **Images to PDF**: รวมภาพนิ่งหลายๆ ภาพที่เลือกเข้าด้วยกันเป็นเอกสาร PDF เล่มเดียว
* **Office Doc to PDF**: แปลงไฟล์เอกสาร Word (DOCX), Excel (XLSX), PowerPoint (PPTX), ODT, TXT เป็น PDF
* **EPUB to PDF**: แปลงไฟล์หนังสือ E-book เป็นเอกสาร PDF
* **PDF to EPUB**: แปลงเอกสาร PDF เป็นไฟล์ E-book (EPUB)

### 4. 🎞️ GIF
* **Video to GIF**: แปลงวิดีโอ (MP4, WEBM, MOV, AVI) เป็นภาพเคลื่อนไหว GIF คุณภาพสูง (2-pass color palette)
* **GIF to MP4**: แปลงภาพ GIF ให้กลับมาเป็นวิดีโอ MP4 เพื่อลดขนาดไฟล์และเล่นได้ลื่นไหล
* **Images to Animated GIF**: เลือกภาพนิ่งหลายภาพมารวมกันเป็นภาพเคลื่อนไหว GIF
* **GIF to APNG**: แปลง GIF เป็น Animated PNG (APNG)
* **APNG to GIF**: แปลงภาพ Animated PNG เป็น GIF

---

## 🚀 วิธีติดตั้ง (Installation)

1. Clone repository หรือเปิดโฟลเดอร์โปรเจกต์:
   ```bash
   git clone https://github.com/n0ngXarm/FILE-to-file.git
   cd FILE-to-file
   ```

2. รันสคริปต์ติดตั้ง:
   ```bash
   ./install.sh
   ```

ระบบจะติดตั้งสคริปต์เข้าสู่ `~/.local/share/nautilus/scripts/FILE-to-file` ทันที

---

## 🖱️ วิธีใช้งาน (How to use)

1. เปิดตัวจัดการไฟล์ **Nautilus** (Files) บนเครื่องของคุณ
2. เลือกไฟล์ที่ต้องการแปลง (เลือก 1 ไฟล์ หรือเลือกหลายๆ ไฟล์พร้อมกันได้)
3. **คลิกขวา** $\rightarrow$ เลือก **Scripts** $\rightarrow$ **FILE-to-file** $\rightarrow$ เลือกหมวดหมู่และคำสั่งที่ต้องการ
4. ระบบจะแจ้งเตือน (Desktop Notification) ที่มุมจอว่ากำลังแปลง และแจ้งเตือนเมื่อแปลงสำเร็จ
5. ไฟล์ที่แปลงแล้วจะถูกบันทึกไว้ในโฟลเดอร์เดียวกันกับไฟล์ต้นฉบับทันที

---

## 💻 ใช้งานผ่าน Command Line (CLI)

คุณสามารถเรียกใช้งานสคริปต์ผ่าน Terminal ได้โดยตรงเช่นกัน:

```bash
# แปลงวิดีโอเป็น MP3
python3 -m core.video_audio to_mp3 video.mp4

# แปลงภาพเป็น WebP
python3 -m core.image_converter to_webp photo.png

# รวมรูปภาพหลายไฟล์เป็น PDF เล่มเดียว
python3 -m core.pdf_doc images_to_pdf page1.jpg page2.jpg page3.jpg

# แปลง PDF เป็น Word
python3 -m core.pdf_doc pdf_to_docx document.pdf

# แปลงวิดีโอเป็น GIF
python3 -m core.gif_converter video_to_gif clip.mp4
```

---

## 🧪 การทดสอบระบบ (Running Tests)

```bash
python3 -m unittest discover tests
```

---

## 🗑️ วิธีถอนการติดตั้ง (Uninstall)

```bash
./uninstall.sh
```

---

## 📄 License
MIT License
