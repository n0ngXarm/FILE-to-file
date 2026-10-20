#!/usr/bin/env bash
# FILE-to-file portable runner
set -e

# Dynamically resolve project directory
if [ -n "$FILE_TO_FILE_HOME" ] && [ -d "$FILE_TO_FILE_HOME" ]; then
    PROJECT_DIR="$FILE_TO_FILE_HOME"
elif [ -f "${HOME}/.config/FILE-to-file/path.conf" ] && [ -d "$(cat "${HOME}/.config/FILE-to-file/path.conf")" ]; then
    PROJECT_DIR="$(cat "${HOME}/.config/FILE-to-file/path.conf")"
elif [ -d "${HOME}/.local/share/FILE-to-file" ]; then
    PROJECT_DIR="${HOME}/.local/share/FILE-to-file"
else
    DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
    PROJECT_DIR="$(cd "${DIR}/.." && pwd)"
fi

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
    if which notify-send >/dev/null 2>&1; then
        notify-send -a "FILE-to-file" "⚠️ กรุณาเลือกไฟล์ก่อนกดใช้งาน"
    fi
    exit 0
fi

MODULE="$1"
ACTION="$2"

exec python3 -m "${MODULE}" "${ACTION}" "${FILES[@]}"
