import unittest

import todo_shell
from test_support import ScriptIO


class TodoShellTests(unittest.TestCase):
    def test_mark_done_without_index_shows_usage(self) -> None:
        io = ScriptIO([])
        items = ["milk"]

        todo_shell.mark_done(items, None, io.write)

        self.assertEqual(items, ["milk"])
        self.assertEqual(io.outputs, ["Usage: done <number from list>\n"])

    def test_run_processes_commands(self) -> None:
        io = ScriptIO(["add milk", "list", "done 1", "quit"])
        todo_shell.run_shell(
            input_fn=io,
            output_fn=io.write,
        )

        self.assertEqual(
            io.outputs,
            [
                "Commands: add <text> | list | done <n> | quit\n",
                "Added item #1.\n",
                "  1. milk",
                "",
                "Removed: milk\n",
                "Goodbye.\n",
            ],
        )
        self.assertEqual(
            io.prompts,
            ["todo> ", "todo> ", "todo> ", "todo> "],
        )


if __name__ == "__main__":
    unittest.main()
