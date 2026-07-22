#!/usr/bin/env python3

# Usage:
#   1. Pipe a blob:        echo '{"key":"val"}' | python3 format_json.py
#   2. Paste interactively (prompts you, end with Ctrl+D):  python3 format_json.py
#   3. File(s):            python3 format_json.py input.json
#
# Options:
#   -o, --output FILE    Write output to FILE (single input only)
#   -i, --indent N       Indentation spaces (default: 2)
#   --in-place           Overwrite input file(s)

import json
import sys
import argparse
from pathlib import Path


def process(text, output_path=None, indent=2):
    data = json.loads(text, strict=False)
    formatted = json.dumps(data, indent=indent, ensure_ascii=False)
    formatted = formatted.replace('\\n', '\n').replace('\\t', '\t')

    if output_path:
        Path(output_path).write_text(formatted + "\n", encoding="utf-8")
        print(f"Written to {output_path}")
    else:
        print(formatted)


def main():
    parser = argparse.ArgumentParser(
        description="Beautify JSON files and unescape \\n and \\t sequences."
    )
    parser.add_argument("files", nargs="*", help="Input JSON file(s); omit to read from stdin")
    parser.add_argument("-o", "--output", help="Output file (only valid for a single input file)")
    parser.add_argument("-i", "--indent", type=int, default=2, help="Indentation spaces (default: 2)")
    parser.add_argument("--in-place", action="store_true", help="Overwrite input file(s)")
    args = parser.parse_args()

    if args.output and len(args.files) > 1:
        print("Error: --output can only be used with a single input file.", file=sys.stderr)
        sys.exit(1)

    if not args.files:
        if sys.stdin.isatty():
            print("Reading JSON (paste below, then press Ctrl+D):", file=sys.stderr)
        text = sys.stdin.read()
        process(text, output_path=args.output, indent=args.indent)
        return

    for path in args.files:
        text = Path(path).read_text(encoding="utf-8")
        out = path if args.in_place else args.output
        process(text, output_path=out, indent=args.indent)


if __name__ == "__main__":
    main()
