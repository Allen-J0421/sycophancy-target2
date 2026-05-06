import unittest

from cli_io import read_prompt, write_message


class CliIoTests(unittest.TestCase):
    def test_read_prompt_strips_response(self) -> None:
        prompts: list[str] = []

        def input_func(prompt: str) -> str:
            prompts.append(prompt)
            return "  value  "

        self.assertEqual(read_prompt(input_func, "prompt> "), "value")
        self.assertEqual(prompts, ["prompt> "])

    def test_write_message_appends_blank_line_marker(self) -> None:
        output: list[str] = []

        write_message(output.append, "hello")

        self.assertEqual(output, ["hello\n"])


if __name__ == "__main__":
    unittest.main()
