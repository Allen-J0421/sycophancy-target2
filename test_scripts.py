import unittest

import guess_the_number
import todo_shell


class TodoShellTests(unittest.TestCase):
    def test_parse_command_normalizes_command_and_argument(self) -> None:
        self.assertEqual(todo_shell.parse_command("  ADD buy milk  "), ("add", "buy milk"))
        self.assertIsNone(todo_shell.parse_command("   "))

    def test_format_items_handles_empty_and_numbered_lists(self) -> None:
        todo = todo_shell.TodoList()
        self.assertEqual(todo_shell.format_items(todo), "(empty)\n")

        todo.add("buy milk")
        todo.add("write tests")
        self.assertEqual(
            todo_shell.format_items(todo),
            "  1. buy milk\n  2. write tests\n",
        )

    def test_parse_item_number_uses_one_based_numbers(self) -> None:
        self.assertEqual(todo_shell.parse_item_number(" 2 "), 1)
        self.assertEqual(todo_shell.item_index("1"), 0)
        self.assertIsNone(todo_shell.parse_item_number("two"))

    def test_complete_validates_index_before_removing(self) -> None:
        todo = todo_shell.TodoList(["first"])

        self.assertEqual(todo.complete(0), "first")
        with self.assertRaises(IndexError):
            todo.complete(0)


class GuessTheNumberTests(unittest.TestCase):
    def test_game_config_validation(self) -> None:
        with self.assertRaises(ValueError):
            guess_the_number.GameConfig(minimum=10, maximum=1)
        with self.assertRaises(ValueError):
            guess_the_number.GameConfig(max_tries=0)

    def test_messages_include_configured_bounds_and_tries(self) -> None:
        config = guess_the_number.GameConfig(minimum=3, maximum=9, max_tries=4)

        self.assertEqual(
            config.intro_message(),
            "Guess an integer from 3 to 9. You have 4 tries.\n",
        )
        self.assertEqual(
            config.out_of_range_message(),
            "Out of range; stay between 3 and 9.\n",
        )
        self.assertEqual(guess_the_number.prompt_for_guess(2), "Tries left: 2. Your guess: ")

    def test_parse_guess_accepts_positive_whole_numbers(self) -> None:
        self.assertEqual(guess_the_number.parse_guess(" 42 "), 42)
        self.assertIsNone(guess_the_number.parse_guess(""))
        self.assertIsNone(guess_the_number.parse_guess("-1"))
        self.assertIsNone(guess_the_number.parse_guess("4.2"))

    def test_guess_helpers(self) -> None:
        config = guess_the_number.GameConfig(minimum=10, maximum=20)

        self.assertTrue(guess_the_number.is_in_range(10, config))
        self.assertFalse(guess_the_number.is_in_range(9, config))
        self.assertEqual(guess_the_number.hint_for_guess(11, 12), "Too low - try something larger.")
        self.assertEqual(guess_the_number.hint_for_guess(13, 12), "Too high - try something smaller.")
        self.assertTrue(guess_the_number.winning_guess(12, 12))
        self.assertEqual(guess_the_number.losing_message(12), "No tries left. The number was 12.\n")


if __name__ == "__main__":
    unittest.main()
