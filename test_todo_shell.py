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


if __name__ == "__main__":
    unittest.main()

