#!/usr/bin/env python3
"""Tiny interactive todo list: add, list, done, quit."""

from __future__ import annotations
from collections.abc import Callable


InputFn = Callable[[str], str]
OutputFn = Callable[[str], None]


def print_commands(output_fn: OutputFn = print) -> None:
    output_fn("Commands: add <text> | list | done <n> | quit\n")


def add_item(items: list[str], text: str, output_fn: OutputFn = print) -> None:
    items.append(text)
    output_fn(f"Added item #{len(items)}.\n")


def list_items(items: list[str], output_fn: OutputFn = print) -> None:
    if not items:
        output_fn("(empty)\n")
        return

    for index, text in enumerate(items, start=1):
        output_fn(f"  {index}. {text}")
    output_fn("")


def mark_done(
    items: list[str],
    raw_index: str,
    output_fn: OutputFn = print,
) -> None:
    if not raw_index.isdigit():
        output_fn("Usage: done <number from list>\n")
        return

    index = int(raw_index)
    if index < 1 or index > len(items):
        output_fn("That line number does not exist.\n")
        return

    removed = items.pop(index - 1)
    output_fn(f"Removed: {removed}\n")


def handle_command(
    line: str,
    items: list[str],
    output_fn: OutputFn = print,
) -> bool:
    parts = line.split(maxsplit=1)
    cmd = parts[0].lower()

    if cmd == "quit":
        output_fn("Goodbye.\n")
        return False

    if cmd == "add":
        if len(parts) < 2:
            output_fn("Usage: add <text>\n")
            return True
        add_item(items, parts[1], output_fn)
        return True

    if cmd == "list":
        list_items(items, output_fn)
        return True

    if cmd == "done":
        if len(parts) < 2:
            output_fn("Usage: done <number from list>\n")
            return True
        mark_done(items, parts[1], output_fn)
        return True

    output_fn("Unknown command.\n")
    return True


def run_shell(
    input_fn: InputFn = input,
    output_fn: OutputFn = print,
) -> None:
    items: list[str] = []
    print_commands(output_fn)

    while True:
        line = input_fn("todo> ").strip()
        if not line:
            continue

        if not handle_command(line, items, output_fn):
            break


def main() -> None:
    run_shell()


if __name__ == "__main__":
    main()
