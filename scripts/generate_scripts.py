import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

SCRIPTS = {
    "1_Video_and_Audio": [
        ("Video to MP4", "core.video_audio", "to_mp4"),
        ("Video to MP3", "core.video_audio", "to_mp3"),
        ("Audio to MP3", "core.video_audio", "to_mp3"),
        ("Audio to WAV", "core.video_audio", "to_wav"),
        ("Audio to OGG", "core.video_audio", "to_ogg"),
        ("MOV to MP4", "core.video_audio", "mov_to_mp4"),
    ],
    "2_Image": [
        ("Image to PNG", "core.image_converter", "to_png"),
        ("Image to JPG", "core.image_converter", "to_jpg"),
        ("Image to WebP", "core.image_converter", "to_webp"),
        ("Image to ICO", "core.image_converter", "to_ico"),
        ("WEBP to PNG", "core.image_converter", "webp_to_png"),
        ("JFIF to PNG", "core.image_converter", "jfif_to_png"),
        ("HEIC to JPG", "core.image_converter", "heic_to_jpg"),
        ("HEIC to PNG", "core.image_converter", "heic_to_png"),
        ("SVG to PNG", "core.image_converter", "svg_to_png"),
        ("PNG to SVG", "core.image_converter", "to_svg"),
    ],
    "3_PDF_and_Documents": [
        ("PDF to Word (DOCX)", "core.pdf_doc", "pdf_to_docx"),
        ("PDF to Images (PNG)", "core.pdf_doc", "pdf_to_png"),
        ("PDF to Images (JPG)", "core.pdf_doc", "pdf_to_jpg"),
        ("Images to PDF", "core.pdf_doc", "images_to_pdf"),
        ("Office Doc to PDF", "core.pdf_doc", "doc_to_pdf"),
        ("EPUB to PDF", "core.pdf_doc", "epub_to_pdf"),
        ("PDF to EPUB", "core.pdf_doc", "pdf_to_epub"),
    ],
    "4_GIF": [
        ("Video to GIF", "core.gif_converter", "video_to_gif"),
        ("GIF to MP4", "core.gif_converter", "gif_to_mp4"),
        ("Images to Animated GIF", "core.gif_converter", "images_to_gif"),
        ("GIF to APNG", "core.gif_converter", "gif_to_apng"),
        ("APNG to GIF", "core.gif_converter", "apng_to_gif"),
    ]
}

def generate():
    runner_path = "/home/nong_ing/Projects/FILE-to-file/scripts/run_action.sh"
    for category, items in SCRIPTS.items():
        cat_dir = BASE_DIR / category
        cat_dir.mkdir(parents=True, exist_ok=True)
        for name, module, action in items:
            script_path = cat_dir / name
            content = f"""#!/usr/bin/env bash
exec "{runner_path}" "{module}" "{action}" "$@"
"""
            with open(script_path, "w", encoding="utf-8") as f:
                f.write(content)
            os.chmod(script_path, 0o755)
            print(f"Created: {script_path}")

if __name__ == "__main__":
    generate()
