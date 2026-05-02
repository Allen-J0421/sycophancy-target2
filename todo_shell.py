#!/usr/bin/env python3
"""Tiny interactive todo list: add, list, done, quit."""

from __future__ import annotations


HELP_TEXT = "Commands: add <text> | list | done <n> | quit\n"


def show_help() -> None:
    print(HELP_TEXT)


def parse_command(line: str) -> tuple[str, str | None]:
    parts = line.split(maxsplit=1)
    command = parts[0].lower()
    argument = parts[1] if len(parts) > 1 else None
    return command, argument


def add_item(items: list[str], text: str) -> None:
    items.append(text)
    print(f"Added item #{len(items)}.\n")


def list_items(items: list[str]) -> None:
    if not items:
        print("(empty)\n")
        return

    for i, text in enumerate(items, start=1):
        print(f"  {i}. {text}")
    print()


def remove_item(items: list[str], raw_index: str) -> None:
    if not raw_index.isdigit():
        print("Usage: done <number from list>\n")
        return

    index = int(raw_index)
    if index < 1 or index > len(items):
        print("That line number does not exist.\n")
        return

    removed = items.pop(index - 1)
    print(f"Removed: {removed}\n")


def handle_command(items: list[str], line: str) -> bool:
    command, argument = parse_command(line)

    match command:
        case "quit":
            print("Goodbye.\n")
            return False
        case "add":
            if argument is None:
                print("Usage: add <text>\n")
                return True
            add_item(items, argument)
            return True
        case "list":
            list_items(items)
            return True
        case "done":
            if argument is None:
                print("Usage: done <number from list>\n")
                return True
            remove_item(items, argument)
            return True
        case _:
            print("Unknown command.\n")
            return True


def main() -> None:
    items: list[str] = []
    show_help()

    while True:
        line = input("todo> ").strip()
        if not line:
            continue

        if not handle_command(items, line):
            break


if __name__ == "__main__":
    main()
