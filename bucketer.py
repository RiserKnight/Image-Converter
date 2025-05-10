#!/usr/bin/env python3

import io
from pathlib import Path
from pillow_heif import register_heif_opener
from PIL import Image

def generate_buckets_and_strategies(file_info):
    """
    Cluster HEIC files into dynamic size buckets and generate 5 conversion strategies per bucket,
    estimating actual output sizes by sampling a representative file.

    :param file_info: list of dicts {'path': Path, 'size_mb': float}
    :return: (buckets, file_to_bucket) where
             buckets: list of dicts {
                 'max_size_mb': float,
                 'files': [Path, ...],
                 'strategies': [
                     {
                         'label': str,
                         'quality': int,
                         'subsampling': int,
                         'optimize': bool,
                         'estimated_size_mb': float
                     }, ...
                 ]
             }
             file_to_bucket: { Path: bucket_index, ... }
    """
    # No files => no buckets
    if not file_info:
        return [], {}

    # Extract unique sorted sizes (rounded)
    sizes = sorted({round(info['size_mb'], 2) for info in file_info})

    # Determine dynamic gap threshold to get <=20 buckets
    gap = 0.5
    max_buckets = 20
    buckets_ranges = []
    while True:
        buckets_ranges = []
        current = [sizes[0]]
        for sz in sizes[1:]:
            if sz - current[-1] <= gap:
                current.append(sz)
            else:
                buckets_ranges.append(current)
                current = [sz]
        buckets_ranges.append(current)
        if len(buckets_ranges) <= max_buckets or gap >= sizes[-1]:
            break
        gap += 0.5

    # Initialize buckets
    buckets = []
    for group in buckets_ranges:
        max_sz = round(group[-1], 2)
        buckets.append({
            'max_size_mb': max_sz,
            'files': [],
            'strategies': []
        })

    # Map files into buckets
    file_to_bucket = {}
    for info in file_info:
        sz = round(info['size_mb'], 2)
        path = info['path']
        for idx, bucket in enumerate(buckets):
            if sz <= bucket['max_size_mb']:
                bucket['files'].append(path)
                file_to_bucket[path] = idx
                break

    # Prepare for estimation
    register_heif_opener()

    def estimate_size(file_path, quality, subsampling, optimize):
        """
        Save file_path to an in-memory buffer with given JPEG settings and return size in MB.
        """
        with Image.open(file_path) as img:
            # Handle alpha
            if img.mode in ("RGBA", "LA") or (img.mode == "P" and "transparency" in img.info):
                bg = Image.new("RGB", img.size, (255, 255, 255))
                bg.paste(img, mask=img.split()[-1])
                img = bg
            else:
                img = img.convert("RGB")

            buffer = io.BytesIO()
            img.save(
                buffer,
                format="JPEG",
                quality=quality,
                subsampling=subsampling,
                optimize=optimize
            )
            size_mb = round(buffer.tell() / (1024 * 1024), 2)
        return size_mb

    # Define strategy templates
    base_strategies = [
        ('Ultra-Fidelity',  98, 0,  True,'Nearly lossless—largest size, minimal artifacts'),
        ('High-Fidelity',   95, 0,  True,'Very high quality with slight compression'),
        ('Balanced',        90, 1,  True,'Good tradeoff of size and detail'),
        ('Size-Saver',      85, 2,  True,'Smaller files with modest softening'),
        ('Ultra-Saver',     80, 2,  True,'Maximum compression—noticeable softness'),
    ]

    # Estimate for each bucket
    for bucket in buckets:
        if not bucket['files']:
            continue
        # Choose the largest file in this bucket as representative
        rep_file = max(bucket['files'], key=lambda p: p.stat().st_size)
        strategies = []
        for label, quality, subsampling, optimize, desc in base_strategies:
            est = estimate_size(rep_file, quality, subsampling, optimize)
            strategies.append({
            'label':              label,
            'quality':            quality,
            'subsampling':        subsampling,
            'optimize':           optimize,
            'estimated_size_mb':  est,
            'description':        desc
            })
        bucket['strategies'] = strategies

    return buckets, file_to_bucket
