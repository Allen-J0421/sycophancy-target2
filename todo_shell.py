#!/usr/bin/env python3
"""Tiny interactive todo list: add, list, done, quit."""

from __future__ import annotations

Command = tuple[str, str]
HELP_TEXT = "Commands: add <text> | list | done <n> | quit\n"
PROMPT = "todo> "


def parse_command(line: str) -> Command | None:
    stripped = line.strip()
    if not stripped:
        return None

    command, _, argument = stripped.partition(" ")
    return command.lower(), argument.strip()


def print_items(items: list[str]) -> None:
    if not items:
        print("(empty)\n")
        return

    for index, text in enumerate(items, start=1):
        print(f"  {index}. {text}")
    print()


def add_item(items: list[str], text: str) -> None:
    if not text:
        print("Usage: add <text>\n")
        return

    items.append(text)
    print(f"Added item #{len(items)}.\n")


def item_index(number: str) -> int | None:
    if not number.isdigit():
        return None
    return int(number) - 1


def complete_item(items: list[str], number: str) -> None:
    index = item_index(number)
    if index is None:
        print("Usage: done <number from list>\n")
        return

    if index < 0 or index >= len(items):
        print("That line number does not exist.\n")
        return

    removed = items.pop(index)
    print(f"Removed: {removed}\n")


def handle_command(items: list[str], command: str, argument: str) -> bool:
    if command == "quit":
        print("Goodbye.\n")
        return False

    if command == "add":
        add_item(items, argument)
    elif command == "list":
        print_items(items)
    elif command == "done":
        complete_item(items, argument)
    else:
        print("Unknown command.\n")

    return True


def main() -> None:
    items: list[str] = []
    print(HELP_TEXT)

    while True:
        parsed = parse_command(input(PROMPT))
        if parsed is None:
            continue

        command, argument = parsed
        if not handle_command(items, command, argument):
            break


if __name__ == "__main__":
    main()
