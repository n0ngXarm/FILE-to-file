#!/usr/bin/env bash
# Uninstaller for FILE-to-file
TARGET_DIR="${HOME}/.local/share/nautilus/scripts/FILE-to-file"
CONFIG_DIR="${HOME}/.config/FILE-to-file"

echo "🗑️  กำลังถอนการติดตั้ง FILE-to-file..."

if [ -d "${TARGET_DIR}" ]; then
    rm -rf "${TARGET_DIR}"
    echo "✅ ลบเมนูคลิกขวาเรียบร้อยแล้ว"
fi

if [ -d "${CONFIG_DIR}" ]; then
    rm -rf "${CONFIG_DIR}"
    echo "✅ ลบการตั้งค่าเรียบร้อยแล้ว"
fi

if which notify-send >/dev/null 2>&1; then
    notify-send -a "FILE-to-file" "FILE-to-file" "ถอนการติดตั้งเรียบร้อยแล้ว"
fi

echo "ถอนการติดตั้งเสร็จสิ้น"
