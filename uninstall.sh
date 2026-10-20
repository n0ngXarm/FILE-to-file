#!/usr/bin/env bash
# Uninstaller for FILE-to-file
NAUTILUS_SCRIPTS_DIR="${HOME}/.local/share/nautilus/scripts"
TARGET_DIR="${NAUTILUS_SCRIPTS_DIR}/FILE-to-file"
CONFIG_DIR="${HOME}/.config/FILE-to-file"

echo "🗑️  กำลังถอนการติดตั้ง FILE-to-file..."

rm -f "${NAUTILUS_SCRIPTS_DIR}/FILE-to-file"
rm -f "${NAUTILUS_SCRIPTS_DIR}/⚡ แปลงไฟล์ (FILE-to-file)"
rm -f "${NAUTILUS_SCRIPTS_DIR}/⚡ Convert File (FILE-to-file)"
rm -f "${NAUTILUS_SCRIPTS_DIR}/⚡ Smart Auto Convert"

if [ -d "${TARGET_DIR}" ]; then
    rm -rf "${TARGET_DIR}"
    echo "✅ ลบเมนูคลิกขวารุ่นเก่าเรียบร้อยแล้ว"
fi

if [ -d "${CONFIG_DIR}" ]; then
    rm -rf "${CONFIG_DIR}"
    echo "✅ ลบการตั้งค่าเรียบร้อยแล้ว"
fi

if which notify-send >/dev/null 2>&1; then
    notify-send -a "FILE-to-file" "FILE-to-file" "ถอนการติดตั้งเรียบร้อยแล้ว"
fi

echo "ถอนการติดตั้งเสร็จสิ้น"
