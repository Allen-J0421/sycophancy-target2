import unittest

import todo_shell


class TestTodoShell(unittest.TestCase):
    def test_parse_command(self) -> None:
        self.assertIsNone(todo_shell.parse_command(""))
        self.assertIsNone(todo_shell.parse_command("   "))

        cmd = todo_shell.parse_command("ADD buy milk")
        assert cmd is not None
        self.assertEqual(cmd.name, "add")
        self.assertEqual(cmd.arg, "buy milk")

        cmd = todo_shell.parse_command("list")
        assert cmd is not None
        self.assertEqual(cmd.name, "list")
        self.assertIsNone(cmd.arg)

    def test_todo_list_add_list_done(self) -> None:
        todos = todo_shell.TodoList()
        self.assertTrue(todos.is_empty())

        self.assertEqual(todos.add("a"), 1)
        self.assertEqual(todos.add("b"), 2)
        self.assertFalse(todos.is_empty())
        self.assertEqual(todos.list_lines(), ["  1. a", "  2. b"])

        removed = todos.done(2)
        self.assertEqual(removed, "b")
        self.assertEqual(todos.list_lines(), ["  1. a"])

    def test_todo_list_done_out_of_range(self) -> None:
        todos = todo_shell.TodoList()
        todos.add("only")
        with self.assertRaises(IndexError):
            todos.done(0)
        with self.assertRaises(IndexError):
            todos.done(2)

    def test_run_shell_injected_io(self) -> None:
        inputs = iter(
            [
                "add a",
                "add b",
                "list",
                "done 2",
                "list",
                "quit",
            ]
        )
        outputs: list[str] = []

        def input_fn(_prompt: str) -> str:
            return next(inputs)

        def output_fn(line: str) -> None:
            outputs.append(line)

        todo_shell.run_shell(input_fn=input_fn, output_fn=output_fn)

        self.assertIn("Added item #1.", outputs)
        self.assertIn("Added item #2.", outputs)
        self.assertIn("  1. a", outputs)
        self.assertIn("  2. b", outputs)
        self.assertIn("Removed: b", outputs)
        self.assertIn("Goodbye.", outputs)

    def test_run_shell_eof_exits_gracefully(self) -> None:
        outputs: list[str] = []

        def input_fn(_prompt: str) -> str:
            raise EOFError

        def output_fn(line: str) -> None:
            outputs.append(line)

        todo_shell.run_shell(input_fn=input_fn, output_fn=output_fn)
        self.assertIn("Goodbye.", outputs)


if __name__ == "__main__":
    unittest.main()
