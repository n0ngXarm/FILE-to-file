import shutil
import subprocess
import os

def send_notification(title: str, message: str, urgency: str = "normal", icon: str = "dialog-information"):
    """
    Sends a desktop notification using notify-send if available.
    """
    if shutil.which("notify-send"):
        try:
            subprocess.run(
                [
                    "notify-send",
                    "-a", "FILE-to-file",
                    "-u", urgency,
                    "-i", icon,
                    title,
                    message
                ],
                check=False
            )
        except Exception:
            pass

def show_error_dialog(title: str, message: str):
    """
    Shows an error popup dialog using zenity if available.
    """
    if shutil.which("zenity") and os.environ.get("DISPLAY"):
        try:
            subprocess.run(
                ["zenity", "--error", f"--title={title}", f"--text={message}", "--timeout=10"],
                check=False
            )
        except Exception:
            pass
    send_notification(title, message, urgency="critical", icon="dialog-error")
