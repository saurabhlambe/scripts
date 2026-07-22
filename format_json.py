#!/usr/bin/env python3
"""
Beautify JSON and expand escape sequences in string values.

Usage:
    1. Pipe a blob:             echo '{"key":"val"}' | python3 format_json.py
    2. Paste interactively      python3 format_json.py
       (end input with Ctrl+D):
    3. File(s):                 python3 format_json.py input.json

Options:
    -o, --output FILE    Write output to FILE (single input only)
    -i, --indent N       Indentation spaces (default: 2)
    --in-place           Overwrite input file(s)
"""

import argparse
import json
import sys
from pathlib import Path


def process(text, output_path=None, indent=2):
    """Parse, beautify, and unescape a JSON string."""
    data = json.loads(text, strict=False)
    formatted = json.dumps(data, indent=indent, ensure_ascii=False)
    formatted = formatted.replace("\\n", "\n").replace("\\t", "\t")

    if output_path:
        Path(output_path).write_text(formatted + "\n", encoding="utf-8")
        print(f"Written to {output_path}")
    else:
        print(formatted)


def main():
    """Entry point for the format_json CLI."""
    parser = argparse.ArgumentParser(
        description="Beautify JSON and expand \\n and \\t sequences."
    )
    parser.add_argument(
        "files",
        nargs="*",
        help="Input JSON file(s); omit to read from stdin",
    )
    parser.add_argument(
        "-o", "--output",
        help="Output file (only valid for a single input file)",
    )
    parser.add_argument(
        "-i", "--indent",
        type=int,
        default=2,
        help="Indentation spaces (default: 2)",
    )
    parser.add_argument(
        "--in-place",
        action="store_true",
        help="Overwrite input file(s)",
    )
    args = parser.parse_args()

    if args.output and len(args.files) > 1:
        print(
            "Error: --output can only be used with a single input file.",
            file=sys.stderr,
        )
        sys.exit(1)

    if not args.files:
        if sys.stdin.isatty():
            print(
                "Reading JSON (paste below, then press Ctrl+D):",
                file=sys.stderr,
            )
        text = sys.stdin.read()
        process(text, output_path=args.output, indent=args.indent)
        return

    for path in args.files:
        text = Path(path).read_text(encoding="utf-8")
        out = path if args.in_place else args.output
        process(text, output_path=out, indent=args.indent)


if __name__ == "__main__":
    main()
