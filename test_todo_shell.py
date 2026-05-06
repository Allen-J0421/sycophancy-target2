import unittest

from todo_shell import (
    CommandResult,
    ParsedCommand,
    TodoList,
    parse_command,
    run_command,
    run_shell,
)


class TodoShellTests(unittest.TestCase):
    def test_complete_item_removes_displayed_number(self) -> None:
        todo_list = TodoList(["alpha", "beta"])

        self.assertEqual(todo_list.complete("1"), "Removed: alpha")
        self.assertEqual(todo_list.items, ["beta"])

    def test_format_items_matches_display_numbers(self) -> None:
        self.assertEqual(TodoList().format(), "(empty)")
        self.assertEqual(TodoList(["alpha", "beta"]).format(), "  1. alpha\n  2. beta")

    def test_parse_command_splits_name_and_arg(self) -> None:
        self.assertEqual(
            parse_command("ADD alpha beta"),
            ParsedCommand("add", "alpha beta"),
        )
        self.assertEqual(parse_command("list"), ParsedCommand("list", ""))

    def test_run_command_dispatches_known_and_unknown_commands(self) -> None:
        todo_list = TodoList()

        self.assertEqual(
            run_command(todo_list, "add alpha"),
            CommandResult(True, "Added item #1."),
        )
        self.assertEqual(
            run_command(todo_list, "wat"),
            CommandResult(True, "Unknown command."),
        )
        self.assertEqual(
            run_command(todo_list, "quit"),
            CommandResult(False, "Goodbye."),
        )

    def test_run_shell_accepts_injected_io(self) -> None:
        commands = iter(["add alpha", "list", "quit"])
        prompts: list[str] = []
        output: list[str] = []

        def input_func(prompt: str) -> str:
            prompts.append(prompt)
            return next(commands)

        run_shell(input_func=input_func, output_func=output.append)

        self.assertEqual(prompts, ["todo> ", "todo> ", "todo> "])
        self.assertEqual(
            output,
            [
                "Commands: add <text> | list | done <n> | quit\n",
                "Added item #1.\n",
                "  1. alpha\n",
                "Goodbye.\n",
            ],
        )


if __name__ == "__main__":
    unittest.main()
