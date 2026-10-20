import os
from pathlib import Path

def get_unique_output_path(desired_path: Path, overwrite: bool = False) -> Path:
    """
    Returns a unique file path. If desired_path already exists and overwrite is False,
    appends _1, _2, etc., before the suffix to avoid accidental data loss.
    """
    if overwrite or not desired_path.exists():
        return desired_path

    parent = desired_path.parent
    stem = desired_path.stem
    suffix = desired_path.suffix

    counter = 1
    while True:
        candidate = parent / f"{stem}_{counter}{suffix}"
        if not candidate.exists():
            return candidate
        counter += 1
