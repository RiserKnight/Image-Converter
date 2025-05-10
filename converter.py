#!/usr/bin/env python3

import os
from pathlib import Path
from pillow_heif import register_heif_opener
from PIL import Image

def perform_conversions(buckets, chosen_map, file_to_bucket, input_dir: Path, output_dir: Path):
    """
    Convert HEIC files based on user-chosen strategies for each bucket.

    :param buckets: list of bucket dicts
    :param chosen_map: dict mapping bucket_index to strategy_index
    :param file_to_bucket: dict mapping Path to bucket_index
    :param input_dir: Path to the input directory (used for structure)
    :param output_dir: Path to the output directory
    """
    # Register the HEIC opener for Pillow
    register_heif_opener()

    # Determine common base directory to preserve structure
    all_paths = list(file_to_bucket.keys())
    try:
        common_base = Path(os.path.commonpath([str(p) for p in all_paths]))
    except ValueError:
        # Fallback to input_dir if common path cannot be determined
        common_base = input_dir

    for file_path, bucket_idx in file_to_bucket.items():
        bucket = buckets[bucket_idx]
        strat_idx = chosen_map.get(bucket_idx)
        if strat_idx is None:
            # Skip if no strategy chosen for this bucket
            continue
        strat = bucket['strategies'][strat_idx]

        # Compute destination path, preserving subdirectories under input_dir
        try:
            rel_path = file_path.relative_to(common_base).with_suffix('.jpg')
        except ValueError:
            # If file_path isn't under common_base, use its name only
            rel_path = file_path.name
        dst_path = output_dir / rel_path
        dst_path.parent.mkdir(parents=True, exist_ok=True)

        # Remove existing file if it exists
        if dst_path.exists():
            dst_path.unlink()

        # Perform conversion
        try:
            with Image.open(file_path) as img:
                # Drop alpha if present
                if img.mode in ("RGBA", "LA") or (img.mode == "P" and "transparency" in img.info):
                    bg = Image.new("RGB", img.size, (255, 255, 255))
                    bg.paste(img, mask=img.split()[-1])
                    img = bg
                else:
                    img = img.convert("RGB")

                img.save(
                    dst_path,
                    format="JPEG",
                    quality=strat['quality'],
                    subsampling=strat['subsampling'],
                    optimize=strat['optimize']
                )
            print(f"✔ Converted: {file_path} → {dst_path} using {strat['label']}")
        except Exception as e:
            print(f"❌ Error converting {file_path}: {e}")
