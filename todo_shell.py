#!/usr/bin/env python3
"""Tiny interactive todo list: add, list, done, quit."""

from __future__ import annotations

Command = tuple[str, str]


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


def complete_item(items: list[str], number: str) -> None:
    if not number.isdigit():
        print("Usage: done <number from list>\n")
        return

    index = int(number) - 1
    if index < 0 or index >= len(items):
        print("That line number does not exist.\n")
        return

    removed = items.pop(index)
    print(f"Removed: {removed}\n")


def main() -> None:
    items: list[str] = []
    print("Commands: add <text> | list | done <n> | quit\n")

    while True:
        parsed = parse_command(input("todo> "))
        if parsed is None:
            continue

        command, argument = parsed

        if command == "quit":
            print("Goodbye.\n")
            break

        if command == "add":
            add_item(items, argument)
            continue

        if command == "list":
            print_items(items)
            continue

        if command == "done":
            complete_item(items, argument)
            continue

        print("Unknown command.\n")


if __name__ == "__main__":
    main()
