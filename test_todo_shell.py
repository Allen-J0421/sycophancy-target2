import unittest

import todo_shell
from test_support import make_script_io


class TodoShellTests(unittest.TestCase):
    def test_run_processes_commands(self) -> None:
        input_fn, outputs = make_script_io(["add milk", "list", "done 1", "quit"])
        todo_shell.run_shell(
            input_fn=input_fn,
            output_fn=outputs.append,
        )

        self.assertEqual(
            outputs,
            [
                "Commands: add <text> | list | done <n> | quit\n",
                "Added item #1.\n",
                "  1. milk",
                "",
                "Removed: milk\n",
                "Goodbye.\n",
            ],
        )


if __name__ == "__main__":
    unittest.main()
