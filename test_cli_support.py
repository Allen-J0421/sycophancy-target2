import unittest

from cli_support import ConsoleIO, parse_positive_int


class ConsoleIOTests(unittest.TestCase):
    def test_ask_and_say_use_injected_callables(self) -> None:
        prompts: list[str] = []
        outputs: list[str] = []
        io = ConsoleIO(
            input_fn=lambda prompt: prompts.append(prompt) or "ok",
            output_fn=outputs.append,
        )

        self.assertEqual(io.ask("name? "), "ok")
        io.say("hello")

        self.assertEqual(prompts, ["name? "])
        self.assertEqual(outputs, ["hello"])

    def test_parse_positive_int(self) -> None:
        self.assertEqual(parse_positive_int("42"), 42)
        self.assertIsNone(parse_positive_int("abc"))
        self.assertIsNone(parse_positive_int(""))


if __name__ == "__main__":
    unittest.main()
