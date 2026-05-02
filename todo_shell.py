#!/usr/bin/env python3
"""Tiny interactive todo list: add, list, done, quit."""

from __future__ import annotations

from collections.abc import Callable

Command = tuple[str, str]
CommandHandler = Callable[[list[str], str], None]
HELP_TEXT = "Commands: add <text> | list | done <n> | quit\n"
PROMPT = "todo> "
COMMAND_ADD = "add"
COMMAND_LIST = "list"
COMMAND_DONE = "done"
COMMAND_QUIT = "quit"
QUIT_COMMANDS = {COMMAND_QUIT}


def parse_command(line: str) -> Command | None:
    stripped = line.strip()
    if not stripped:
        return None

    command, _, argument = stripped.partition(" ")
    return command.lower(), argument.strip()


def format_items(items: list[str]) -> str:
    if not items:
        return "(empty)\n"

    lines = [f"  {index}. {text}" for index, text in enumerate(items, start=1)]
    return "\n".join(lines) + "\n"


def print_items(items: list[str]) -> None:
    print(format_items(items))


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


def handle_list(items: list[str], _argument: str) -> None:
    print_items(items)


COMMAND_HANDLERS: dict[str, CommandHandler] = {
    COMMAND_ADD: add_item,
    COMMAND_LIST: handle_list,
    COMMAND_DONE: complete_item,
}


def handle_command(items: list[str], command: str, argument: str) -> bool:
    if command in QUIT_COMMANDS:
        print("Goodbye.\n")
        return False

    handler = COMMAND_HANDLERS.get(command)
    if handler is None:
        print("Unknown command.\n")
    else:
        handler(items, argument)

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
