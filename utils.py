import random
from problem import PuzzleState, EightPuzzle

def generate_random_state(steps=20):
    goal = random.choice(EightPuzzle.GOALS)
    state = PuzzleState(goal)
    problem = EightPuzzle(state)
    visited = {state}
    for _ in range(steps):
        successors = problem.get_successors(state)
        random.shuffle(successors)
        moved = False
        for succ, _, _ in successors:
            if succ not in visited:
                visited.add(succ)
                state = succ
                moved = True
                break
        if not moved:
            state = successors[0][0]
    return state