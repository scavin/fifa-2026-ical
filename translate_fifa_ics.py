#!/usr/bin/env python3
from __future__ import annotations

import sys

from fifa_ics_common import (
    TRANSLATABLE_PROPERTIES,
    build_argument_parser,
    read_source,
    translate_property_value,
)


def parse_args():
    parser = build_argument_parser(
        "Translate FIFA World Cup 2026 ICS team names into Chinese "
        "using lightweight field-level parsing."
    )
    return parser.parse_args()


def detect_newline(text: str) -> str:
    return "\r\n" if "\r\n" in text else "\n"


def unfold_ics(text: str) -> list[str]:
    physical_lines = text.splitlines()
    logical_lines: list[str] = []

    for line in physical_lines:
        if line.startswith((" ", "\t")) and logical_lines:
            logical_lines[-1] += line[1:]
        else:
            logical_lines.append(line)

    return logical_lines


def fold_ics_line(line: str, max_octets: int = 75) -> list[str]:
    if len(line.encode("utf-8")) <= max_octets:
        return [line]

    folded: list[str] = []
    prefix = ""
    current = ""

    for char in line:
        candidate = prefix + current + char
        if current and len(candidate.encode("utf-8")) > max_octets:
            folded.append(prefix + current)
            prefix = " "
            current = char
        else:
            current += char

    if current:
        folded.append(prefix + current)

    return folded


def translate_ics_content(ics_content: str) -> str:
    newline = detect_newline(ics_content)
    translated_lines: list[str] = []

    for line in unfold_ics(ics_content):
        if ":" not in line:
            translated_lines.extend(fold_ics_line(line))
            continue

        property_name, value = line.split(":", 1)
        base_name = property_name.split(";", 1)[0].upper()

        if base_name in TRANSLATABLE_PROPERTIES:
            line = f"{property_name}:{translate_property_value(property_name, value)}"

        translated_lines.extend(fold_ics_line(line))

    return newline.join(translated_lines) + newline


def main() -> int:
    args = parse_args()
    ics_content = read_source(args.input, args.url)

    translated = translate_ics_content(ics_content)
    args.output.write_text(translated, encoding="utf-8")
    print(f"Wrote translated ICS to {args.output}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
