import os
import sys
import shutil
import subprocess
from pathlib import Path
from PIL import Image
from core.notify import send_notification, show_error_dialog

def pdf_to_docx(input_path: str) -> str:
    """Converts PDF document to editable Word .docx format."""
    src = Path(input_path)
    output_path = src.with_suffix(".docx")

    try:
        from pdf2docx import Converter
        cv = Converter(str(src))
        cv.convert(str(output_path), start=0, end=None)
        cv.close()
        return str(output_path)
    except Exception as e:
        # Fallback to libreoffice writer
        if shutil.which("libreoffice") or shutil.which("soffice"):
            cmd_bin = "libreoffice" if shutil.which("libreoffice") else "soffice"
            subprocess.run([cmd_bin, "--headless", "--convert-to", "docx", str(src), "--outdir", str(src.parent)], check=True)
            return str(output_path)
        raise e

def pdf_to_images(input_path: str, fmt: str = "png", dpi: int = 150) -> list:
    """Converts each page of a PDF document into an image."""
    src = Path(input_path)
    fmt = fmt.lower().lstrip(".")
    out_files = []

    # Try PyMuPDF
    try:
        import pymupdf as fitz
        doc = fitz.open(str(src))
        zoom = dpi / 72.0
        mat = fitz.Matrix(zoom, zoom)
        for page_num in range(len(doc)):
            page = doc[page_num]
            pix = page.get_pixmap(matrix=mat, alpha=False if fmt in ("jpg", "jpeg") else True)
            out_file = src.parent / f"{src.stem}_page_{page_num + 1}.{fmt}"
            pix.save(str(out_file))
            out_files.append(str(out_file))
        doc.close()
        return out_files
    except Exception:
        pass

    # Fallback to pdftoppm
    if shutil.which("pdftoppm"):
        prefix = str(src.parent / f"{src.stem}_page")
        flag = f"-{fmt}" if fmt in ("png", "jpeg") else "-png"
        cmd = ["pdftoppm", flag, "-r", str(dpi), str(src), prefix]
        subprocess.run(cmd, check=True)
        return [str(p) for p in src.parent.glob(f"{src.stem}_page*")]

    raise RuntimeError("ไม่สามารถแปลง PDF เป็นภาพได้ กรุณาติดตั้ง pymupdf หรือ poppler-utils")

def images_to_pdf(image_paths: list, output_path: str = None) -> str:
    """Combines multiple image files into a single multi-page PDF document."""
    if not image_paths:
        raise ValueError("ไม่มีไฟล์รูปภาพให้รวม")

    first_path = Path(image_paths[0])
    if not output_path:
        if len(image_paths) == 1:
            output_path = str(first_path.with_suffix(".pdf"))
        else:
            output_path = str(first_path.parent / f"Combined_{first_path.stem}.pdf")

    images = []
    first_image = None

    for p in image_paths:
        try:
            img = Image.open(p)
            if img.mode != "RGB":
                img = img.convert("RGB")
            if first_image is None:
                first_image = img
            else:
                images.append(img)
        except Exception as e:
            print(f"Skipping {p}: {e}")

    if not first_image:
        raise ValueError("ไม่สามารถเปิดไฟล์รูปภาพที่เลือกได้")

    first_image.save(output_path, "PDF", resolution=100.0, save_all=True, append_images=images)
    return output_path

def office_to_pdf(input_path: str) -> str:
    """Converts DOCX, PPTX, XLSX, ODT, TXT to PDF using LibreOffice headless."""
    src = Path(input_path)
    output_path = src.with_suffix(".pdf")

    cmd_bin = "libreoffice" if shutil.which("libreoffice") else "soffice"
    if not cmd_bin:
        raise RuntimeError("ไม่พบ LibreOffice ในระบบ กรุณาติดตั้ง libreoffice")

    cmd = [cmd_bin, "--headless", "--convert-to", "pdf", str(src), "--outdir", str(src.parent)]
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
    return str(output_path)

def epub_to_pdf(input_path: str) -> str:
    """Converts EPUB ebook to PDF."""
    src = Path(input_path)
    output_path = src.with_suffix(".pdf")

    if shutil.which("ebook-convert"):
        subprocess.run(["ebook-convert", str(src), str(output_path)], check=True)
        return str(output_path)
    elif shutil.which("pandoc"):
        subprocess.run(["pandoc", str(src), "-o", str(output_path)], check=True)
        return str(output_path)
    elif shutil.which("libreoffice"):
        return office_to_pdf(input_path)
    raise RuntimeError("กรุณาติดตั้ง ebook-convert (Calibre) หรือ pandoc เพื่อแปลง EPUB")

def pdf_to_epub(input_path: str) -> str:
    """Converts PDF to EPUB ebook."""
    src = Path(input_path)
    output_path = src.with_suffix(".epub")

    if shutil.which("ebook-convert"):
        subprocess.run(["ebook-convert", str(src), str(output_path)], check=True)
        return str(output_path)
    elif shutil.which("pandoc"):
        subprocess.run(["pandoc", str(src), "-o", str(output_path)], check=True)
        return str(output_path)
    raise RuntimeError("กรุณาติดตั้ง ebook-convert (Calibre) หรือ pandoc เพื่อแปลงเป็น EPUB")

def main():
    if len(sys.argv) < 3:
        print("Usage: python3 -m core.pdf_doc <action> <file1> [file2...]")
        print("Actions: pdf_to_docx, pdf_to_png, pdf_to_jpg, images_to_pdf, doc_to_pdf, epub_to_pdf, pdf_to_epub")
        sys.exit(1)

    action = sys.argv[1]
    files = sys.argv[2:]

    send_notification("📄 FILE-to-file: Document", f"กำลังแปลง {len(files)} ไฟล์เอกสาร...")

    success_count = 0
    errors = []

    if action == "images_to_pdf":
        try:
            out = images_to_pdf(files)
            send_notification("✅ FILE-to-file: Document", f"รวมรูปภาพสำเร็จเป็น PDF:\n{os.path.basename(out)}")
            return
        except Exception as e:
            show_error_dialog("ข้อผิดพลาดในการรวมรูปภาพเป็น PDF", str(e))
            return

    for f in files:
        if not os.path.exists(f):
            continue
        try:
            if action in ("pdf_to_docx", "pdf_to_word"):
                out = pdf_to_docx(f)
            elif action == "pdf_to_png":
                out = pdf_to_images(f, "png")
            elif action == "pdf_to_jpg":
                out = pdf_to_images(f, "jpg")
            elif action in ("doc_to_pdf", "office_to_pdf"):
                out = office_to_pdf(f)
            elif action == "epub_to_pdf":
                out = epub_to_pdf(f)
            elif action == "pdf_to_epub":
                out = pdf_to_epub(f)
            else:
                out = office_to_pdf(f)
            success_count += 1
        except Exception as e:
            errors.append(f"{os.path.basename(f)}: {str(e)}")

    if errors:
        show_error_dialog("ข้อผิดพลาดในการแปลงเอกสาร", "\n".join(errors))
    else:
        send_notification("✅ FILE-to-file: Document", f"แปลงเอกสารสำเร็จ {success_count} ไฟล์เรียบร้อยแล้ว!")

if __name__ == "__main__":
    main()
