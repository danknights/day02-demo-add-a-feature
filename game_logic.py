import random


def solved_board(size):
    return list(range(1, size * size + 1))


def is_solvable(board, size):
    blank = size * size
    tiles = [value for value in board if value != blank]
    inversions = sum(
        1
        for i in range(len(tiles))
        for j in range(i + 1, len(tiles))
        if tiles[i] > tiles[j]
    )
    if size % 2 == 1:
        return inversions % 2 == 0
    row_from_bottom = size - board.index(blank) // size
    return (inversions + row_from_bottom) % 2 == 1


def move_tile(board, index, size):
    blank = size * size
    blank_index = board.index(blank)
    blank_row, blank_col = divmod(blank_index, size)
    row, col = divmod(index, size)
    if blank_row != row and blank_col != col:
        return None

    moved_board = board.copy()
    row_step = (blank_row > row) - (blank_row < row)
    col_step = (blank_col > col) - (blank_col < col)
    current_row, current_col = blank_row, blank_col
    while (current_row, current_col) != (row, col):
        previous_row = current_row - row_step
        previous_col = current_col - col_step
        current_index = current_row * size + current_col
        previous_index = previous_row * size + previous_col
        moved_board[current_index] = board[previous_index]
        current_row, current_col = previous_row, previous_col
    moved_board[index] = blank
    return moved_board


def scrambled_board(size, n_swaps=None):
    n_swaps = n_swaps or size * size * 10
    while True:
        board = solved_board(size)
        for _ in range(n_swaps):
            i, j = random.sample(range(size * size), 2)
            board[i], board[j] = board[j], board[i]
        if board != solved_board(size) and is_solvable(board, size):
            return board
