# Intelligent Sudoku Solver: Hybrid CSP & Backtracking

This Sudoku Solver moves away from simple brute-force methods to implement an intelligent, hybrid AI approach. By combining Constraint Satisfaction Problem (CSP) techniques with optimized Backtracking search, the system solves puzzles of varying complexity with high efficiency. It utilizes deterministic logic to fill cells whenever possible and falls back to a search-based approach only when necessary.

The solver incorporates **Constraint Propagation** (Naked Singles and Hidden Singles) to reduce the search space and employs the **Minimum Remaining Values (MRV)** heuristic during backtracking to prioritize the most constrained cells. This mirrors human-like problem-solving while maintaining the computational speed of search algorithms.

### Gallery

| Main Landing Screen | Difficulty Selection |
| :---: | :---: |
| <img src="Screenshots/Main.png" width="400"> | <img src="Screenshots/Difficulty.png" width="400"> |

| Gameplay Visualization |
| :---: |
| <img src="Screenshots/Gameplay.png" width="800"> |

### System Functionality

The application uses a modular architecture that separates puzzle logic from the interactive visualization layer:

*   **Hybrid Solver Engine**: Executes deterministic CSP logic first, then employs recursive backtracking with MRV heuristics for remaining cells.
*   **Unique Puzzle Generation**: Algorithmically generates valid Sudoku grids and ensures every puzzle has exactly one unique solution.
*   **Real-time Visualization**: Animates the solving process using color-coding to distinguish between logic-solved and search-solved cells.
*   **Difficulty Scaling**: Supports Easy (35 cells removed), Medium (45 cells removed), and Hard (55 cells removed) levels.

### Project Structure

```text
.
├── Bg.png               # Landing screen background asset
├── Bg1.png              # Secondary background asset
├── setting.png          # UI settings icon
├── sudoku_core.py       # Core AI logic (CSP, Backtracking, MRV)
├── themed gui.py        # Pygame-based User Interface and Animation
└── Screenshots/         # UI documentation images
