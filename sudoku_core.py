"""
Sudoku Core Logic Module
Handles puzzle generation, solving algorithms (CSP + Backtracking), and validation
"""

import random
import copy
import time


class Sudoku:
    def __init__(self):  
        self.grid = [[0 for _ in range(9)] for _ in range(9)]
        self.original_grid = None  
        self.solution_grid = None  
        self.backtrack_cells = set()  
        self.csp_cells = set()  
        self.solving_complete = False  
        self.random_colors = self.generate_random_colors()
        
    def generate_random_colors(self):
        """Generate vibrant random colors for different solving methods"""
        colors = []
        for _ in range(10):  
            r = random.randint(100, 255)
            g = random.randint(100, 255) 
            b = random.randint(100, 255)
            
            max_val = max(r, g, b)
            if max_val < 200:
                if random.choice([True, False, False]):
                    r = 255
                elif random.choice([True, False]):
                    g = 255
                else:
                    b = 255
            
            colors.append((r, g, b))
        return colors
    
    def get_random_color(self, cell_type='csp'):
        """Get a random vibrant color based on cell type"""
        if cell_type == 'csp':
            # Use first half of colors for CSP
            return random.choice(self.random_colors[:5])
        else:  # backtrack
            # Use second half of colors for backtracking
            return random.choice(self.random_colors[5:])
        
    def is_valid(self, num, row, col):
        # Check row and column
        for i in range(9):
            if self.grid[row][i] == num or self.grid[i][col] == num:
                return False

        # Check 3x3 box
        start_row, start_col = 3 * (row // 3), 3 * (col // 3)
        for i in range(3):
            for j in range(3):
                if self.grid[start_row + i][start_col + j] == num:
                    return False

        return True

    def is_valid_grid(self, grid, num, row, col):
        for i in range(9):
            if grid[row][i] == num or grid[i][col] == num:
                return False
        start_row, start_col = 3 * (row // 3), 3 * (col // 3)
        for i in range(3):
            for j in range(3):
                if grid[start_row + i][start_col + j] == num:
                    return False
        return True

    def fill_grid(self):
        numbers = list(range(1, 10))
        for i in range(9):
            for j in range(9):
                if self.grid[i][j] == 0:
                    random.shuffle(numbers)
                    for num in numbers:
                        if self.is_valid(num, i, j):
                            self.grid[i][j] = num
                            if self.fill_grid():
                                return True
                            self.grid[i][j] = 0
                    return False
        return True

    def count_solutions(self, grid_copy):
        """Helper to check uniqueness of the puzzle."""
        def backtrack():
            for row in range(9):
                for col in range(9):
                    if grid_copy[row][col] == 0:
                        for num in range(1, 10):
                            if self.is_valid_grid(grid_copy, num, row, col):
                                grid_copy[row][col] = num
                                if backtrack():
                                    return True
                                grid_copy[row][col] = 0
                        return False
            return True

        return backtrack()

    def generate_puzzle(self, difficulty="medium"):
        max_retries = 5
        retry_count = 0
        
        while retry_count < max_retries:
            self.grid = [[0 for _ in range(9)] for _ in range(9)]
            self.fill_grid()
            self.solution_grid = copy.deepcopy(self.grid)

            if difficulty == "easy":
                cells_to_remove = 35
            elif difficulty == "medium":
                cells_to_remove = 45
            elif difficulty == "hard":
                cells_to_remove = 55
            else:
                raise ValueError("Difficulty must be 'easy', 'medium', or 'hard'.")

            attempts = 0
            max_attempts = cells_to_remove * 5
            removed = 0

            while removed < cells_to_remove and attempts < max_attempts:
                row, col = random.randint(0, 8), random.randint(0, 8)
                if self.grid[row][col] == 0:
                    attempts += 1
                    continue

                backup = self.grid[row][col]
                self.grid[row][col] = 0
                removed += 1
                attempts += 1

            self.original_grid = copy.deepcopy(self.grid)
            self.backtrack_cells = set()
            self.csp_cells = set()
            self.solving_complete = False
            self.random_colors = self.generate_random_colors()
            
            # Test if puzzle is solvable
            test_grid = copy.deepcopy(self.grid)
            temp_sudoku = Sudoku()
            temp_sudoku.grid = test_grid
            temp_sudoku.original_grid = self.original_grid
            
            if temp_sudoku.solve():
                # Puzzle is solvable
                break
            else:
                # Puzzle is unsolvable, retry
                retry_count += 1
                if retry_count >= max_retries:
                    print(f"Warning: Generated unsolvable puzzle after {max_retries} retries. Proceeding anyway.")
                    break

    def load_new_puzzle(self, difficulty="medium"):
        self.grid = [[0 for _ in range(9)] for _ in range(9)]  # Reset grid
        self.generate_puzzle(difficulty)

    # CSP Methods
    def get_empty_cell(self):
        """Return the position of an empty cell with fewest possibilities."""
        min_possibilities = 10
        best_cell = None
        
        for row in range(9):
            for col in range(9):
                if self.grid[row][col] == 0:
                    possibilities = self.count_possibilities(row, col)
                    if possibilities < min_possibilities and possibilities > 0:
                        min_possibilities = possibilities
                        best_cell = (row, col)
        
        return best_cell
    
    def count_possibilities(self, row, col):
        """Count the number of possible values for a cell."""
        count = 0
        for num in range(1, 10):
            if self.is_valid(num, row, col):
                count += 1
        return count
    
    def get_possible_values(self, row, col):
        """Return a list of possible values for a cell."""
        return [num for num in range(1, 10) if self.is_valid(num, row, col)]
    
    def get_grid_state(self):
        """Return current grid state for visualization"""
        return copy.deepcopy(self.grid)

    def solve(self, screen=None, box_x=0, box_y=0, cell_size=60, update_display=False):
        """Enhanced solve using hybrid approach with complete grid validation."""
        self.solving_complete = False
        
        # Phase 1: Enhanced CSP with multiple constraint propagation techniques
        progress_made = True
        iteration_count = 0
        max_iterations = 50  # Prevent infinite loops
        
        while progress_made and iteration_count < max_iterations:
            progress_made = False
            iteration_count += 1
            
            # Naked Singles (cells with only one possibility)
            for row in range(9):
                for col in range(9):
                    if self.grid[row][col] == 0:
                        possible_values = self.get_possible_values(row, col)
                        if len(possible_values) == 1:
                            self.grid[row][col] = possible_values[0]
                            self.csp_cells.add((row, col))
                            progress_made = True
                            
                            if update_display and screen:
                                self._update_visual_solving_callback(screen, box_x, box_y, cell_size)
            
            # Hidden Singles (numbers that can only go in one place in a unit)
            if not progress_made:
                progress_made = self.find_hidden_singles(screen, box_x, box_y, cell_size, update_display)
            
            # Check if puzzle is solved after CSP
            if self.is_complete():
                self.solving_complete = True
                if update_display and screen:
                    self._update_visual_solving_callback(screen, box_x, box_y, cell_size)
                return True
        
        # Phase 2: Use backtracking for remaining cells
        result = self.solve_backtracking(screen, box_x, box_y, cell_size, update_display)
        if result:
            self.solving_complete = True
            if update_display and screen:
                self._update_visual_solving_callback(screen, box_x, box_y, cell_size)
        return result
    
    def is_complete(self):
        """Check if the puzzle is completely solved"""
        for row in range(9):
            for col in range(9):
                if self.grid[row][col] == 0:
                    return False
        return True
    
    def find_hidden_singles(self, screen=None, box_x=0, box_y=0, cell_size=60, update_display=False):
        """Find hidden singles in rows, columns, and boxes"""
        progress_made = False
        
        # Check rows
        for row in range(9):
            for num in range(1, 10):
                possible_cols = []
                for col in range(9):
                    if self.grid[row][col] == 0 and self.is_valid(num, row, col):
                        possible_cols.append(col)
                
                if len(possible_cols) == 1:
                    col = possible_cols[0]
                    self.grid[row][col] = num
                    self.csp_cells.add((row, col))
                    progress_made = True
                    
                    if update_display and screen:
                        self._update_visual_solving_callback(screen, box_x, box_y, cell_size)
        
        # Check columns
        for col in range(9):
            for num in range(1, 10):
                possible_rows = []
                for row in range(9):
                    if self.grid[row][col] == 0 and self.is_valid(num, row, col):
                        possible_rows.append(row)
                
                if len(possible_rows) == 1:
                    row = possible_rows[0]
                    self.grid[row][col] = num
                    self.csp_cells.add((row, col))
                    progress_made = True
                    
                    if update_display and screen:
                        self._update_visual_solving_callback(screen, box_x, box_y, cell_size)
        
        # Check 3x3 boxes
        for box_row in range(3):
            for box_col in range(3):
                for num in range(1, 10):
                    possible_cells = []
                    start_row, start_col = 3 * box_row, 3 * box_col
                    
                    for i in range(3):
                        for j in range(3):
                            row, col = start_row + i, start_col + j
                            if self.grid[row][col] == 0 and self.is_valid(num, row, col):
                                possible_cells.append((row, col))
                    
                    if len(possible_cells) == 1:
                        row, col = possible_cells[0]
                        self.grid[row][col] = num
                        self.csp_cells.add((row, col))
                        progress_made = True
                        
                        if update_display and screen:
                            self._update_visual_solving_callback(screen, box_x, box_y, cell_size)
        
        return progress_made
        
    def solve_backtracking(self, screen=None, box_x=0, box_y=0, cell_size=60, update_display=False):
        """Enhanced backtracking with complete validation."""
        # Find empty cell with minimum remaining values (MRV heuristic)
        empty_cell = self.get_empty_cell()
        if not empty_cell:
            return True  # Puzzle solved
            
        row, col = empty_cell
        possible_values = self.get_possible_values(row, col)
        
        # Try each possible value
        for num in possible_values:
            if self.is_valid(num, row, col):
                # Place the number
                self.grid[row][col] = num
                self.backtrack_cells.add((row, col))
                
                # Visual update for placing number
                if update_display and screen:
                    self._update_visual_solving_callback(screen, box_x, box_y, cell_size)
                    
                # Recursively solve
                if self.solve_backtracking(screen, box_x, box_y, cell_size, update_display):
                    return True
                    
                # Backtrack: remove the number
                self.grid[row][col] = 0
                self.backtrack_cells.discard((row, col))
                
                # Visual update for backtracking
                if update_display and screen:
                    self._update_visual_solving_callback(screen, box_x, box_y, cell_size)
                    
        return False

    def _update_visual_solving_callback(self, screen, box_x, box_y, cell_size):
        """Callback for visual updates - to be overridden or handled by GUI"""
        # This is a placeholder. The GUI will handle the actual rendering.
        pass
