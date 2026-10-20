#!/usr/bin/env bash
# Installer for FILE-to-file Nautilus context menu
set -e

PROJECT_DIR="/home/nong_ing/Projects/FILE-to-file"
TARGET_DIR="${HOME}/.local/share/nautilus/scripts/FILE-to-file"

echo "============================================="
echo "   🚀 ติดตั้ง FILE-to-file เข้า Nautilus      "
echo "============================================="

# Ensure target scripts directory exists
mkdir -p "${TARGET_DIR}"

# Copy category folders
cp -r "${PROJECT_DIR}/scripts/1_Video_and_Audio" "${TARGET_DIR}/"
cp -r "${PROJECT_DIR}/scripts/2_Image" "${TARGET_DIR}/"
cp -r "${PROJECT_DIR}/scripts/3_PDF_and_Documents" "${TARGET_DIR}/"
cp -r "${PROJECT_DIR}/scripts/4_GIF" "${TARGET_DIR}/"

# Make all scripts executable
find "${TARGET_DIR}" -type f -exec chmod +x {} +
chmod +x "${PROJECT_DIR}/scripts/run_action.sh"

echo "✅ ติดตั้งสคริปต์ลงใน: ${TARGET_DIR}"
echo ""
echo "วิธีใช้งาน:"
echo "1. เปิดตัวจัดการไฟล์ (Nautilus)"
echo "2. เลือกไฟล์ที่ต้องการแปลง"
echo "3. คลิกขวา -> Scripts -> FILE-to-file -> เลือกหมวดหมู่และคำสั่งที่ต้องการได้ทันที!"

if which notify-send >/dev/null 2>&1; then
    notify-send -a "FILE-to-file" -i "dialog-information" "FILE-to-file" "✅ ติดตั้งเมนูคลิกขวาเรียบร้อยแล้ว!"
fi
