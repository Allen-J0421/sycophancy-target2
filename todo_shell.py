#!/usr/bin/env python3
"""Tiny interactive todo list: add, list, done, quit."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass, field

Command = tuple[str, str]
CommandHandler = Callable[["TodoList", str], None]

HELP_TEXT = "Commands: add <text> | list | done <n> | quit\n"
PROMPT = "todo> "
COMMAND_ADD = "add"
COMMAND_LIST = "list"
COMMAND_DONE = "done"
COMMAND_QUIT = "quit"
QUIT_COMMANDS = {COMMAND_QUIT}
USAGE_ADD = "Usage: add <text>\n"
USAGE_DONE = "Usage: done <number from list>\n"
UNKNOWN_COMMAND = "Unknown command.\n"
BAD_LINE_NUMBER = "That line number does not exist.\n"


@dataclass
class TodoList:
    items: list[str] = field(default_factory=list)

    def add(self, text: str) -> int:
        self.items.append(text)
        return len(self.items)

    def has_index(self, index: int) -> bool:
        return 0 <= index < len(self.items)

    def complete(self, index: int) -> str:
        if not self.has_index(index):
            raise IndexError("todo item index out of range")
        return self.items.pop(index)


def parse_command(line: str) -> Command | None:
    stripped = line.strip()
    if not stripped:
        return None

    command, _, argument = stripped.partition(" ")
    return command.lower(), argument.strip()


def format_items(todo: TodoList) -> str:
    if not todo.items:
        return "(empty)\n"

    lines = [f"  {index}. {text}" for index, text in enumerate(todo.items, start=1)]
    return "\n".join(lines) + "\n"


def print_items(todo: TodoList) -> None:
    print(format_items(todo))


def add_item(todo: TodoList, text: str) -> None:
    if not text:
        print(USAGE_ADD)
        return

    item_number = todo.add(text)
    print(f"Added item #{item_number}.\n")


def parse_item_number(number: str) -> int | None:
    stripped = number.strip()
    if not stripped.isdigit():
        return None
    return int(stripped) - 1


def item_index(number: str) -> int | None:
    return parse_item_number(number)


def complete_item(todo: TodoList, number: str) -> None:
    index = parse_item_number(number)
    if index is None:
        print(USAGE_DONE)
        return

    if not todo.has_index(index):
        print(BAD_LINE_NUMBER)
        return

    removed = todo.complete(index)
    print(f"Removed: {removed}\n")


def handle_list(todo: TodoList, _argument: str) -> None:
    print_items(todo)


COMMAND_HANDLERS: dict[str, CommandHandler] = {
    COMMAND_ADD: add_item,
    COMMAND_LIST: handle_list,
    COMMAND_DONE: complete_item,
}


def handle_command(todo: TodoList, command: str, argument: str) -> bool:
    if command in QUIT_COMMANDS:
        print("Goodbye.\n")
        return False

    handler = COMMAND_HANDLERS.get(command)
    if handler is None:
        print(UNKNOWN_COMMAND)
    else:
        handler(todo, argument)

    return True


def main() -> None:
    todo = TodoList()
    print(HELP_TEXT)

    while True:
        parsed = parse_command(input(PROMPT))
        if parsed is None:
            continue

        command, argument = parsed
        if not handle_command(todo, command, argument):
            break


if __name__ == "__main__":
    main()
