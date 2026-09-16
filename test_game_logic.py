import unittest

from game_logic import is_solvable, move_tile, scrambled_board, solved_board


class GameLogicTests(unittest.TestCase):
    def test_each_supported_puzzle_has_the_expected_solved_board(self):
        self.assertEqual(solved_board(2), [1, 2, 3, 4])
        self.assertEqual(solved_board(3), list(range(1, 10)))
        self.assertEqual(solved_board(4), list(range(1, 17)))

    def test_only_adjacent_tiles_move_into_the_blank(self):
        board = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 16, 15]

        moved = move_tile(board, 15, 4)
        self.assertEqual(moved, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16])

        self.assertIsNone(move_tile(board, 9, 4))
        self.assertEqual(board[-2:], [16, 15])

    def test_pushes_tiles_horizontally_toward_a_blank_on_the_right(self):
        board = [1, 2, 9, 3, 4, 5, 6, 7, 8]

        moved = move_tile(board, 0, 3)

        self.assertEqual(moved, [9, 1, 2, 3, 4, 5, 6, 7, 8])

    def test_pushes_tiles_horizontally_toward_a_blank_on_the_left(self):
        board = [9, 1, 2, 3, 4, 5, 6, 7, 8]

        moved = move_tile(board, 2, 3)

        self.assertEqual(moved, [1, 2, 9, 3, 4, 5, 6, 7, 8])

    def test_pushes_tiles_vertically_toward_a_blank_below(self):
        board = [1, 2, 3, 4, 5, 6, 7, 9, 8]

        moved = move_tile(board, 1, 3)

        self.assertEqual(moved, [1, 9, 3, 4, 2, 6, 7, 5, 8])

    def test_pushes_tiles_vertically_toward_a_blank_above(self):
        board = [1, 9, 3, 4, 2, 6, 7, 5, 8]

        moved = move_tile(board, 7, 3)

        self.assertEqual(moved, [1, 2, 3, 4, 5, 6, 7, 9, 8])

    def test_four_by_four_push_can_shift_three_tiles(self):
        board = [1, 2, 3, 16, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 4]

        moved = move_tile(board, 15, 4)

        self.assertEqual(
            moved,
            [1, 2, 3, 8, 5, 6, 7, 12, 9, 10, 11, 4, 13, 14, 15, 16],
        )

    def test_line_moves_work_for_the_2_by_2_and_4_by_4_boards(self):
        boards = {
            2: ([1, 4, 3, 2], 3, [1, 2, 3, 4]),
            4: (
                [1, 2, 3, 4, 5, 6, 16, 8, 9, 10, 7, 12, 13, 14, 11, 15],
                14,
                [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 16, 15],
            ),
        }
        for size, (board, index, expected) in boards.items():
            with self.subTest(size=size):
                self.assertEqual(move_tile(board, index, size), expected)

    def test_non_aligned_tile_returns_none_without_mutating_the_board(self):
        board = [1, 2, 3, 4, 5, 6, 7, 8, 9]

        moved = move_tile(board, 0, 3)

        self.assertIsNone(moved)
        self.assertEqual(board, [1, 2, 3, 4, 5, 6, 7, 8, 9])

    def test_valid_line_move_does_not_mutate_the_input_board(self):
        board = [1, 2, 9, 3, 4, 5, 6, 7, 8]

        moved = move_tile(board, 0, 3)

        self.assertEqual(moved, [9, 1, 2, 3, 4, 5, 6, 7, 8])
        self.assertEqual(board, [1, 2, 9, 3, 4, 5, 6, 7, 8])

    def test_solvability_uses_the_board_width(self):
        self.assertTrue(is_solvable(solved_board(3), 3))
        self.assertTrue(is_solvable(solved_board(4), 4))
        self.assertFalse(is_solvable([2, 1, 3, 4, 5, 6, 7, 8, 9], 3))

    def test_scramble_never_returns_the_solved_board(self):
        for size in (2, 3, 4):
            for _ in range(20):
                board = scrambled_board(size)
                self.assertNotEqual(board, solved_board(size))


if __name__ == "__main__":
    unittest.main()
