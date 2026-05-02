#!/usr/bin/env python3
"""Tiny interactive todo list: add, list, done, quit."""

from __future__ import annotations

from typing import Callable

from cli_utils import (
    parse_command_line,
    parse_list_index,
    prompt_line,
    require_argument,
    say,
)

HELP_TEXT = "Commands: add <text> | list | done <n> | quit"
ADD_USAGE = "Usage: add <text>"
DONE_USAGE = "Usage: done <number from list>"


CommandHandler = Callable[[list[str], str | None], bool]


def handle_add(items: list[str], argument: str | None) -> bool:
    argument, error = require_argument(argument, ADD_USAGE)
    if error is not None:
        say(error)
        return True

    items.append(argument)
    say(f"Added item #{len(items)}.")
    return True


def handle_done(items: list[str], argument: str | None) -> bool:
    argument, error = require_argument(argument, DONE_USAGE)
    if error is not None:
        say(error)
        return True

    index, error = parse_list_index(
        argument,
        len(items),
        usage_text=DONE_USAGE,
    )
    if error is not None:
        say(error)
        return True

    removed = items.pop(index - 1)
    say(f"Removed: {removed}")
    return True


def list_items(items: list[str]) -> None:
    for line in format_items(items):
        print(line)
    print()


def format_items(items: list[str]) -> list[str]:
    if not items:
        return ["(empty)"]

    return [f"  {i}. {text}" for i, text in enumerate(items, start=1)]


def handle_quit(_items: list[str], _argument: str | None) -> bool:
    say("Goodbye.")
    return False


def handle_list(items: list[str], _argument: str | None) -> bool:
    list_items(items)
    return True


COMMAND_HANDLERS: dict[str, CommandHandler] = {
    "add": handle_add,
    "done": handle_done,
    "quit": handle_quit,
    "list": handle_list,
}


def handle_command(items: list[str], line: str) -> bool:
    command, argument = parse_command_line(line)

    handler = COMMAND_HANDLERS.get(command)
    if handler is None:
        say("Unknown command.")
        return True

    return handler(items, argument)


def main() -> None:
    items: list[str] = []
    say(HELP_TEXT)

    while True:
        line = prompt_line("todo> ")
        if not line:
            continue

        if not handle_command(items, line):
            break


if __name__ == "__main__":
    main()
