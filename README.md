<div align="center">

# 🧩 8-Puzzle AI Solver

**A high-performance AI agent that solves a non-standard 8-puzzle with knight moves, divisibility swaps, jump-overs, and multiple goal states.**

[![Python 3.8+](https://img.shields.io/badge/Python-3.8%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.55-FF4B4B?logo=streamlit&logoColor=white)](https://streamlit.io/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

<br>

</div>

---

## 🔥 Why This Project Is Interesting

The classic 8-puzzle is a well-studied toy problem in AI. This variant turns it into a **genuinely harder** search challenge by adding four distinct move types:

| Move              | Classic 8-Puzzle | This Variant |
| ----------------- | :--------------: | :----------: |
| Basic Slide       |        ✅        |      ✅      |
| Knight Jump       |        ❌        |      ✅      |
| Divisibility Swap |        ❌        |      ✅      |
| Jump-Over         |        ❌        |      ✅      |
| Multiple Goals    |        ❌        | ✅ (4 goals) |

These rules **dramatically increase the branching factor**, making uninformed search far more expensive while rewarding well-designed heuristics. The project also ships with an interactive Streamlit dashboard for real-time visualization and benchmarking — not just a script, but a tool you can explore with.

---

## ✨ Features

- **4 unique action types** — slide, knight, divisibility swap, and jump-over
- **4 goal configurations** — the solver finds the closest reachable goal
- **BFS & A\* Search** with pluggable heuristic interface
- **2 admissible heuristics** — Halved Hamming and Halved Chebyshev Sum
- **Interactive Streamlit UI** — step-by-step solution playback and batch experiments
- **Search tree visualization** — Graphviz rendering of expanded nodes
- **Benchmark suite** — compare algorithms across randomized trials with charts

---

## 📐 Algorithms

### Breadth-First Search (BFS)

Explores the state space level by level using a FIFO queue. Guarantees an **optimal solution** when all step costs are uniform (cost = 1 per move), but expands many nodes on deeper instances.

### A\* Search

Uses a priority queue ordered by `f(n) = g(n) + h(n)` where `g(n)` is the path cost so far and `h(n)` is a heuristic estimate to the nearest goal. With an **admissible** heuristic, A\* is guaranteed optimal and typically expands far fewer nodes than BFS.

---

## 🧠 Heuristics & Admissibility

Both heuristics compute their raw value across **all 4 goal states** and take the **minimum**, then **divide by 2** (ceiling).

| Heuristic         | Raw Metric            | Formula                       |
| ----------------- | --------------------- | ----------------------------- |
| **Hamming / 2**   | # of misplaced tiles  | `⌈ min_goal(misplaced) / 2 ⌉` |
| **Chebyshev / 2** | Σ Chebyshev distances | `⌈ min_goal(Σ cheb) / 2 ⌉`    |

### Why divide by 2?

In the standard 8-puzzle, each action moves **one tile one step** toward (or away from) its goal. Manhattan or Hamming distances then serve as natural lower bounds.

In this variant, a single action can move a tile **up to 2 positions** (knight jump, jump-over) or fix **two tiles at once** (divisibility swap). That means one action can reduce the raw distance by up to **2 units**. Dividing by 2 accounts for this worst-case reduction:

```
h(n) = ⌈raw(n) / 2⌉  ≤  true cost
```

Because no single action can reduce the raw metric by more than 2, the halved value **never overestimates** the true cost — preserving **admissibility** and therefore A\* optimality.

---

## 🧩 Move Rules in Detail

### 1. Basic Slide

Standard 4-directional slide of a tile adjacent to the blank (Up / Down / Left / Right).

### 2. Knight Move

A tile at an L-shaped chess-knight offset from the blank jumps directly into the blank position.

### 3. Divisibility Swap

Two **adjacent, non-blank** tiles `A` and `B` swap positions if `A % B == 0` or `B % A == 0`. The blank is not involved.

### 4. Jump-Over

When three cells form a line as `A - B - Blank`, tile A leaps over B into the blank. B stays in place.

---

## 🎯 Goal States

The solver accepts **any** of these four configurations as a valid goal:

```
Goal 1        Goal 2        Goal 3        Goal 4
1 2 3         8 7 6         _ 1 2         _ 8 7
4 5 6         5 4 3         3 4 5         6 5 4
7 8 _         2 1 _         6 7 8         3 2 1
```

---

## 📁 Project Structure

```
task1/
├── app.py                  # Streamlit web UI (tabs: visualization + experiments)
├── main.py                 # CLI entry point (demo + batch experiments)
├── experiment.py           # Benchmark runner shared by CLI and UI
├── requirements.txt
├── README.md
└── src/
    ├── __init__.py          # Package exports
    ├── problem.py           # PuzzleState, EightPuzzle (state space + actions)
    ├── search.py            # BFS, A*, SearchResult, Node
    ├── heuristics.py        # HammingHeuristic, ChebyshevSumHeuristic
    ├── utils.py             # Random state generator
    └── visualization.py     # Text tree + Graphviz rendering
```

### Architecture Overview

```
┌──────────────┐       ┌──────────────┐
│   app.py     │       │   main.py    │
│  (Streamlit) │       │    (CLI)     │
└──────┬───────┘       └──────┬───────┘
       │                      │
       └──────┬───────────────┘
              ▼
     ┌─────────────────┐
     │  experiment.py  │  ← orchestrates trials
     └────────┬────────┘
              ▼
  ┌───────────────────────────────────────┐
  │               src/                    │
  │                                       │
  │  problem.py ─── state space + rules   │
  │  search.py  ─── BFS, A* algorithms    │
  │  heuristics.py ── Hamming/2, Cheb/2   │
  │  utils.py   ─── random state gen      │
  │  visualization.py ── tree rendering   │
  └───────────────────────────────────────┘
```

The `src` package is **framework-agnostic** — it has zero dependency on Streamlit. Both the CLI (`main.py`) and the web UI (`app.py`) consume it through `experiment.py`, keeping the core logic cleanly separated.

---

## 🚀 Installation

```bash
# Clone the repository
git clone https://github.com/dyphat0711/8-puzzle-ai-solver.git
cd 8-puzzle-ai-solver

# (Recommended) Create a virtual environment
python -m venv venv
source venv/bin/activate   # Linux/macOS
venv\Scripts\activate      # Windows

# Install dependencies
pip install -r requirements.txt
```

### Dependencies

| Package     | Version | Purpose                   |
| ----------- | ------- | ------------------------- |
| `streamlit` | 1.55+   | Interactive web dashboard |
| `graphviz`  | 0.21+   | Search tree visualization |
| `pandas`    | 2.3+    | Experiment data handling  |

> **Note:** You also need the [Graphviz system binary](https://graphviz.org/download/) installed for tree rendering.

---

## 💻 Usage

### Web UI (Streamlit)

```bash
streamlit run app.py
```

The dashboard has two tabs:

| Tab                            | Description                                                                                                  |
| ------------------------------ | ------------------------------------------------------------------------------------------------------------ |
| **Step-by-step Visualization** | Pick an algorithm, solve a random puzzle, and watch each move animated on a board with a search tree diagram |
| **Experiments & History**      | Run batch trials, compare BFS vs A\* variants, view summary tables and performance charts                    |

### Command Line

```bash
python main.py
```

Runs an interactive demo (choose your algorithm) followed by a batch benchmark of all three solvers.

---

## 🧪 Example Run

```
============================================================
TRÌNH GIẢI 8-PUZZLE
============================================================

[Trạng thái bắt đầu]
2 8 3
1 _ 5
4 7 6

Đang tìm đường đi bằng A* (Chebyshev/2)...
Đã giải xong trong 0.0032 giây!
Cost: 5 | Nodes Expanded: 12 | Max Frontier: 18

[Đường đi chi tiết - 5 bước]

Bước 0 [BẮT ĐẦU]
  2 8 3
  1 _ 5
  4 7 6

Bước 1 [Slide-Up]
  2 _ 3
  1 8 5
  4 7 6

  ... (remaining steps) ...

Bước 5 [Slide-Right]
  1 2 3
  4 5 6
  7 8 _
```

---

## 📊 Benchmark Metrics

Each experiment records four metrics per solver:

| Metric                | Description                                  |
| --------------------- | -------------------------------------------- |
| **Path Cost**         | Total number of actions in the solution      |
| **Nodes Expanded**    | States popped from the frontier and explored |
| **Max Frontier Size** | Peak memory usage of the open list           |
| **Execution Time**    | Wall-clock time in seconds                   |

### Sample Benchmark (5 trials, 15-step shuffle)

| Algorithm         | Avg Cost | Avg Expanded | Avg Frontier | Avg Time (s) |
| ----------------- | :------: | :----------: | :----------: | :----------: |
| A\* (Chebyshev/2) |   ~5.2   |     ~28      |     ~42      |    ~0.005    |
| A\* (Hamming/2)   |   ~5.2   |     ~35      |     ~51      |    ~0.007    |
| BFS               |   ~5.2   |     ~180     |     ~290     |    ~0.035    |

> A\* with Chebyshev/2 consistently expands **5–10× fewer nodes** than BFS while finding solutions of the same cost.

---

## 📈 Future Improvements

- **Pattern Database heuristic** — precompute exact sub-problem costs for stronger lower bounds
- **Linear Conflict** — augment Chebyshev with conflict penalties for tiles in the same row/column
- **IDA\*** — iterative-deepening A\* to reduce memory from O(b^d) to O(d)
- **Bidirectional search** — search from start and goal simultaneously (feasible with multiple goals via virtual goal node)
- **Parallel state expansion** — leverage multiprocessing for large branching factors
- **Animated GIF export** — render the solution path as a shareable animation

---

## 🤝 Contributing

Contributions are welcome! To get started:

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/your-feature`)
3. Commit your changes (`git commit -m 'Add your feature'`)
4. Push to the branch (`git push origin feature/your-feature`)
5. Open a Pull Request

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

---

<div align="center">

**If you found this useful, consider giving it a ⭐**

</div>
