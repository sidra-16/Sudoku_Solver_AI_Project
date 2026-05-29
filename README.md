# Sudoku Solver

A Python-based Sudoku Solver that uses AI techniques to solve puzzles automatically. The project combines CSP (Constraint Satisfaction Problem) methods with Backtracking and the MRV heuristic to solve Sudoku boards efficiently.

## Features

* Solve Sudoku puzzles automatically
* Easy, Medium, and Hard difficulty levels
* Real-time solving visualization
* Color-coded solving animation
* Puzzle generator with unique solutions
* Interactive GUI built with Pygame

## Technologies Used

* Python
* Pygame
* CSP (Constraint Satisfaction Problem)
* Backtracking Algorithm
* MRV Heuristic

## How It Works

The solver first applies logical CSP techniques like Naked Singles and Hidden Singles. If the puzzle is still incomplete, it uses Backtracking with the MRV heuristic to finish the solution efficiently.

## Run the Project

```bash
python themed_gui.py
```

## Project Structure

* `sudoku_core.py` → Solver logic and puzzle generation
* `themed_gui.py` → GUI and visualization
* `assets/` → Images and UI resources

## Authors

* Muhammad Nafay Anjum
* Sidra Tul Muntaha
