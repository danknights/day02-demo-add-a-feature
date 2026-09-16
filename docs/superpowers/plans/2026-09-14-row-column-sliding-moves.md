# Row/Column Sliding Moves Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Let players click any tile aligned with the empty space and shift the intervening line of tiles toward the empty space as one counted move.

**Architecture:** Keep board transformation rules in the pure `move_tile` function in `game_logic.py`. Update the Streamlit handler in `fifteen.py` to accept aligned tiles, count one move per successful push, preserve timer and win behavior, and carry enough animation metadata to animate all shifted tiles.

**Tech Stack:** Python, `unittest`, Streamlit, existing CSS keyframe animations.

**Spec:** `docs/superpowers/specs/2026-09-14-row-column-sliding-moves-design.md`

## Global Constraints

- Support the 2×2, 3×3, and 4×4 puzzles.
- A valid push increments the move counter exactly once, regardless of how many tiles shift.
- All tiles between the clicked tile and the empty space shift toward the empty space.
- A click on a tile in a different row and column has no effect.
- No database schema changes are required.

---

### Task 1: Define line-move board behavior with failing tests

**Files:**
- Modify: `test_game_logic.py`
- Reference: `game_logic.py:move_tile`

**Interfaces:**
- Consumes: `move_tile(board: list[int], index: int, size: int)`.
- Produces: Tests requiring a shifted board for aligned selections and `None` for non-aligned selections.

- [ ] **Step 1: Add horizontal and vertical line-move tests**

Add tests for these exact cases:

```python
def test_pushes_tiles_horizontally_toward_a_blank_on_the_right(self):
    board = [1, 2, 9, 3, 4, 5, 6, 7, 8]
    self.assertEqual(move_tile(board, 0, 3), [9, 1, 2, 3, 4, 5, 6, 7, 8])

def test_pushes_tiles_horizontally_toward_a_blank_on_the_left(self):
    board = [9, 1, 2, 3, 4, 5, 6, 7, 8]
    self.assertEqual(move_tile(board, 2, 3), [1, 2, 9, 3, 4, 5, 6, 7, 8])

def test_pushes_tiles_vertically_toward_a_blank_below(self):
    board = [1, 9, 3, 4, 2, 6, 7, 8, 5]
    self.assertEqual(move_tile(board, 1, 3), [1, 2, 3, 4, 9, 6, 7, 8, 5])

def test_pushes_tiles_vertically_toward_a_blank_above(self):
    board = [1, 2, 3, 4, 9, 6, 7, 8, 5]
    self.assertEqual(move_tile(board, 7, 3), [1, 2, 3, 4, 8, 6, 7, 9, 5])
```

- [ ] **Step 2: Add dimension and invalid-selection tests**

Add these cases so the helper is exercised across all supported dimensions and invalid selections are explicitly non-mutating:

```python
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
    self.assertIsNone(move_tile(board, 0, 3))
    self.assertEqual(board, [1, 2, 3, 4, 5, 6, 7, 8, 9])
```

- [ ] **Step 3: Run the focused tests and verify the red state**

```bash
python -m unittest test_game_logic -v
```

Expected: FAIL in the new line-move assertions because the current implementation accepts only adjacent tiles.

### Task 2: Implement the pure board transformation

**Files:**
- Modify: `game_logic.py:move_tile`
- Test: `test_game_logic.py`

**Interfaces:**
- Consumes: The failing cases from Task 1.
- Produces: `move_tile(board, index, size)` returning a shifted board or `None`, without mutating the input for invalid moves.

- [ ] **Step 1: Locate the blank and selected coordinates**

Use `blank = size * size`, `divmod` for both indexes, and reject a selection unless either the row or column matches.

- [ ] **Step 2: Shift the selected-to-blank path toward the blank**

Copy the board, calculate a row/column step of `-1`, `0`, or `1`, walk backward from the blank toward the selected tile, copy each preceding tile into the current position, and place the blank at the selected index.

- [ ] **Step 3: Run the unit suite**

```bash
python -m unittest test_game_logic -v
```

Expected: PASS for all existing and new game-logic tests.

- [ ] **Step 4: Commit the pure logic change**

```bash
git add game_logic.py test_game_logic.py
git commit -m "feat: support row and column puzzle pushes"
```

### Task 3: Integrate aligned pushes into the Streamlit handler

**Files:**
- Modify: `fifteen.py:slide`, `fifteen.py:fresh_game`, and `fifteen.py:render_board`
- Test: `test_game_logic.py`; manually verify the Streamlit interaction

**Interfaces:**
- Consumes: `move_tile` returning either a shifted board or `None`.
- Produces: One move-counter increment per successful push, unchanged timer/win/save flow, and animation metadata for all shifted tiles.

- [ ] **Step 1: Replace the adjacency-only guard in `slide`**

Call `move_tile(board, idx, dimension)` and return without incrementing `tick` or `moves` when it returns `None`. On success, update the board and increment `moves` exactly once.

- [ ] **Step 2: Preserve timer and solved-state behavior**

Keep the existing timer start behavior, calculate final time after the complete push, and compare the resulting board with `solved_board(dimension)`.

- [ ] **Step 3: Animate every shifted tile**

Record each affected tile’s value and displacement using the original row/column and blank position. Reuse `PITCH`, `ANIM_MS`, and the unique rerender tick; board state and move counting must not depend on animation completion.

- [ ] **Step 4: Manually verify all supported sizes and directions**

```bash
streamlit run fifteen.py
```

Verify one-tile and multi-tile pushes, invalid clicks, one-move counting, solving, score saving, and disabled interaction for 2×2, 3×3, and 4×4 puzzles.

- [ ] **Step 5: Run the regression suite and commit**

```bash
python -m unittest test_game_logic -v
git add fifteen.py
git commit -m "feat: integrate row and column pushes into puzzle UI"
```
