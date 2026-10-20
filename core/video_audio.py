import os
import sys
import shutil
import subprocess
from pathlib import Path
from core.notify import send_notification, show_error_dialog
from core.utils import get_unique_output_path

def _check_ffmpeg():
    if not shutil.which("ffmpeg"):
        raise RuntimeError("ไม่พบคำสั่ง 'ffmpeg' ในระบบ กรุณาติดตั้ง ffmpeg ก่อนใช้งาน")

def video_to_mp4(input_path: str) -> str:
    _check_ffmpeg()
    src = Path(input_path).resolve()
    output_path = src.with_suffix(".mp4")
    if output_path == src:
        output_path = src.with_name(f"{src.stem}_converted.mp4")
    output_path = get_unique_output_path(output_path)
    
    cmd = [
        "ffmpeg", "-y", "-i", str(src),
        "-c:v", "libx264", "-preset", "fast", "-crf", "22",
        "-c:a", "aac", "-b:a", "192k",
        str(output_path)
    ]
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
    return str(output_path)

def video_to_mp3(input_path: str) -> str:
    _check_ffmpeg()
    src = Path(input_path).resolve()
    output_path = get_unique_output_path(src.with_suffix(".mp3"))
    cmd = [
        "ffmpeg", "-y", "-i", str(src),
        "-vn", "-c:a", "libmp3lame", "-q:a", "2",
        str(output_path)
    ]
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
    return str(output_path)

def audio_to_format(input_path: str, fmt: str = "mp3") -> str:
    _check_ffmpeg()
    src = Path(input_path).resolve()
    output_path = src.with_suffix(f".{fmt.lower()}")
    if output_path == src:
        output_path = src.with_name(f"{src.stem}_converted.{fmt.lower()}")
    output_path = get_unique_output_path(output_path)

    fmt_lower = fmt.lower()
    if fmt_lower == "mp3":
        codec = ["-c:a", "libmp3lame", "-q:a", "2"]
    elif fmt_lower == "wav":
        codec = ["-c:a", "pcm_s16le"]
    elif fmt_lower == "ogg":
        codec = ["-c:a", "libvorbis", "-q:a", "5"]
    elif fmt_lower == "aac":
        codec = ["-c:a", "aac", "-b:a", "192k"]
    elif fmt_lower == "m4a":
        codec = ["-c:a", "aac", "-b:a", "192k"]
    else:
        codec = []

    cmd = ["ffmpeg", "-y", "-i", str(src), "-vn"] + codec + [str(output_path)]
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
    return str(output_path)

def main():
    if len(sys.argv) < 3:
        print("Usage: python3 -m core.video_audio <action> <file1> [file2...]")
        print("Actions: to_mp4, to_mp3, to_wav, to_ogg, to_aac")
        sys.exit(1)

    action = sys.argv[1]
    files = sys.argv[2:]

    send_notification("FILE-to-file: Media", f"กำลังแปลง {len(files)} ไฟล์...")

    success_count = 0
    errors = []

    for f in files:
        if not os.path.exists(f):
            continue
        try:
            if action in ("to_mp4", "mov_to_mp4"):
                out = video_to_mp4(f)
            elif action in ("to_mp3", "video_to_mp3", "audio_to_mp3"):
                out = video_to_mp3(f)
            elif action == "to_wav":
                out = audio_to_format(f, "wav")
            elif action == "to_ogg":
                out = audio_to_format(f, "ogg")
            elif action == "to_aac":
                out = audio_to_format(f, "aac")
            else:
                out = audio_to_format(f, action.replace("to_", ""))
            success_count += 1
        except Exception as e:
            errors.append(f"{os.path.basename(f)}: {str(e)}")

    if errors:
        show_error_dialog("ข้อผิดพลาดในการแปลงไฟล์", "\n".join(errors))
    else:
        send_notification("FILE-to-file: Media", f"แปลงสำเร็จ {success_count} ไฟล์เรียบร้อยแล้ว")

if __name__ == "__main__":
    main()
