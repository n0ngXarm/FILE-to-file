#!/usr/bin/env bash
# FILE-to-file runner
set -e

# Project root directory
PROJECT_DIR="/home/nong_ing/Projects/FILE-to-file"
export PYTHONPATH="${PROJECT_DIR}:${PYTHONPATH}"

# Gather files
FILES=()
if [ -n "$NAUTILUS_SCRIPT_SELECTED_FILE_PATHS" ]; then
    while IFS= read -r line; do
        [ -n "$line" ] && FILES+=("$line")
    done <<< "$NAUTILUS_SCRIPT_SELECTED_FILE_PATHS"
else
    FILES=("$@")
fi

if [ ${#FILES[@]} -eq 0 ]; then
    notify-send "FILE-to-file" "⚠️ กรุณาเลือกไฟล์ก่อนกดใช้งาน"
    exit 0
fi

MODULE="$1"
ACTION="$2"

python3 -m "${MODULE}" "${ACTION}" "${FILES[@]}"
