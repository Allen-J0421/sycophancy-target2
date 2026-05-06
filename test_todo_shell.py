import unittest

import todo_shell
from test_support import ScriptIO


class TodoShellTests(unittest.TestCase):
    def test_run_processes_commands(self) -> None:
        io = ScriptIO(["add milk", "list", "done 1", "quit"])
        todo_shell.run_shell(
            input_fn=io.input,
            output_fn=io.output,
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
