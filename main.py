# main.py
from experiment import run_demo, run_experiments

from src import (
    EightPuzzle,
    generate_random_state,
    BreadthFirstSearch,
    AStarSearch,
    HammingHeuristic,
    ChebyshevSumHeuristic,
    render_tree_graphviz
)

if __name__ == "__main__":
    run_demo()
    
    # Visualize the search tree for a single random puzzle
    initial_state = generate_random_state(steps=15)
    problem = EightPuzzle(initial_state)
    solver = AStarSearch(ChebyshevSumHeuristic())
    result = solver.search(problem)
    
    render_tree_graphviz(solver.expanded_nodes, n=15, filename="search_tree", view=True)
    
    # Experiment between BFS and A* with 2 heuristics
    run_experiments(num_trials=5, shuffle_steps=15)