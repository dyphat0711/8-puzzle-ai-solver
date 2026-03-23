# heuristics.py
import math
from src import EightPuzzle

# ── Abstract heuristic ───────────────────────────────────────────────────────

class Heuristic:
    def __call__(self, state):
        raise NotImplementedError

    @property
    def name(self):
        raise NotImplementedError


# ── Pre-computed goal-tile positions ─────────────────────────────────────────

GOAL_POSITIONS = []
for _g in EightPuzzle.GOALS:
    _pos = {}
    for _i, _v in enumerate(_g):
        if _v != 0:
            _pos[_v] = divmod(_i, 3)
    GOAL_POSITIONS.append(_pos)


# ── Heuristic 1: Hamming (Misplaced Tiles / 2) ───────────────────────

class HammingHeuristic(Heuristic):
    @property
    def name(self):
        return "Hamming/2"

    def __call__(self, state):
        board = state.board
        best = 9  # upper-bound sentinel (max 8 misplaced tiles)
        for goal in EightPuzzle.GOALS:
            misplaced = 0
            for i in range(9):
                if board[i] != 0 and board[i] != goal[i]:
                    misplaced += 1
            if misplaced < best:
                best = misplaced
        return math.ceil(best / 2)


# ── Heuristic 2: Chebyshev-Sum Distance ──────────────────────────────

class ChebyshevSumHeuristic(Heuristic):
    @property
    def name(self):
        return "Chebyshev/2"

    def __call__(self, state):
        board = state.board
        best = math.inf
        for gpos in GOAL_POSITIONS:
            total = 0
            for i in range(9):
                val = board[i]
                if val == 0:
                    continue
                cr, cc = divmod(i, 3)
                gr, gc = gpos[val]
                total += max(abs(cr - gr), abs(cc - gc))
            if total < best:
                best = total
        return math.ceil(best / 2)