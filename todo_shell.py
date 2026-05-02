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


def add_item(items: list[str], text: str) -> None:
    items.append(text)
    say(f"Added item #{len(items)}.")


def run_text_command(
    items: list[str],
    argument: str | None,
    usage_text: str,
    action: Callable[[list[str], str], None],
) -> bool:
    argument, error = require_argument(argument, usage_text)
    if error is not None:
        say(error)
        return True

    action(items, argument)
    return True


def list_items(items: list[str]) -> None:
    for line in format_items(items):
        print(line)
    print()


def format_items(items: list[str]) -> list[str]:
    if not items:
        return ["(empty)"]

    return [f"  {i}. {text}" for i, text in enumerate(items, start=1)]


def remove_item(items: list[str], raw_index: str) -> None:
    index, error = parse_list_index(
        raw_index,
        len(items),
        usage_text=DONE_USAGE,
    )
    if error is not None:
        say(error)
        return

    removed = items.pop(index - 1)
    say(f"Removed: {removed}")


def handle_quit(_items: list[str], _argument: str | None) -> bool:
    say("Goodbye.")
    return False


def handle_add(items: list[str], argument: str | None) -> bool:
    return run_text_command(items, argument, ADD_USAGE, add_item)


def handle_list(items: list[str], _argument: str | None) -> bool:
    list_items(items)
    return True


def handle_done(items: list[str], argument: str | None) -> bool:
    return run_text_command(items, argument, DONE_USAGE, remove_item)


CommandHandler = Callable[[list[str], str | None], bool]
COMMAND_HANDLERS: dict[str, CommandHandler] = {
    "quit": handle_quit,
    "add": handle_add,
    "list": handle_list,
    "done": handle_done,
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
