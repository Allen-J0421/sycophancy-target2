#!/usr/bin/env python3
"""Tiny interactive todo list: add, list, done, quit."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass, field

Command = tuple[str, str]
HELP_TEXT = "Commands: add <text> | list | done <n> | quit\n"
PROMPT = "todo> "
COMMAND_ADD = "add"
COMMAND_LIST = "list"
COMMAND_DONE = "done"
COMMAND_QUIT = "quit"
QUIT_COMMANDS = {COMMAND_QUIT}


@dataclass
class TodoList:
    items: list[str] = field(default_factory=list)

    def add(self, text: str) -> int:
        self.items.append(text)
        return len(self.items)

    def complete(self, index: int) -> str:
        return self.items.pop(index)

    def has_index(self, index: int) -> bool:
        return 0 <= index < len(self.items)


CommandHandler = Callable[[TodoList, str], None]


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
        print("Usage: add <text>\n")
        return

    item_number = todo.add(text)
    print(f"Added item #{item_number}.\n")


def item_index(number: str) -> int | None:
    if not number.isdigit():
        return None
    return int(number) - 1


def complete_item(todo: TodoList, number: str) -> None:
    index = item_index(number)
    if index is None:
        print("Usage: done <number from list>\n")
        return

    if not todo.has_index(index):
        print("That line number does not exist.\n")
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
        print("Unknown command.\n")
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
