"""Merge multiple PDF files into one.

Usage:
    python scripts/merge_pdfs.py file1.pdf file2.pdf ... [-o output.pdf]

Default output: misc/merged.pdf
"""

import os
import sys
from PyPDF2 import PdfMerger

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_OUTPUT_DIR = os.path.join(PROJECT_ROOT, "misc")
DEFAULT_OUTPUT = os.path.join(DEFAULT_OUTPUT_DIR, "merged.pdf")


def merge(paths, output=DEFAULT_OUTPUT):
    os.makedirs(os.path.dirname(output), exist_ok=True)
    merger = PdfMerger()
    merger.add_metadata({})
    for p in paths:
        if not os.path.isfile(p):
            print(f"Error: '{p}' not found.")
            sys.exit(1)
        merger.append(p)
    merger.write(output)
    merger.close()
    print(f"Merged {len(paths)} files → {output}")


if __name__ == "__main__":
    args = sys.argv[1:]
    if not args or args[0] in ("-h", "--help"):
        print(__doc__.strip())
        sys.exit(0)

    output = DEFAULT_OUTPUT
    if "-o" in args:
        idx = args.index("-o")
        output = args[idx + 1]
        args = args[:idx] + args[idx + 2:]

    merge(args, output)
