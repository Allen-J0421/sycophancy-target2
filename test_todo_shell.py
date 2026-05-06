import unittest

import todo_shell


class TodoShellTests(unittest.TestCase):
    def test_run_processes_commands(self) -> None:
        inputs = iter(["add milk", "list", "done 1", "quit"])
        outputs: list[str] = []
        todo_shell.run_shell(
            input_fn=lambda prompt: next(inputs),
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
