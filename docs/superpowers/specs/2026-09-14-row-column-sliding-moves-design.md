# Design Spec: Row/Column Sliding Moves

## Summary

Allow a player to click or tap any tile in the same row or column as the empty space. The clicked tile and every tile between it and the empty space shift one position toward the empty space. The entire push counts as one move.

Example:

```text
Before:  1  2  _  3
Click 1

After:   _  1  2  3
```

This behavior applies to the 2×2, 3×3, and 4×4 puzzles.

## Functional requirements

- A tile is movable when it shares the empty space’s row or column.
- A tile may be clicked from either side of the empty space.
- All tiles between the clicked tile and the empty space shift toward the empty space.
- The clicked tile moves into the position immediately next to the former empty space.
- A valid push increments the move counter exactly once, regardless of how many tiles shift.
- A click on a tile in a different row and column has no effect.
- Invalid clicks must not change the board or move counter.
- After every valid push, the app checks whether the puzzle is solved.
- The existing timer, scramble behavior, puzzle-size selection, score saving, and leaderboard behavior remain unchanged.
- A solved puzzle disables further tile interaction.

## Game-logic design

Extend `move_tile(board, index, size)` in `game_logic.py` to support line moves.

Suggested interface:

```python
def move_tile(board, index, size):
    """Return the board after pushing the selected tile toward the blank.

    Return None when the selected tile is not in the blank's row or column.
    """
```

Algorithm:

1. Locate the empty position.
2. Convert the empty position and selected position into row/column coordinates.
3. Reject the move if the positions are neither in the same row nor the same column.
4. Determine the direction from the selected tile toward the empty position.
5. Copy the board.
6. Shift each tile along the selected-to-empty path one position toward the empty space.
7. Place the empty value in the selected tile’s original position.
8. Return the new board.

The helper must not mutate the caller’s board when the move is invalid. It should preserve the existing board representation, where the blank is represented by `size * size`.

Because each push is equivalent to a sequence of adjacent sliding moves, solvability remains preserved.

## UI and interaction design

Update the click handler in `fifteen.py` so that it:

- Determines whether the selected tile is aligned with the blank.
- Calls the updated game-logic helper for aligned tiles.
- Increments `st.session_state.moves` once after a successful push.
- Leaves the board and move count unchanged for invalid clicks.
- Performs the solved-board check after the complete push.

The existing Streamlit buttons already provide mouse, touch, and keyboard activation. No separate gesture implementation is required.

## Animation

The current animation tracks only one moving tile. Extend the animation state to describe every tile shifted by the push, for example:

```python
[
    (value, dx, dy),
    (value, dx, dy),
]
```

All affected tiles should animate simultaneously toward the empty position. The animation should:

- Clearly show the direction of the push.
- Use the existing animation duration and grid spacing unless visual testing shows they need adjustment.
- Avoid animating unaffected tiles.
- Continue to use unique widget keys or animation identifiers so Streamlit rerenders reliably after each move.

If simultaneous multi-tile animation proves unreliable in Streamlit, the fallback is a single short animation of the moving group or a final-state transition. The board state and move counting must not depend on animation completion.

## Acceptance criteria

1. On a 2×2, 3×3, or 4×4 board, clicking any tile aligned with the blank produces the correct shifted board.
2. Clicking an aligned tile works whether the blank is to the left, right, above, or below the clicked tile.
3. Clicking a non-aligned tile does nothing.
4. A multi-tile push increments the move counter by exactly one.
5. A one-tile adjacent move still works as before and counts as one move.
6. A valid push starts the game timer if the game has not started.
7. Solving the puzzle after a push displays the normal win state with the correct time and move count.
8. The leaderboard records the resulting move count using the existing schema.
9. Existing scrambling and solvability tests continue to pass.
10. Board state remains unchanged after an invalid click.

## Tests to add

Add unit tests in `test_game_logic.py` covering:

- Horizontal pushes with the blank to the right and to the left of the clicked tile.
- Vertical pushes with the blank below and above the clicked tile.
- One-tile adjacent moves.
- Non-aligned tiles returning `None`.
- No mutation of the input board on invalid moves.
- Correct behavior for dimensions 2, 3, and 4.

Add or update application-level tests, where practical, to verify that:

- Each successful push increments `moves` once.
- Invalid clicks do not increment `moves`.
- A push can produce a solved board and trigger the win state.

No database schema changes are required.
