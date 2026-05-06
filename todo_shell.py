#!/usr/bin/env python3
"""Tiny interactive todo list: add, list, done, quit."""

from __future__ import annotations


def print_commands() -> None:
    print("Commands: add <text> | list | done <n> | quit\n")


def add_item(items: list[str], text: str) -> None:
    items.append(text)
    print(f"Added item #{len(items)}.\n")


def list_items(items: list[str]) -> None:
    if not items:
        print("(empty)\n")
        return

    for index, text in enumerate(items, start=1):
        print(f"  {index}. {text}")
    print()


def mark_done(items: list[str], raw_index: str) -> None:
    if not raw_index.isdigit():
        print("Usage: done <number from list>\n")
        return

    index = int(raw_index)
    if index < 1 or index > len(items):
        print("That line number does not exist.\n")
        return

    removed = items.pop(index - 1)
    print(f"Removed: {removed}\n")


def handle_command(line: str, items: list[str]) -> bool:
    parts = line.split(maxsplit=1)
    cmd = parts[0].lower()

    if cmd == "quit":
        print("Goodbye.\n")
        return False

    if cmd == "add":
        if len(parts) < 2:
            print("Usage: add <text>\n")
            return True
        add_item(items, parts[1])
        return True

    if cmd == "list":
        list_items(items)
        return True

    if cmd == "done":
        if len(parts) < 2:
            print("Usage: done <number from list>\n")
            return True
        mark_done(items, parts[1])
        return True

    print("Unknown command.\n")
    return True


def main() -> None:
    items: list[str] = []
    print_commands()

    while True:
        line = input("todo> ").strip()
        if not line:
            continue

        if not handle_command(line, items):
            break


if __name__ == "__main__":
    main()
