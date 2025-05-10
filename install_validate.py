#!/usr/bin/env python3

import sys
import subprocess
from pathlib import Path

def install_and_validate(input_dir: Path, output_dir: Path):
    """
    Ensures required Python packages are installed,
    verifies input_dir exists, and creates output_dir if needed.
    """
    # Required modules and their pip package names
    required = {
        'Pillow': 'Pillow',
        'pillow_heif': 'pillow-heif',
    }
    for module_name, pkg_name in required.items():
        try:
            __import__(module_name)
        except ImportError:
            print(f"📦 {pkg_name!r} not found. Installing...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", pkg_name])

    # Verify input directory exists
    if not input_dir.is_dir():
        print(f"Error: Input directory {input_dir!r} does not exist or is not a directory.")
        sys.exit(1)

    # Create output directory if missing
    output_dir.mkdir(parents=True, exist_ok=True)
