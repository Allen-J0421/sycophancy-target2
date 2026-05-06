#!/usr/bin/env python3
"""Tiny interactive todo list: add, list, done, quit."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass, field

from cli_io import InputFunc, OutputFunc, write_message

COMMANDS_HELP = "Commands: add <text> | list | done <n> | quit\n"


def parse_command(line: str) -> tuple[str, str]:
    cmd, _, arg = line.partition(" ")
    return cmd.lower(), arg.strip()


@dataclass
class TodoList:
    items: list[str] = field(default_factory=list)

    def add(self, text: str) -> str:
        if not text:
            return "Usage: add <text>"

        self.items.append(text)
        return f"Added item #{len(self.items)}."

    def format(self) -> str:
        if not self.items:
            return "(empty)"

        return "\n".join(
            f"  {index}. {text}" for index, text in enumerate(self.items, start=1)
        )

    def complete(self, item_number: str) -> str:
        if not item_number.isdigit():
            return "Usage: done <number from list>"

        index = int(item_number) - 1
        if index < 0 or index >= len(self.items):
            return "That line number does not exist."

        removed = self.items.pop(index)
        return f"Removed: {removed}"


CommandHandler = Callable[[TodoList, str], tuple[bool, str]]


def handle_quit(_todo_list: TodoList, _arg: str) -> tuple[bool, str]:
    return False, "Goodbye."


def handle_add(todo_list: TodoList, arg: str) -> tuple[bool, str]:
    return True, todo_list.add(arg)


def handle_list(todo_list: TodoList, _arg: str) -> tuple[bool, str]:
    return True, todo_list.format()


def handle_done(todo_list: TodoList, arg: str) -> tuple[bool, str]:
    return True, todo_list.complete(arg)


COMMAND_HANDLERS: dict[str, CommandHandler] = {
    "quit": handle_quit,
    "add": handle_add,
    "list": handle_list,
    "done": handle_done,
}


def run_command(todo_list: TodoList, line: str) -> tuple[bool, str]:
    cmd, arg = parse_command(line)
    handler = COMMAND_HANDLERS.get(cmd)
    if handler is None:
        return True, "Unknown command."

    return handler(todo_list, arg)


def run_shell(
    input_func: InputFunc = input, output_func: OutputFunc = print
) -> None:
    todo_list = TodoList()
    output_func(COMMANDS_HELP)

    while True:
        line = input_func("todo> ").strip()
        if not line:
            continue

        should_continue, message = run_command(todo_list, line)
        write_message(output_func, message)
        if not should_continue:
            break


def main() -> None:
    run_shell()


if __name__ == "__main__":
    main()
