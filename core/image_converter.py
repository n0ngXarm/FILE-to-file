import os
import sys
import shutil
import subprocess
from pathlib import Path
from PIL import Image
from core.notify import send_notification, show_error_dialog

def _ensure_rgb(img: Image.Image) -> Image.Image:
    """Converts RGBA or LA images to RGB with white background for formats like JPEG."""
    if img.mode in ("RGBA", "LA", "P"):
        background = Image.new("RGB", img.size, (255, 255, 255))
        if img.mode == "P":
            img = img.convert("RGBA")
        background.paste(img, mask=img.split()[-1] if "A" in img.mode else None)
        return background
    elif img.mode != "RGB":
        return img.convert("RGB")
    return img

def convert_image(input_path: str, target_format: str) -> str:
    target_ext = target_format.lower().lstrip(".")
    src = Path(input_path)
    output_path = src.with_suffix(f".{target_ext}")
    if output_path == src:
        output_path = src.with_name(f"{src.stem}_converted.{target_ext}")

    # Check for HEIC
    if src.suffix.lower() in (".heic", ".heif"):
        return heic_to_format(input_path, target_ext)

    # Check for SVG source
    if src.suffix.lower() == ".svg":
        return svg_to_png(input_path, str(output_path))

    # Check for SVG target
    if target_ext == "svg":
        return png_to_svg(input_path)

    with Image.open(src) as img:
        if target_ext in ("jpg", "jpeg"):
            img = _ensure_rgb(img)
            img.save(output_path, "JPEG", quality=95, optimize=True)
        elif target_ext == "png":
            img.save(output_path, "PNG", optimize=True)
        elif target_ext == "webp":
            img.save(output_path, "WEBP", quality=90)
        elif target_ext == "ico":
            # For ICO, resize icon nicely
            sizes = [(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)]
            img.save(output_path, format="ICO", sizes=sizes)
        elif target_ext == "bmp":
            img = _ensure_rgb(img)
            img.save(output_path, "BMP")
        else:
            img.save(output_path, target_ext.upper())

    return str(output_path)

def jfif_to_png(input_path: str) -> str:
    return convert_image(input_path, "png")

def heic_to_format(input_path: str, target_format: str = "jpg") -> str:
    target_ext = target_format.lower().lstrip(".")
    src = Path(input_path)
    output_path = src.with_suffix(f".{target_ext}")

    # Try pillow_heif if available
    try:
        import pillow_heif
        pillow_heif.register_heif_opener()
        with Image.open(src) as img:
            if target_ext in ("jpg", "jpeg"):
                img = _ensure_rgb(img)
                img.save(output_path, "JPEG", quality=95)
            else:
                img.save(output_path, target_ext.upper())
        return str(output_path)
    except Exception:
        pass

    # Try ImageMagick
    if shutil.which("magick") or shutil.which("convert"):
        cmd_bin = "magick" if shutil.which("magick") else "convert"
        subprocess.run([cmd_bin, str(src), str(output_path)], check=True)
        return str(output_path)

    # Try ffmpeg
    if shutil.which("ffmpeg"):
        subprocess.run(["ffmpeg", "-y", "-i", str(src), str(output_path)], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
        return str(output_path)

    raise RuntimeError("ไม่สามารถแปลงไฟล์ HEIC ได้ กรุณาติดตั้ง pillow-heif หรือ libheif")

def png_to_svg(input_path: str) -> str:
    src = Path(input_path)
    output_path = src.with_suffix(".svg")

    # If potrace is installed, vectorize cleanly
    if shutil.which("potrace"):
        pnm_path = src.with_suffix(".pnm")
        try:
            with Image.open(src) as img:
                img.convert("1").save(pnm_path)
            subprocess.run(["potrace", str(pnm_path), "-s", "-o", str(output_path)], check=True)
            if pnm_path.exists():
                pnm_path.unlink()
            return str(output_path)
        except Exception:
            if pnm_path.exists():
                pnm_path.unlink()

    # Fallback: embed high-resolution PNG in standard scalable SVG wrapper
    with Image.open(src) as img:
        width, height = img.size
    import base64
    with open(src, "rb") as f:
        b64_data = base64.b64encode(f.read()).decode("utf-8")

    svg_content = f'''<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="{width}" height="{height}" viewBox="0 0 {width} {height}">
  <image width="{width}" height="{height}" xlink:href="data:image/png;base64,{b64_data}"/>
</svg>'''
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(svg_content)
    return str(output_path)

def svg_to_png(input_path: str, output_path: str = None) -> str:
    src = Path(input_path)
    if not output_path:
        output_path = str(src.with_suffix(".png"))

    # Try ImageMagick
    if shutil.which("magick") or shutil.which("convert"):
        cmd_bin = "magick" if shutil.which("magick") else "convert"
        subprocess.run([cmd_bin, "-background", "none", "-density", "300", str(src), str(output_path)], check=True)
        return str(output_path)

    # Try cairosvg if available
    try:
        import cairosvg
        cairosvg.svg2png(url=str(src), write_to=str(output_path))
        return str(output_path)
    except Exception:
        pass

    raise RuntimeError("ไม่สามารถแปลงไฟล์ SVG เป็น PNG ได้ กรุณาติดตั้ง ImageMagick")

def main():
    if len(sys.argv) < 3:
        print("Usage: python3 -m core.image_converter <action> <file1> [file2...]")
        print("Actions: to_png, to_jpg, to_webp, to_ico, to_svg, jfif_to_png, heic_to_jpg, heic_to_png")
        sys.exit(1)

    action = sys.argv[1]
    files = sys.argv[2:]

    send_notification("🖼️ FILE-to-file: Image", f"กำลังแปลง {len(files)} รูปภาพ...")

    success_count = 0
    errors = []

    for f in files:
        if not os.path.exists(f):
            continue
        try:
            if action in ("to_png", "webp_to_png", "jfif_to_png"):
                out = convert_image(f, "png")
            elif action in ("to_jpg", "webp_to_jpg"):
                out = convert_image(f, "jpg")
            elif action == "to_webp":
                out = convert_image(f, "webp")
            elif action == "to_ico":
                out = convert_image(f, "ico")
            elif action == "to_svg":
                out = png_to_svg(f)
            elif action == "svg_to_png":
                out = svg_to_png(f)
            elif action == "heic_to_jpg":
                out = heic_to_format(f, "jpg")
            elif action == "heic_to_png":
                out = heic_to_format(f, "png")
            else:
                fmt = action.replace("to_", "")
                out = convert_image(f, fmt)
            success_count += 1
        except Exception as e:
            errors.append(f"{os.path.basename(f)}: {str(e)}")

    if errors:
        show_error_dialog("ข้อผิดพลาดในการแปลงรูปภาพ", "\n".join(errors))
    else:
        send_notification("✅ FILE-to-file: Image", f"แปลงภาพสำเร็จ {success_count} ไฟล์เรียบร้อยแล้ว!")

if __name__ == "__main__":
    main()
