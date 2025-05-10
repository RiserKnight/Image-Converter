#!/usr/bin/env python3
"""
run.py

Orchestrates the HEIC-to-JPEG batch conversion:
  1. install_and_validate()
  2. analyze_files()
  3. generate_buckets_and_strategies()
  4. prompt_user_for_strategies()
  5. perform_conversions()
"""

import sys
import argparse
from pathlib import Path

from install_validate import install_and_validate
from analyzer import analyze_files
from bucketer import generate_buckets_and_strategies
from prompter import prompt_user_for_strategies
from converter import perform_conversions


def main():
    parser = argparse.ArgumentParser(
        description="Batch convert HEIC images to JPEG using dynamic size buckets and user-selected strategies"
    )
    parser.add_argument(
        "input_folder", type=str,
        help="Path to folder containing .heic files"
    )
    parser.add_argument(
        "output_folder", type=str,
        help="Path to folder where converted .jpg files will be saved"
    )
    args = parser.parse_args()

    input_dir = Path(args.input_folder)
    output_dir = Path(args.output_folder)

    # Step 1: Install dependencies and validate directories
    install_and_validate(input_dir, output_dir)

    # Step 2: Analyze files
    file_info = analyze_files(input_dir)
    if not file_info:
        print(f"No .heic files found in {input_dir!r}. Exiting.")
        sys.exit(0)

    # Step 3: Generate buckets and strategies
    buckets, file_to_bucket = generate_buckets_and_strategies(file_info)

    # Step 4: Prompt user for strategy choices
    chosen_map = prompt_user_for_strategies(buckets)

    # Step 5: Perform conversions
    perform_conversions(buckets, chosen_map, file_to_bucket, input_dir, output_dir)

    print("✅ All done!")


if __name__ == "__main__":
    main()
