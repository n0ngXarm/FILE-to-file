#!/usr/bin/env bash
# Uninstaller for FILE-to-file
TARGET_DIR="${HOME}/.local/share/nautilus/scripts/FILE-to-file"

if [ -d "${TARGET_DIR}" ]; then
    rm -rf "${TARGET_DIR}"
    echo "✅ ลบเมนูคลิกขวา FILE-to-file เรียบร้อยแล้ว"
    if which notify-send >/dev/null 2>&1; then
        notify-send -a "FILE-to-file" "FILE-to-file" "ถอนการติดตั้งเรียบร้อยแล้ว"
    fi
else
    echo "ℹ️ ไม่พบเมนู FILE-to-file ในระบบ"
fi
