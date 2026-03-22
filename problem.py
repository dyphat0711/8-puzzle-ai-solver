# problem.py
class SearchProblem:
    """Domain-independent interface for a state-space search problem.

    Any concrete problem only needs to implement three methods, making the
    search algorithms completely reusable across different domains.
    """

    def get_start_state(self):
        raise NotImplementedError

    def is_goal_state(self, state):
        raise NotImplementedError

    def get_successors(self, state):
        raise NotImplementedError


# ── Puzzle state ─────────────────────────────────────────────────────────────

class PuzzleState:
    """Immutable, hashable snapshot of a 3x3 sliding-tile board.

    The board is a 9-element tuple read left-to-right, top-to-bottom.
    ``0`` represents the blank cell.
    """

    __slots__ = ("board", "blank")

    def __init__(self, board):
        self.board = tuple(board)
        self.blank = self.board.index(0)

    def __hash__(self):
        return hash(self.board)

    def __eq__(self, other: object):
        return isinstance(other, PuzzleState) and self.board == other.board

    def __repr__(self) -> str:
        b = self.board
        def _f(v):
            return str(v) if v else "_"
        return (
            f"{_f(b[0])} {_f(b[1])} {_f(b[2])}\n"
            f"{_f(b[3])} {_f(b[4])} {_f(b[5])}\n"
            f"{_f(b[6])} {_f(b[7])} {_f(b[8])}"
        )

    def swap(self, i, j):
        """Return a **new** state with positions *i* and *j* exchanged."""
        lst = list(self.board)
        lst[i], lst[j] = lst[j], lst[i]
        return PuzzleState(lst)


# ── Grid helpers ─────────────────────────────────────────────────────────────

_BASIC_DIRS = (
    (-1, 0, "Up"), (1, 0, "Down"), (0, -1, "Left"), (0, 1, "Right"),
)

_KNIGHT_OFFSETS = (
    (-2, -1), (-2, 1), (-1, -2), (-1, 2),
    (1, -2),  (1, 2),  (2, -1),  (2, 1),
)

# (delta_A_row, delta_A_col, delta_B_row, delta_B_col) relative to blank
_JUMP_PATTERNS = (
    (-2, 0, -1, 0),   # A two rows above, B one row above
    (2,  0,  1, 0),   # A two rows below, B one row below
    (0, -2,  0, -1),  # A two cols left,  B one col left
    (0,  2,  0,  1),  # A two cols right, B one col right
)


def _rc(idx):
    return divmod(idx, 3)


def _idx(r, c):
    return r * 3 + c


def _ok(r, c):
    return 0 <= r < 3 and 0 <= c < 3


# ── Concrete puzzle ──────────────────────────────────────────────────────────

class EightPuzzle(SearchProblem):
    """8-Puzzle with **4 goal states** and **4 action types**.

    Actions
    -------
    1. Basic slide (Up / Down / Left / Right) into the blank.
    2. L-shaped chess-knight jump into the blank.
    3. Divisibility swap of two adjacent non-blank tiles (A%B==0 or B%A==0).
    4. Jump-over: A leaps over B into the blank when A-B-Blank are consecutive.
    """

    GOALS = (
        (1, 2, 3, 4, 5, 6, 7, 8, 0),
        (8, 7, 6, 5, 4, 3, 2, 1, 0),
        (0, 1, 2, 3, 4, 5, 6, 7, 8),
        (0, 8, 7, 6, 5, 4, 3, 2, 1),
    )
    GOAL_SET = frozenset(GOALS)

    def __init__(self, initial):
        self._initial = initial

    def get_start_state(self):
        return self._initial

    def is_goal_state(self, state) :
        return state.board in self.GOAL_SET

    def get_successors(self, state):
        out = []
        b = state.board
        blank = state.blank
        br, bc = _rc(blank)
        self._basic(out, state, b, blank, br, bc)
        self._knight(out, state, b, blank, br, bc)
        self._div_swap(out, state, b)
        self._jump(out, b, blank, br, bc)
        return out

    # ── action generators (static to keep state immutable) ───────────────

    @staticmethod
    def _basic(out, state, b, blank, br, bc):
        """1. Slide an adjacent tile into the blank."""
        for dr, dc, name in _BASIC_DIRS:
            nr, nc = br + dr, bc + dc
            if _ok(nr, nc):
                out.append((state.swap(blank, _idx(nr, nc)), f"Slide-{name}", 1))

    @staticmethod
    def _knight(out, state, b, blank, br, bc):
        """2. Knight-shaped jump into the blank."""
        for dr, dc in _KNIGHT_OFFSETS:
            nr, nc = br + dr, bc + dc
            if _ok(nr, nc):
                ni = _idx(nr, nc)
                out.append((state.swap(blank, ni), f"Knight({b[ni]})", 1))

    @staticmethod
    def _div_swap(out, state, b):
        """3. Swap two adjacent non-blank tiles when one value divides the other."""
        for i in range(9):
            if b[i] == 0:
                continue
            ri, ci = _rc(i)
            # Only check right and down neighbours to avoid duplicate pairs
            for dr, dc in ((0, 1), (1, 0)):
                nr, nc = ri + dr, ci + dc
                if not _ok(nr, nc):
                    continue
                j = _idx(nr, nc)
                if b[j] == 0:
                    continue
                a, bv = b[i], b[j]
                if a % bv == 0 or bv % a == 0:
                    out.append((state.swap(i, j), f"DivSwap({a},{bv})", 1))

    @staticmethod
    def _jump(out, b, blank, br, bc):
        """4. Tile A jumps over tile B into the blank (A-B-Blank consecutive)."""
        for da_r, da_c, dm_r, dm_c in _JUMP_PATTERNS:
            ar, ac = br + da_r, bc + da_c
            mr, mc = br + dm_r, bc + dm_c
            if _ok(ar, ac) and _ok(mr, mc):
                ai = _idx(ar, ac)
                mi = _idx(mr, mc)
                if b[ai] != 0 and b[mi] != 0:
                    lst = list(b)
                    lst[blank] = b[ai]
                    lst[ai] = 0
                    out.append((PuzzleState(lst), f"Jump({b[ai]}over{b[mi]})", 1))