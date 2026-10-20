import os
import sys
import shutil
import subprocess
from pathlib import Path
from core.notify import send_notification, show_error_dialog
from core.ui_dialog import select_target_format

def detect_file_type(file_path: str) -> dict:
    """
    Detects the true type of a file using both extension and system MIME analysis.
    """
    src = Path(file_path)
    ext = src.suffix.lower().lstrip(".")

    mime = "application/octet-stream"
    human_desc = "Unknown File"

    try:
        res = subprocess.run(["file", "--mime-type", "-b", str(src)], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True, check=True)
        mime = res.stdout.strip()
    except Exception:
        pass

    try:
        res2 = subprocess.run(["file", "-b", str(src)], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True, check=True)
        human_desc = res2.stdout.strip()
    except Exception:
        pass

    # Categorize
    category = "unknown"
    if mime == "application/pdf" or ext == "pdf":
        category = "pdf"
        human_desc = "เอกสาร PDF (Portable Document Format)"
    elif mime.startswith("image/") or ext in ("png", "jpg", "jpeg", "webp", "gif", "heic", "heif", "jfif", "bmp", "tiff", "ico", "svg"):
        category = "image"
        human_desc = f"ไฟล์รูปภาพ ({mime} / .{ext})"
    elif mime.startswith("video/") or ext in ("mp4", "mkv", "avi", "mov", "webm", "flv", "wmv", "m4v"):
        category = "video"
        human_desc = f"ไฟล์วิดีโอ ({mime} / .{ext})"
    elif mime.startswith("audio/") or ext in ("mp3", "wav", "ogg", "aac", "m4a", "flac", "wma"):
        category = "audio"
        human_desc = f"ไฟล์เสียง ({mime} / .{ext})"
    elif mime in (
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        "application/vnd.openxmlformats-officedocument.presentationml.presentation",
        "application/msword",
        "application/vnd.ms-excel",
        "application/vnd.ms-powerpoint",
        "application/vnd.oasis.opendocument.text",
        "text/plain",
        "text/markdown",
        "text/csv"
    ) or ext in ("docx", "doc", "xlsx", "xls", "pptx", "ppt", "odt", "ods", "odp", "txt", "md", "csv"):
        category = "office"
        human_desc = f"เอกสาร Office / ข้อความ ({mime} / .{ext})"
    elif ext == "epub" or "epub" in mime:
        category = "epub"
        human_desc = "หนังสืออิเล็กทรอนิกส์ Ebook (EPUB)"

    return {
        "category": category,
        "mime": mime,
        "desc": human_desc,
        "ext": ext
    }

def get_options_for_category(category: str, is_multiple: bool = False) -> list:
    """
    Returns available conversion options: (key, title, module, action)
    """
    if category == "pdf":
        return [
            ("docx", "Word (.docx) - แปลงเป็นเอกสารแก้ไขข้อความได้", "core.pdf_doc", "pdf_to_docx"),
            ("png", "รูปภาพ PNG - เรนเดอร์แยกภาพทุกหน้า", "core.pdf_doc", "pdf_to_png"),
            ("jpg", "รูปภาพ JPG - เรนเดอร์แยกภาพทุกหน้า", "core.pdf_doc", "pdf_to_jpg"),
            ("epub", "Ebook (.epub) - แปลงเป็นหนังสือดิจิทัล", "core.pdf_doc", "pdf_to_epub"),
        ]
    elif category == "image":
        opts = [
            ("png", "PNG - รูปภาพคมชัดสูง / รองรับพื้นหลังโปร่งใส", "core.image_converter", "to_png"),
            ("jpg", "JPG - รูปภาพขนาดกะทัดรัดมาตรฐาน", "core.image_converter", "to_jpg"),
            ("webp", "WebP - รูปภาพโหลดเร็ว ประหยัดพื้นที่จัดเก็บ", "core.image_converter", "to_webp"),
            ("pdf", "PDF - รวมภาพเป็นเอกสาร PDF", "core.pdf_doc", "images_to_pdf"),
            ("ico", "ICO - ไอคอนหลายขนาด (16x16 ถึง 256x256)", "core.image_converter", "to_ico"),
        ]
        if is_multiple:
            opts.append(("gif", "GIF - รวมภาพทั้งหมดเป็นภาพเคลื่อนไหว", "core.gif_converter", "images_to_gif"))
        return opts
    elif category == "video":
        return [
            ("mp3", "MP3 - แยกดูดเสียงออกจากวิดีโอ (คุณภาพสูง)", "core.video_audio", "to_mp3"),
            ("gif", "GIF - แปลงคลิปเป็นภาพเคลื่อนไหว GIF", "core.gif_converter", "video_to_gif"),
            ("mp4", "MP4 - แปลงเป็นวิดีโอมาตรฐานสากล H.264", "core.video_audio", "to_mp4"),
            ("wav", "WAV - แยกเสียงแบบไม่สูญเสียคุณภาพ (Lossless)", "core.video_audio", "to_wav"),
        ]
    elif category == "audio":
        return [
            ("mp3", "MP3 - แปลงเป็นไฟล์เสียงมาตรฐานสากล", "core.video_audio", "to_mp3"),
            ("wav", "WAV - แปลงเป็นเสียง Lossless", "core.video_audio", "to_wav"),
            ("ogg", "OGG - แปลงเป็นเสียง Vorbis", "core.video_audio", "to_ogg"),
        ]
    elif category in ("office", "epub"):
        return [
            ("pdf", "PDF - บันทึกเป็นเอกสาร PDF มาตรฐาน", "core.pdf_doc", "doc_to_pdf"),
        ]
    else:
        # Unknown fallback: offer text/hex or view info
        return [
            ("pdf", "ลองแปลงเป็น PDF (หากเป็นเอกสาร/ข้อความ)", "core.pdf_doc", "doc_to_pdf"),
        ]

def ask_user_choice_zenity(file_info: dict, options: list, filename: str) -> tuple:
    """
    Shows a clean Zenity dialog for the user to choose their desired target format.
    """
    if not shutil.which("zenity") or not os.environ.get("DISPLAY"):
        return options[0]  # Default to first option if GUI not available

    cmd = [
        "zenity", "--list", "--radiolist",
        "--title=⚡ Smart Auto Convert",
        f"--text=ตรวจพบ: <b>{file_info['desc']}</b>\nไฟล์: <i>{filename}</i>\n\nกรุณาเลือกรูปแบบที่ต้องการแปลง:",
        "--column=เลือก", "--column=รหัส", "--column=รูปแบบผลลัพธ์",
        "--height=340", "--width=520"
    ]

    for i, (key, desc, _, _) in enumerate(options):
        selected = "TRUE" if i == 0 else "FALSE"
        cmd.extend([selected, key, desc])

    try:
        res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True)
        chosen_key = res.stdout.strip()
        if not chosen_key:
            return None  # User clicked cancel
        for opt in options:
            if opt[0] == chosen_key:
                return opt
    except Exception:
        pass

    return options[0]

def auto_convert_files(files: list):
    if not files:
        send_notification("⚡ Smart Auto Convert", "⚠️ ไม่มีไฟล์ที่ถูกเลือก")
        return

    first_file = files[0]
    file_info = detect_file_type(first_file)
    is_multiple = len(files) > 1

    options = get_options_for_category(file_info["category"], is_multiple=is_multiple)

    display_name = os.path.basename(first_file)
    if is_multiple:
        display_name += f" (และอีก {len(files) - 1} ไฟล์)"

    choice = select_target_format(file_info, options, display_name)
    if not choice:
        # User canceled
        return

    key, title, module, action = choice

    # Invoke module action
    send_notification("⚡ Smart Auto Convert", f"🔄 กำลังแปลงไฟล์เป็น {key.upper()}...")

    cmd = [sys.executable, "-m", module, action] + files
    res = subprocess.run(cmd)
    if res.returncode != 0:
        show_error_dialog("ข้อผิดพลาด", "ไม่สามารถแปลงไฟล์ได้ กรุณาตรวจสอบความถูกต้องของไฟล์")

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 -m core.auto_convert [action] <file1> [file2...]")
        sys.exit(1)

    args = sys.argv[1:]
    if args[0] == "auto":
        files = args[1:]
    else:
        files = args

    auto_convert_files(files)

if __name__ == "__main__":
    main()
