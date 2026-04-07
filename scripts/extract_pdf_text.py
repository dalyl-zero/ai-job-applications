"""Extract text from a PDF file, with caching.

Usage:
    python scripts/extract_pdf_text.py path/to/file.pdf

Extracted text is cached in references/extracted/ keyed by filename + content hash.
Subsequent calls for the same unchanged file return the cached result.
"""

import os
import sys
import hashlib
from PyPDF2 import PdfReader

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CACHE_DIR = os.path.join(PROJECT_ROOT, "references", "extracted")


def _cache_path(pdf_path):
    """Return a cache file path based on filename + content hash."""
    os.makedirs(CACHE_DIR, exist_ok=True)
    base = os.path.splitext(os.path.basename(pdf_path))[0]
    with open(pdf_path, "rb") as f:
        file_hash = hashlib.md5(f.read()).hexdigest()[:8]
    return os.path.join(CACHE_DIR, f"{base}_{file_hash}.txt")


def extract_text(pdf_path):
    cache = _cache_path(pdf_path)

    if os.path.exists(cache):
        with open(cache, "r", encoding="utf-8") as f:
            return f.read()

    reader = PdfReader(pdf_path)
    text = []
    for page in reader.pages:
        content = page.extract_text()
        if content:
            text.append(content)
    result = "\n".join(text)

    with open(cache, "w", encoding="utf-8") as f:
        f.write(result)

    return result


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python scripts/extract_pdf_text.py path/to/file.pdf")
        sys.exit(1)

    print(extract_text(sys.argv[1]))
