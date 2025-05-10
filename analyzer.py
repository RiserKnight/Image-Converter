#!/usr/bin/env python3

from pathlib import Path


def analyze_files(input_dir: Path):
    """
    Walks through the input_dir recursively, finds all .heic files,
    and returns a list of dictionaries with:
      - 'path': the Path to the file
      - 'size_mb': file size in megabytes (float)
    """
    file_info = []
    for file in input_dir.rglob('*'):
        if file.is_file() and file.suffix.lower() == '.heic':
            try:
                size_bytes = file.stat().st_size
            except (OSError, IOError) as e:
                print(f"⚠️ Could not access {file}: {e}")
                continue
            size_mb = size_bytes / (1024 * 1024)
            file_info.append({'path': file, 'size_mb': size_mb})
    return file_info
