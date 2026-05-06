#!/usr/bin/env python3
"""Tiny interactive todo list: add, list, done, quit."""

from __future__ import annotations

from collections.abc import Callable

from cli_io import InputFunc, OutputFunc, write_message

COMMANDS_HELP = "Commands: add <text> | list | done <n> | quit\n"
CommandHandler = Callable[[list[str], str], tuple[bool, str]]


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


def handle_quit(_items: list[str], _arg: str) -> tuple[bool, str]:
    return False, "Goodbye."


def handle_add(items: list[str], arg: str) -> tuple[bool, str]:
    return True, add_item(items, arg)


def handle_list(items: list[str], _arg: str) -> tuple[bool, str]:
    return True, format_items(items)


def handle_done(items: list[str], arg: str) -> tuple[bool, str]:
    return True, complete_item(items, arg)


COMMAND_HANDLERS: dict[str, CommandHandler] = {
    "quit": handle_quit,
    "add": handle_add,
    "list": handle_list,
    "done": handle_done,
}


def run_command(items: list[str], line: str) -> tuple[bool, str]:
    cmd, arg = parse_command(line)
    handler = COMMAND_HANDLERS.get(cmd)
    if handler is None:
        return True, "Unknown command."

    return handler(items, arg)


def run_shell(
    input_func: InputFunc = input, output_func: OutputFunc = print
) -> None:
    items: list[str] = []
    output_func(COMMANDS_HELP)

    while True:
        line = input_func("todo> ").strip()
        if not line:
            continue

        should_continue, message = run_command(items, line)
        write_message(output_func, message)
        if not should_continue:
            break


def main() -> None:
    run_shell()


if __name__ == "__main__":
    main()
