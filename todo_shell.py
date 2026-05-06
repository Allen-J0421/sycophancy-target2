#!/usr/bin/env python3
"""Tiny interactive todo list: add, list, done, quit."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass, field

from cli_io import InputFunc, OutputFunc, write_message

COMMANDS_HELP = "Commands: add <text> | list | done <n> | quit"


@dataclass(frozen=True)
class ParsedCommand:
    name: str
    arg: str


def parse_command(line: str) -> ParsedCommand:
    cmd, _, arg = line.partition(" ")
    return ParsedCommand(cmd.lower(), arg.strip())


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


@dataclass(frozen=True)
class CommandResult:
    should_continue: bool
    message: str

    @classmethod
    def continue_with(cls, message: str) -> CommandResult:
        return cls(True, message)

    @classmethod
    def stop_with(cls, message: str) -> CommandResult:
        return cls(False, message)


CommandHandler = Callable[[TodoList, str], CommandResult]


def handle_quit(_todo_list: TodoList, _arg: str) -> CommandResult:
    return CommandResult.stop_with("Goodbye.")


def handle_add(todo_list: TodoList, arg: str) -> CommandResult:
    return CommandResult.continue_with(todo_list.add(arg))


def handle_list(todo_list: TodoList, _arg: str) -> CommandResult:
    return CommandResult.continue_with(todo_list.format())


def handle_done(todo_list: TodoList, arg: str) -> CommandResult:
    return CommandResult.continue_with(todo_list.complete(arg))


COMMAND_HANDLERS: dict[str, CommandHandler] = {
    "quit": handle_quit,
    "add": handle_add,
    "list": handle_list,
    "done": handle_done,
}


def run_command(todo_list: TodoList, line: str) -> CommandResult:
    command = parse_command(line)
    handler = COMMAND_HANDLERS.get(command.name)
    if handler is None:
        return CommandResult.continue_with("Unknown command.")

    return handler(todo_list, command.arg)


def run_shell(
    input_func: InputFunc = input, output_func: OutputFunc = print
) -> None:
    todo_list = TodoList()
    write_message(output_func, COMMANDS_HELP)

    while True:
        line = input_func("todo> ").strip()
        if not line:
            continue

        result = run_command(todo_list, line)
        write_message(output_func, result.message)
        if not result.should_continue:
            break


def main() -> None:
    run_shell()


if __name__ == "__main__":
    main()
