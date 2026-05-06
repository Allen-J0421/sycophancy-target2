#!/usr/bin/env python3
"""Tiny interactive todo list: add, list, done, quit."""

from __future__ import annotations

COMMANDS_HELP = "Commands: add <text> | list | done <n> | quit\n"


def parse_command(line: str) -> tuple[str, str]:
    cmd, _, arg = line.partition(" ")
    return cmd.lower(), arg.strip()


def add_item(items: list[str], text: str) -> None:
    if not text:
        print("Usage: add <text>\n")
        return

    items.append(text)
    print(f"Added item #{len(items)}.\n")


def list_items(items: list[str]) -> None:
    if not items:
        print("(empty)\n")
        return

    for index, text in enumerate(items, start=1):
        print(f"  {index}. {text}")
    print()


def complete_item(items: list[str], item_number: str) -> None:
    if not item_number.isdigit():
        print("Usage: done <number from list>\n")
        return

    index = int(item_number) - 1
    if index < 0 or index >= len(items):
        print("That line number does not exist.\n")
        return

    removed = items.pop(index)
    print(f"Removed: {removed}\n")


def main() -> None:
    items: list[str] = []
    print(COMMANDS_HELP)

    while True:
        line = input("todo> ").strip()
        if not line:
            continue

        cmd, arg = parse_command(line)

        if cmd == "quit":
            print("Goodbye.\n")
            break

        if cmd == "add":
            add_item(items, arg)
            continue

        if cmd == "list":
            list_items(items)
            continue

        if cmd == "done":
            complete_item(items, arg)
            continue

        print("Unknown command.\n")


if __name__ == "__main__":
    main()
