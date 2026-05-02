#!/usr/bin/env python3
"""Tiny interactive todo list: add, list, done, quit."""

from __future__ import annotations


HELP_TEXT = "Commands: add <text> | list | done <n> | quit\n"
ADD_USAGE = "Usage: add <text>"
DONE_USAGE = "Usage: done <number from list>"


def say(message: str) -> None:
    print(message)
    print()


def show_help() -> None:
    say(HELP_TEXT.rstrip())


def parse_command(line: str) -> tuple[str, str | None]:
    parts = line.split(maxsplit=1)
    if not parts:
        return "", None

    command = parts[0].lower()
    argument = parts[1] if len(parts) > 1 else None
    return command, argument


def add_item(items: list[str], text: str) -> None:
    items.append(text)
    say(f"Added item #{len(items)}.")


def list_items(items: list[str]) -> None:
    if not items:
        say("(empty)")
        return

    for i, text in enumerate(items, start=1):
        print(f"  {i}. {text}")
    print()


def remove_item(items: list[str], raw_index: str) -> None:
    if not raw_index.isdigit():
        say(DONE_USAGE)
        return

    index = int(raw_index)
    if index < 1 or index > len(items):
        say("That line number does not exist.")
        return

    removed = items.pop(index - 1)
    say(f"Removed: {removed}")


def handle_command(items: list[str], line: str) -> bool:
    command, argument = parse_command(line)

    match command:
        case "quit":
            say("Goodbye.")
            return False
        case "add":
            if argument is None:
                say(ADD_USAGE)
                return True
            add_item(items, argument)
            return True
        case "list":
            list_items(items)
            return True
        case "done":
            if argument is None:
                say(DONE_USAGE)
                return True
            remove_item(items, argument)
            return True
        case _:
            say("Unknown command.")
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
