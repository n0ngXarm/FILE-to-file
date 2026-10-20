import os
import sys
import shutil
import subprocess
from pathlib import Path
from PIL import Image
from core.notify import send_notification, show_error_dialog

def _check_ffmpeg():
    if not shutil.which("ffmpeg"):
        raise RuntimeError("ไม่พบคำสั่ง 'ffmpeg' ในระบบ กรุณาติดตั้ง ffmpeg ก่อนใช้งาน")

def video_to_gif(input_path: str, fps: int = 15, width: int = 480) -> str:
    """Converts video (MP4, WEBM, MOV, AVI, etc.) to high quality animated GIF."""
    _check_ffmpeg()
    src = Path(input_path)
    output_path = src.with_suffix(".gif")

    filter_complex = f"fps={fps},scale={width}:-1:flags=lanczos,split[s0][s1];[s0]palettegen[p];[s1][p]paletteuse"
    cmd = [
        "ffmpeg", "-y", "-i", str(src),
        "-vf", filter_complex,
        str(output_path)
    ]
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
    return str(output_path)

def gif_to_mp4(input_path: str) -> str:
    """Converts animated GIF to MP4 video for efficient storage and playback."""
    _check_ffmpeg()
    src = Path(input_path)
    output_path = src.with_suffix(".mp4")

    cmd = [
        "ffmpeg", "-y", "-i", str(src),
        "-movflags", "faststart",
        "-pix_fmt", "yuv420p",
        "-vf", "scale=trunc(iw/2)*2:trunc(ih/2)*2",
        str(output_path)
    ]
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
    return str(output_path)

def images_to_gif(image_paths: list, output_path: str = None, duration: int = 200) -> str:
    """Combines multiple still images into an animated GIF."""
    if not image_paths:
        raise ValueError("ไม่มีไฟล์รูปภาพให้แปลง")

    first_path = Path(image_paths[0])
    if not output_path:
        output_path = str(first_path.parent / f"Animated_{first_path.stem}.gif")

    frames = []
    first_frame = None

    for p in image_paths:
        try:
            img = Image.open(p)
            if first_frame is None:
                first_frame = img
            else:
                frames.append(img)
        except Exception as e:
            print(f"Skipping {p}: {e}")

    if not first_frame:
        raise ValueError("ไม่สามารถเปิดรูปภาพที่เลือกได้")

    first_frame.save(
        output_path,
        save_all=True,
        append_images=frames,
        duration=duration,
        loop=0,
        optimize=True
    )
    return output_path

def gif_to_apng(input_path: str) -> str:
    """Converts GIF to Animated PNG (APNG)."""
    _check_ffmpeg()
    src = Path(input_path)
    output_path = src.with_suffix(".png")
    if output_path == src:
        output_path = src.with_name(f"{src.stem}_animated.png")

    cmd = [
        "ffmpeg", "-y", "-i", str(src),
        "-plays", "0",
        "-f", "apng",
        str(output_path)
    ]
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
    return str(output_path)

def apng_to_gif(input_path: str) -> str:
    """Converts Animated PNG (APNG) to GIF."""
    return video_to_gif(input_path)

def main():
    if len(sys.argv) < 3:
        print("Usage: python3 -m core.gif_converter <action> <file1> [file2...]")
        print("Actions: video_to_gif, gif_to_mp4, images_to_gif, gif_to_apng, apng_to_gif")
        sys.exit(1)

    action = sys.argv[1]
    files = sys.argv[2:]

    send_notification("🎞️ FILE-to-file: GIF", f"กำลังแปลง {len(files)} ไฟล์...")

    success_count = 0
    errors = []

    if action == "images_to_gif":
        try:
            out = images_to_gif(files)
            send_notification("✅ FILE-to-file: GIF", f"สร้างภาพเคลื่อนไหว GIF สำเร็จ:\n{os.path.basename(out)}")
            return
        except Exception as e:
            show_error_dialog("ข้อผิดพลาดในการสร้าง GIF จากรูปภาพ", str(e))
            return

    for f in files:
        if not os.path.exists(f):
            continue
        try:
            if action in ("video_to_gif", "mp4_to_gif", "mov_to_gif", "webm_to_gif", "avi_to_gif"):
                out = video_to_gif(f)
            elif action == "gif_to_mp4":
                out = gif_to_mp4(f)
            elif action == "gif_to_apng":
                out = gif_to_apng(f)
            elif action == "apng_to_gif":
                out = apng_to_gif(f)
            else:
                out = video_to_gif(f)
            success_count += 1
        except Exception as e:
            errors.append(f"{os.path.basename(f)}: {str(e)}")

    if errors:
        show_error_dialog("ข้อผิดพลาดในการแปลงไฟล์ GIF", "\n".join(errors))
    else:
        send_notification("✅ FILE-to-file: GIF", f"แปลง GIF สำเร็จ {success_count} ไฟล์เรียบร้อยแล้ว!")

if __name__ == "__main__":
    main()
