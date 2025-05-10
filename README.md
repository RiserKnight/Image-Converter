# Image-Converter

A command-line tool to recursively scan a folder of HEIC images, dynamically group them into size-based buckets, and interactively apply one of five JPEG conversion strategies per bucket.

## Features

- Automatic analysis of `.heic` files (including subfolders).
- Dynamic bucket clustering (max 20 buckets).
- Five built-in strategies per bucket with descriptions and estimated sizes:

  1. **Ultra-Fidelity** – nearly lossless
  2. **High-Fidelity** – very high quality
  3. **Balanced** – good quality/size tradeoff
  4. **Size-Saver** – smaller files, slight softening
  5. **Ultra-Saver** – maximum compression

- Interactive CLI prompts for strategy selection.
- Overwrites existing files and preserves folder structure.

## Installation

```bash
git clone https://github.com/RiserKnight/Image-Converter.git
cd Image-Converter
```

## Usage

```bash
python .\run.py "C:\Users\riser\OneDrive\Desktop\Input" "C:\Users\riser\OneDrive\Desktop\Output"
```

## License

RiserKnight Github
