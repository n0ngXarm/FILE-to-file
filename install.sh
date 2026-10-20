#!/usr/bin/env bash
# ==============================================================================
# FILE-to-file: Universal Linux Installer
# Automated setup for GNOME Nautilus Context Menu & CLI
# ==============================================================================
set -e

# Detect current project location
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TARGET_DIR="${HOME}/.local/share/nautilus/scripts/FILE-to-file"
CONFIG_DIR="${HOME}/.config/FILE-to-file"

echo "=========================================================="
echo "          🚀 ติดตั้ง FILE-to-file Converter               "
echo "=========================================================="
echo "📂 โฟลเดอร์ต้นทาง: ${SCRIPT_DIR}"

# 1. Save config path
mkdir -p "${CONFIG_DIR}"
echo "${SCRIPT_DIR}" > "${CONFIG_DIR}/path.conf"

# 2. Check system prerequisites
MISSING_PKGS=()

which ffmpeg >/dev/null 2>&1 || MISSING_PKGS+=("ffmpeg")
which pdftoppm >/dev/null 2>&1 || MISSING_PKGS+=("poppler-utils (pdftoppm)")
which libreoffice >/dev/null 2>&1 || which soffice >/dev/null 2>&1 || MISSING_PKGS+=("libreoffice")
which zenity >/dev/null 2>&1 || MISSING_PKGS+=("zenity")
which notify-send >/dev/null 2>&1 || MISSING_PKGS+=("libnotify (notify-send)")

if [ ${#MISSING_PKGS[@]} -gt 0 ]; then
    echo ""
    echo "⚠️  ตรวจพบโปรแกรมเสริมที่แนะนำยังไม่ได้ติดตั้ง:"
    for pkg in "${MISSING_PKGS[@]}"; do
        echo "   - $pkg"
    done
    echo ""
    echo "💡 คำสั่งแนะนำในการติดตั้งตาม OS ของคุณ:"
    if [ -f /etc/fedora-release ] || [ -f /etc/redhat-release ]; then
        echo "   👉 sudo dnf install -y ffmpeg poppler-utils libreoffice zenity libnotify"
    elif [ -f /etc/debian_version ] || [ -f /etc/lsb-release ]; then
        echo "   👉 sudo apt update && sudo apt install -y ffmpeg poppler-utils libreoffice zenity libnotify-bin"
    elif [ -f /etc/arch-release ]; then
        echo "   👉 sudo pacman -S --needed ffmpeg poppler libreoffice-fresh zenity libnotify"
    else
        echo "   👉 กรุณาติดตั้งผ่าน Package Manager ของระบบคุณ"
    fi
    echo ""
else
    echo "✅ เครื่องมือพื้นฐานของระบบครบถ้วนสมบูรณ์!"
fi

# 3. Install Python requirements
echo "📦 กำลังตรวจสอบ Python packages..."
python3 -m pip install --quiet -r "${SCRIPT_DIR}/requirements.txt" 2>/dev/null || true

# 4. Copy scripts to Nautilus Scripts directory
echo "🔗 กำลังเชื่อมต่อเข้าสู่ Nautilus Context Menu..."
mkdir -p "${TARGET_DIR}"

# Ensure script generation is up to date
python3 "${SCRIPT_DIR}/scripts/generate_scripts.py" >/dev/null 2>&1 || true

# Copy Auto Convert script
cp -f "${SCRIPT_DIR}/scripts/⚡ Smart Auto Convert" "${TARGET_DIR}/"

# Copy category folders
cp -r "${SCRIPT_DIR}/scripts/1_Video_and_Audio" "${TARGET_DIR}/"
cp -r "${SCRIPT_DIR}/scripts/2_Image" "${TARGET_DIR}/"
cp -r "${SCRIPT_DIR}/scripts/3_PDF_and_Documents" "${TARGET_DIR}/"
cp -r "${SCRIPT_DIR}/scripts/4_GIF" "${TARGET_DIR}/"

# Set executable permissions
find "${TARGET_DIR}" -type f -exec chmod +x {} +
chmod +x "${SCRIPT_DIR}/scripts/run_action.sh"
chmod +x "${SCRIPT_DIR}/install.sh"
chmod +x "${SCRIPT_DIR}/uninstall.sh"

echo "=========================================================="
echo "🎉 ติดตั้งสำเร็จเรียบร้อยแล้ว!"
echo "📁 เมนูถูกติดตั้งไว้ที่: ${TARGET_DIR}"
echo ""
echo "🖱️  วิธีใช้งาน:"
echo "1. เปิดโปรแกรมจัดการไฟล์ (Nautilus)"
echo "2. คลิกขวาที่ไฟล์ใดก็ได้"
echo "3. เลือกเมนู 'Scripts' -> 'FILE-to-file'"
echo "4. เลือก '⚡ Smart Auto Convert' หรือเลือกตามหมวดหมู่ได้ทันที!"
echo "=========================================================="

if which notify-send >/dev/null 2>&1; then
    notify-send -a "FILE-to-file" -i "dialog-information" "FILE-to-file" "✅ ติดตั้งเมนูคลิกขวาเรียบร้อยแล้ว พร้อมใช้งานทันที!"
fi
