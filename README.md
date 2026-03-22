# 8-Puzzle AI Solver

## Overview
The 8-Puzzle AI Solver is a project that implements algorithms to solve the classic 8-puzzle problem. The 8-puzzle consists of a 3x3 grid with 8 numbered tiles and one blank space, allowing tiles to slide into the blank space. The objective is to move the tiles into a specified goal state using the fewest number of moves.

## Features
- **Multiple algorithms**: Implementations of various search algorithms such as A*, BFS, DFS, and Uniform Cost Search.
- **Interactive visualization**: A visual representation of the solving process to help users understand how the algorithms work.
- **User-friendly interface**: Simple and easy-to-use interface for inputting puzzles and viewing solutions.
- **Performance metrics**: Displays time taken and number of moves for finding solutions.
- **Configurable goal states**: Support for custom goal state configurations.
- **Heuristic evaluation**: Implements heuristics like Manhattan distance for optimized pathfinding.

## Installation
To get started with the 8-Puzzle AI Solver, clone the repository and ensure you have the necessary dependencies installed:

```bash
# Clone the repository
git clone https://github.com/dyphat0711/8-puzzle-ai-solver.git

# Change into the directory
cd 8-puzzle-ai-solver

# Install dependencies (if applicable)
# For example, for Python, you might run:
pip install -r requirements.txt
```

## Usage
To use the 8-Puzzle AI Solver:

1. **Input the initial puzzle configuration**: Provide a space-separated string or a 2D array representing the initial state of the puzzle, where `0` represents the blank space.
2. **Choose the algorithm**: Select the solving algorithm you'd like to apply.
3. **Run the solver**: Execute the main program to find the solution, and view the result.

```bash
# Example command to run the solver
python solver.py
```

## Algorithms
The following algorithms are implemented:
- **Breadth-First Search (BFS)**: Explores all possible states at the present depth prior to moving on to states at the next depth level. Guarantees shortest solution.
- **Depth-First Search (DFS)**: Explores as far as possible along each branch before backing up. Suitable for memory-constrained environments.
- **Uniform Cost Search**: Expands the least cost node in the frontier.
- **A* Search**: Combines the benefits of BFS and heuristics to efficiently find the shortest path. Recommended for optimal performance.

## How It Works
1. The solver reads the initial puzzle state
2. Applies the selected algorithm with appropriate heuristics
3. Explores the state space to find a path to the goal state
4. Returns the sequence of moves needed to solve the puzzle
5. Displays metrics such as execution time and number of moves

## Performance
The performance of different algorithms varies:
- **BFS**: Complete but can be slow for deep solutions
- **A***: Most efficient, especially with Manhattan distance heuristic
- **DFS**: Fast but does not guarantee optimal solutions

## Contributing
Contributions are welcome! To contribute to the 8-Puzzle AI Solver:
1. Fork the repository.
2. Create your feature branch (`git checkout -b feature/YourFeature`).
3. Commit your changes (`git commit -m 'Add some feature'`).
4. Push to the branch (`git push origin feature/YourFeature`).
5. Create a new Pull Request.

## License
This project is open source and available under the MIT License.

Thank you for considering contributing to the project!