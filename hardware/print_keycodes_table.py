#!/usr/bin/env python3
"""Print keyboard keycode-to-command mappings from a 16-bit table.

The input file is expected to contain 3500 big-endian unsigned 16-bit values.
Each index is the keycode, and entries equal to 0xFFFF are skipped.
"""

from __future__ import annotations

import argparse
from pathlib import Path

SKIP_VALUE = 0xFFFF


def read_keycode_table(path: Path) -> list[tuple[int, int]]:
    data = path.read_bytes()
    if len(data) % 2 != 0:
        raise ValueError(f"{path} length is not a multiple of 2 bytes")

    entries = len(data) // 2

    pairs: list[tuple[int, int]] = []
    for keycode in range(entries):
        value = int.from_bytes(
            data[keycode * 2 : (keycode + 1) * 2],
            byteorder="big",
            signed=False,
        )
        if value != SKIP_VALUE:
            pairs.append((keycode, value))

    return pairs


def uniquify_pairs(pairs: list[tuple[int, int]]) -> list[tuple[int, int]]:
    by_command: dict[int, int] = {}
    for keycode, command in pairs:
        existing = by_command.get(command)
        if existing is None or keycode < existing:
            by_command[command] = keycode

    return [
        (keycode, command)
        for command, keycode in sorted(by_command.items(), key=lambda item: item[1])
    ]


def sort_pairs(pairs: list[tuple[int, int]], *, by_command: bool) -> list[tuple[int, int]]:
    if by_command:
        return sorted(pairs, key=lambda pair: pair[1])
    return pairs


def print_csv(pairs: list[tuple[int, int]]) -> None:
    print("keycode,command")
    for keycode, command in pairs:
        print(f"{keycode},{command:#06x}")


def print_markdown(pairs: list[tuple[int, int]]) -> None:
    print("| keycode | command |")
    print("| ---: | ---: |")
    for keycode, command in pairs:
        print(f"| {keycode} | {command:#06x} |")


def print_c_array(pairs: list[tuple[int, int]]) -> None:
    print("static const uint16_t keycode_table[] = {")
    for keycode, command in pairs:
        print(f"    {keycode}, // command {command:#06x}")
    print("};")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Read a 16-bit keycode table and print non-0xFFFF mappings."
    )
    parser.add_argument(
        "path",
        nargs="?",
        default="keycodes_table.bin",
        help="Path to the binary file containing the 16-bit table",
    )
    parser.add_argument(
        "-f",
        "--format",
        choices=("csv", "markdown", "c"),
        default="csv",
        help="Output format: csv (default), markdown, or c",
    )
    parser.add_argument(
        "-u",
        "--uniquify",
        action="store_true",
        help="Discard duplicate command IDs, keeping only the lowest keycode for each command.",
    )
    parser.add_argument(
        "-s",
        "--sort",
        choices=("keycode", "command"),
        default="keycode",
        help="Sort output by keycode (default) or by command ID.",
    )
    args = parser.parse_args()

    table_path = Path(args.path)
    pairs = read_keycode_table(table_path)
    if args.uniquify:
        pairs = uniquify_pairs(pairs)
    pairs = sort_pairs(pairs, by_command=(args.sort == "command"))

    if args.format == "csv":
        print_csv(pairs)
    elif args.format == "markdown":
        print_markdown(pairs)
    else:
        print_c_array(pairs)


if __name__ == "__main__":
    main()
