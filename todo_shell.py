#!/usr/bin/env python3
"""Tiny interactive todo list: add, list, done, quit."""

from __future__ import annotations

COMMANDS_HELP = "Commands: add <text> | list | done <n> | quit\n"


def parse_command(line: str) -> tuple[str, str]:
    cmd, _, arg = line.partition(" ")
    return cmd.lower(), arg.strip()


def add_item(items: list[str], text: str) -> str:
    if not text:
        return "Usage: add <text>"

    items.append(text)
    return f"Added item #{len(items)}."


def format_items(items: list[str]) -> str:
    if not items:
        return "(empty)"

    return "\n".join(f"  {index}. {text}" for index, text in enumerate(items, start=1))


def complete_item(items: list[str], item_number: str) -> str:
    if not item_number.isdigit():
        return "Usage: done <number from list>"

    index = int(item_number) - 1
    if index < 0 or index >= len(items):
        return "That line number does not exist."

    removed = items.pop(index)
    return f"Removed: {removed}"


def run_command(items: list[str], line: str) -> tuple[bool, str]:
    cmd, arg = parse_command(line)

    if cmd == "quit":
        return False, "Goodbye."
    if cmd == "add":
        return True, add_item(items, arg)
    if cmd == "list":
        return True, format_items(items)
    if cmd == "done":
        return True, complete_item(items, arg)

    return True, "Unknown command."


def main() -> None:
    items: list[str] = []
    print(COMMANDS_HELP)

    while True:
        line = input("todo> ").strip()
        if not line:
            continue

        should_continue, message = run_command(items, line)
        print(f"{message}\n")
        if not should_continue:
            break


if __name__ == "__main__":
    main()
