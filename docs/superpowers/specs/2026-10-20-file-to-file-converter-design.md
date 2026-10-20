# Design Specification: FILE-to-file Converter

## 1. Overview
`FILE-to-file` is a modular, high-performance file conversion suite integrated natively into the GNOME Nautilus file manager on Linux (via Nautilus Scripts), as well as accessible as a standalone CLI.

It provides 4 distinct converter categories inspired by popular web converter suites:
1. **Video & Audio**
2. **Image**
3. **PDF & Documents**
4. **GIF**

All conversions run locally, offline, and securely without uploading user files to any cloud or third-party servers. When triggered from the Nautilus file manager, operations notify the user via native desktop notifications (`notify-send`) and write output files directly alongside the source files.

---

## 2. Directory Architecture

```
FILE-to-file/
├── core/
│   ├── __init__.py
│   ├── notify.py           # Desktop notification & progress helper
│   ├── video_audio.py      # Video and Audio conversion engine (ffmpeg)
│   ├── image_converter.py  # Image conversion engine (Pillow / ImageMagick)
│   ├── pdf_doc.py          # PDF & Document engine (PyMuPDF / pdf2docx / LibreOffice)
│   └── gif_converter.py    # GIF creation and conversion engine (ffmpeg / Pillow)
├── scripts/
│   ├── 1_Video_and_Audio/
│   │   ├── Video to MP4
│   │   ├── Video to MP3
│   │   ├── Audio to MP3
│   │   ├── Audio to WAV
│   │   ├── Audio to OGG
│   │   └── MOV to MP4
│   ├── 2_Image/
│   │   ├── Image to PNG
│   │   ├── Image to JPG
│   │   ├── Image to WebP
│   │   ├── Image to ICO
│   │   ├── WEBP to PNG
│   │   ├── JFIF to PNG
│   │   ├── HEIC to JPG
│   │   ├── HEIC to PNG
│   │   ├── SVG to PNG
│   │   └── PNG to SVG
│   ├── 3_PDF_and_Documents/
│   │   ├── PDF to Word (DOCX)
│   │   ├── PDF to Images (PNG)
│   │   ├── PDF to Images (JPG)
│   │   ├── Images to PDF
│   │   ├── Office Doc to PDF
│   │   ├── EPUB to PDF
│   │   └── PDF to EPUB
│   └── 4_GIF/
│       ├── Video to GIF
│       ├── GIF to MP4
│       ├── Images to Animated GIF
│       ├── GIF to APNG
│       └── APNG to GIF
├── tests/
│   └── test_converters.py  # Integration & unit tests
├── install.sh              # One-click installer for Nautilus scripts
├── uninstall.sh            # Uninstaller
├── requirements.txt        # Optional Python dependencies
└── README.md               # Complete user guide
```

---

## 3. Detailed Component Specifications

### 3.1 Core Engines

1. **`video_audio.py`**:
   - Uses `ffmpeg` with standard encoding parameters.
   - `video_to_mp4`: `-c:v libx264 -preset fast -crf 22 -c:a aac -b:a 192k`
   - `to_mp3`: `-vn -c:a libmp3lame -q:a 2` (VBR ~190kbps high quality)
   - `to_wav`: `-vn -c:a pcm_s16le`
   - `to_ogg`: `-vn -c:a libvorbis -q:a 5`

2. **`image_converter.py`**:
   - Uses `PIL.Image` (Pillow) with RGBA $\leftrightarrow$ RGB auto-handling (e.g. converting PNG with alpha to JPG with white background).
   - Format conversion: `PNG`, `JPG`/`JPEG`, `WEBP`, `ICO`, `BMP`, `TIFF`.
   - `jfif_to_png`: Native Pillow load and PNG save.
   - `heic_to_format`: Tries `pillow_heif` if available, falls back to `magick` or `ffmpeg`.
   - `png_to_svg`: Vectorization or scalable SVG wrapping.
   - `svg_to_png`: Uses `cairosvg` or `magick` rasterization.

3. **`pdf_doc.py`**:
   - `pdf_to_docx`: Uses `pdf2docx.Converter` to reconstruct layout and text into Microsoft Word format.
   - `pdf_to_images`: Uses `pymupdf` (fitz) or `pdftoppm` with configurable DPI (default 150-200 DPI). Each page is rendered as `<pdf_name>_page_N.<ext>`.
   - `images_to_pdf`: Uses `PIL.Image` to merge selected image files into a single multi-page PDF with `save(pdf_path, save_all=True, append_images=...)`.
   - `office_to_pdf`: Invokes `libreoffice --headless --convert-to pdf` for DOCX, XLSX, PPTX, ODT, TXT.
   - `epub_to_pdf` / `pdf_to_epub`: Invokes `ebook-convert` or `pandoc` if present, with graceful error handling.

4. **`gif_converter.py`**:
   - `video_to_gif`: High-quality 2-pass palette generation using `ffmpeg`:
     `-vf "fps=15,scale=480:-1:flags=lanczos,split[s0][s1];[s0]palettegen[p];[s1][p]paletteuse"`
   - `gif_to_mp4`: `-movflags faststart -pix_fmt yuv420p -vf "scale=trunc(iw/2)*2:trunc(ih/2)*2"`
   - `images_to_gif`: Uses `PIL.Image` with `save(..., save_all=True, duration=200, loop=0)`.

---

## 4. Nautilus Integration (`NAUTILUS_SCRIPT_SELECTED_FILE_PATHS`)
Nautilus populates the environment variable `NAUTILUS_SCRIPT_SELECTED_FILE_PATHS` with newline-delimited paths of selected files.
Each script:
1. Reads `NAUTILUS_SCRIPT_SELECTED_FILE_PATHS`.
2. Triggers `notify-send "FILE-to-file" "🔄 กำลังแปลงไฟล์..."`.
3. Invokes corresponding python core converter with the list of files.
4. Triggers `notify-send "FILE-to-file" "✅ แปลงไฟล์สำเร็จ: <ชื่อไฟล์>"`.

---

## 5. Testing & Verification
- Unit and integration tests for every format conversion in `tests/test_converters.py`.
- Automated test run generates sample files (PDF, image, audio, doc) and verifies output file creation, integrity, and non-zero byte size.

---

## 6. Deployment & Git
- Push to GitHub remote `https://github.com/n0ngXarm/FILE-to-file.git` on branch `main`.
