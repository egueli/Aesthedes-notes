#!/usr/bin/env python3
"""Generate a C-style keycode array from a YAML keycodes list.

The input YAML is expected to look like:

keycodes:
  - id: 4
    command: 0x0d4d
    led: null
    description: null
  - id: 12
    command: 0x09c5
    led: [0x14, 0x4015, 0x4013, 0x4012]
    description: "X"

Only entries whose description is null are kept, and the output matches the
style used by the existing MAME table:

static const uint16_t keycode_table[] = {
    4, // command: 0x0d4d
    5, // command: 0x0d51
    ...
};
"""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError as exc:  # pragma: no cover - runtime dependency check
    raise SystemExit(
        "PyYAML is required. Install it with: python3 -m pip install pyyaml"
    ) from exc


def load_keycodes(path: Path) -> list[dict[str, Any]]:
    with path.open("r", encoding="utf-8") as fh:
        doc = yaml.safe_load(fh) or {}

    if not isinstance(doc, dict):
        raise ValueError("YAML root must be a mapping")

    entries = doc.get("keycodes", [])
    if not isinstance(entries, list):
        raise ValueError("YAML 'keycodes' entry must be a list")

    return entries


def build_c_array(entries: list[dict[str, Any]]) -> str:
    lines = ["static const uint16_t keycode_table[] = {"]

    for entry in entries:
        if entry.get("description") is not None:
            continue

        keycode = int(entry["id"])
        command = int(entry["command"], 0) if isinstance(entry["command"], str) else int(entry["command"])
        lines.append(f"    {keycode}, // command: {command:#06x}")

    lines.append("};")
    return "\n".join(lines) + "\n"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Read a YAML keycodes file and emit a C-style array containing only "
            "entries whose description is null."
        )
    )
    parser.add_argument("input", type=Path, help="Path to the YAML input file")
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        help="Optional output file. Defaults to stdout.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    entries = load_keycodes(args.input)
    output = build_c_array(entries)

    if args.output is not None:
        args.output.write_text(output, encoding="utf-8")
    else:
        print(output, end="")


if __name__ == "__main__":
    main()
