import pygame
import sys
import random
import copy
import time
import os
from sudoku_core import Sudoku

# Initialize Pygame
pygame.init()

# Start in windowed mode (not fullscreen)
is_fullscreen = False
screen = pygame.display.set_mode((1400, 900))
screen_width, screen_height = 1400, 900
pygame.display.set_caption("Sudoku Solver")

# Colors and Fonts
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARK_GRAY = (50, 50, 50)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
PURPLE = (128, 0, 128)
LIGHT_BLUE = (173, 216, 230)

title_font = pygame.font.SysFont("freestyle script", 100, bold=True) or pygame.font.SysFont("Comic Sans MS", 90, bold=True)
button_font = pygame.font.SysFont("Comic Sans MS", 40, bold=True)
small_font = pygame.font.SysFont("arial", 24)

# Load background
script_dir = os.path.dirname(os.path.abspath(__file__))
bg_path = os.path.join(script_dir, "Bg1.png")

try:
    bg_image = pygame.image.load(bg_path)
    bg_image = pygame.transform.scale(bg_image, (screen_width, screen_height))
except FileNotFoundError:
    print(f"Bg1.png not found at: {bg_path}")
    bg_image = pygame.Surface((screen_width, screen_height))
    bg_image.fill((50, 50, 70))  # Fallback dark background


def draw_button(text, x, y, width, height, color=WHITE, border_radius=20):
    mouse_pos = pygame.mouse.get_pos()
    hovered = pygame.Rect(x, y, width, height).collidepoint(mouse_pos)
    text_color = BLUE if hovered else color

    label = button_font.render(text, True, text_color)
    label_rect = label.get_rect(center=(x + width // 2, y + height // 2))
    screen.blit(label, label_rect)

    return pygame.Rect(x, y, width, height)


def update_visual_solving(game, screen, box_x, box_y, cell_size):
    """Update the display during solving process with complete grid redraw."""
    # Create a fresh surface for the grid
    grid_surface = pygame.Surface((9 * cell_size, 9 * cell_size))
    grid_surface.fill((255, 255, 255))  # White background
    
    # Draw all grid lines
    for i in range(10):
        line_width = 4 if i % 3 == 0 else 1
        # Vertical lines
        pygame.draw.line(grid_surface, BLACK, 
                       (i * cell_size, 0), 
                       (i * cell_size, 9 * cell_size), line_width)
        # Horizontal lines
        pygame.draw.line(grid_surface, BLACK, 
                       (0, i * cell_size), 
                       (9 * cell_size, i * cell_size), line_width)
    
    # Draw all numbers with appropriate colors
    for row in range(9):
        for col in range(9):
            value = game.grid[row][col]
            if value != 0:
                # Determine color based on cell type
                if game.original_grid and game.original_grid[row][col] != 0:
                    # Original puzzle numbers
                    color = BLACK
                elif game.solving_complete:
                    # All solved numbers get random colors when complete
                    color = random.choice(game.random_colors)
                elif (row, col) in game.csp_cells:
                    # CSP solved cells
                    color = game.get_random_color('csp')
                elif (row, col) in game.backtrack_cells:
                    # Backtracking solved cells
                    color = game.get_random_color('backtrack')
                else:
                    # Default color for any other solved cells
                    color = random.choice(game.random_colors)
                    
                # Render and center the number in the cell
                num_surface = button_font.render(str(value), True, color)
                num_rect = num_surface.get_rect(
                    center=(col * cell_size + cell_size // 2,
                           row * cell_size + cell_size // 2))
                grid_surface.blit(num_surface, num_rect)
    
    # Blit the complete grid surface to the screen
    screen.blit(grid_surface, (box_x, box_y))
    pygame.display.flip()
    time.sleep(0.05)  # Shorter delay for smoother animation


def show_settings():
    global screen, screen_width, screen_height

    running = True
    box_width, box_height = 500, 300
    box_x = (screen_width - box_width) // 2
    box_y = (screen_height - box_height) // 2

    while running:
        # Fullscreen background stays as the main bg_image
        screen.blit(bg_image, (0, 0))

        # Dark overlay behind the settings box
        overlay = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        screen.blit(overlay, (0, 0))

        # Transparent modal box with rounded corners
        modal_surface = pygame.Surface((box_width, box_height), pygame.SRCALPHA)
        pygame.draw.rect(modal_surface, (255, 255, 255, 100), (0, 0, box_width, box_height), border_radius=20)
        screen.blit(modal_surface, (box_x, box_y))

        # Layout
        spacing = 60
        start_y = box_y + 70

        # Buttons
        info_rect = draw_button("Info", box_x + 140, start_y, 220, 50)
        close_rect = draw_button("Close", box_x + 140, start_y + spacing + 10, 220, 50)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if info_rect.collidepoint(event.pos):
                    show_info()
                elif close_rect.collidepoint(event.pos):
                    running = False

        pygame.display.flip()

def show_info():
    global screen, screen_width, screen_height

    info_running = True
    box_width, box_height = 600, 450
    box_x = (screen_width - box_width) // 2
    box_y = (screen_height - box_height) // 2

    info_text = [
        "Enhanced Sudoku Solver v2.1",
        "Hybrid algorithm with advanced CSP techniques",
        "and intelligent backtracking for all difficulties.",
        "",
        "Features:",
        "• Naked Singles: Cells with only one possibility", 
        "• Hidden Singles: Numbers with only one position",
        "• Minimum Remaining Values (MRV) heuristic",
        "• Complete grid validation and redraw",
        "• Random vibrant colors for visual appeal",
        "",
        "Color System:",
        "Random vibrant colors distinguish CSP vs Backtracking"
    ]

    while info_running:
        screen.blit(bg_image, (0, 0))

        overlay = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))  # Dark overlay
        screen.blit(overlay, (0, 0))

        # Modal info box
        info_surface = pygame.Surface((box_width, box_height), pygame.SRCALPHA)
        info_surface.fill((0, 0, 0, 0))  # Fully transparent initially
        pygame.draw.rect(info_surface, (255, 255, 255, 60), (0, 0, box_width, box_height), border_radius=20)
        screen.blit(info_surface, (box_x, box_y))

        # Draw info text
        for idx, line in enumerate(info_text):
            line_surface = small_font.render(line, True, WHITE)
            line_rect = line_surface.get_rect(center=(screen_width // 2, box_y + 30 + idx * 30))
            screen.blit(line_surface, line_rect)

        # Close button
        close_rect = draw_button("Close", box_x + (box_width - 200) // 2, box_y + box_height - 60, 200, 50)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if close_rect.collidepoint(event.pos):
                    info_running = False

        pygame.display.flip()


def landing_screen():
    button_width, button_height = 220, 60
    spacing = 40
    total_height = 3 * button_height + 2 * spacing
    start_y = (screen_height - total_height) // 2
    x_center = (screen_width - button_width) // 2

    while True:
        screen.blit(bg_image, (0, 0))

        title_surface = title_font.render("SUDOKU SOLVER", True, WHITE)
        screen.blit(title_surface, title_surface.get_rect(center=(screen_width // 2, screen_height // 6)))

        start_rect = draw_button("START", x_center, start_y, button_width, button_height)
        settings_rect = draw_button("SETTING", x_center, start_y + button_height + spacing, button_width, button_height)
        exit_rect = draw_button("EXIT", x_center, start_y + 2 * (button_height + spacing), button_width, button_height)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if start_rect.collidepoint(event.pos):
                    difficulty_screen()
                elif settings_rect.collidepoint(event.pos):
                    show_settings()
                elif exit_rect.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()

        pygame.display.flip()
        
def difficulty_screen():
    button_width, button_height = 220, 60
    spacing = 30
    total_height = 4 * button_height + 3 * spacing
    start_y = (screen_height - total_height) // 2
    x_center = (screen_width - button_width) // 2

    buttons = {
        "Easy": (x_center, start_y),
        "Medium": (x_center, start_y + (button_height + spacing)),
        "Hard": (x_center, start_y + 2 * (button_height + spacing)),
        "Back": (x_center, start_y + 3 * (button_height + spacing)),
    }

    while True:
        screen.blit(bg_image, (0, 0))

        title = title_font.render("Select Difficulty", True, WHITE)
        screen.blit(title, title.get_rect(center=(screen_width // 2, screen_height // 6)))

        for name, (x, y) in buttons.items():
            draw_button(name, x, y, button_width, button_height)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for name, (x, y) in buttons.items():
                    if pygame.Rect(x, y, button_width, button_height).collidepoint(event.pos):
                        if name == "Back":
                            return  # Return to landing screen
                        else:
                            game = Sudoku()
                            game.generate_puzzle(difficulty=name.lower())
                            show_grid_modal(game)

        pygame.display.flip()

def show_grid_modal(game):
    modal_width, modal_height = 540, 720
    box_x = (screen_width - modal_width) // 2
    box_y = (screen_height - modal_height) // 2

    cell_size = 60
    solving_active = False
    
    running = True
    while running:
        screen.blit(bg_image, (0, 0))

        # Dimmed background
        overlay = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        screen.blit(overlay, (0, 0))

        # Transparent modal with rounded corners
        modal_surface = pygame.Surface((modal_width, modal_height), pygame.SRCALPHA)
        pygame.draw.rect(modal_surface, (255, 255, 255, 70), (0, 0, modal_width, modal_height), border_radius=20)
        screen.blit(modal_surface, (box_x, box_y))

        # Draw Sudoku Grid Numbers (only when not actively solving)
        if not solving_active:
            # Clear the grid area with white background
            grid_surface = pygame.Surface((9 * cell_size, 9 * cell_size))
            grid_surface.fill((255, 255, 255))
            screen.blit(grid_surface, (box_x, box_y))
            
            # Draw numbers
            for row in range(9):
                for col in range(9):
                    value = game.grid[row][col]
                    if value != 0:
                        num_surface = button_font.render(str(value), True, BLACK)
                        num_rect = num_surface.get_rect(center=(box_x + col * cell_size + cell_size // 2,
                                                              box_y + row * cell_size + cell_size // 2))
                        screen.blit(num_surface, num_rect)

        # Draw Grid Lines
        for i in range(10):
            line_width = 4 if i % 3 == 0 else 1
            pygame.draw.line(screen, BLACK, (box_x + i * cell_size, box_y),
                             (box_x + i * cell_size, box_y + 9 * cell_size), line_width)
            pygame.draw.line(screen, BLACK, (box_x, box_y + i * cell_size),
                             (box_x + 9 * cell_size, box_y + i * cell_size), line_width)

        # Draw Buttons
        back_rect = draw_button("Back", box_x + 100, box_y + 580, 140, 40)
        solve_rect = draw_button("Solve", box_x + 300, box_y + 580, 140, 40)
        new_puzzle_rect = draw_button("New Puzzle", box_x + 170, box_y + 630, 200, 40)

        # Event Handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and not solving_active:
                if back_rect.collidepoint(event.pos):
                    running = False
                elif solve_rect.collidepoint(event.pos):
                    solving_active = True
                    # Reset solving state
                    game.original_grid = copy.deepcopy(game.grid)
                    game.backtrack_cells = set()
                    game.csp_cells = set()
                    game.solving_complete = False
                    game.random_colors = game.generate_random_colors()
                    
                    # Inject the GUI's update function into the game object
                    game._update_visual_solving_callback = lambda s, bx, by, cs: update_visual_solving(game, screen, box_x, box_y, cell_size)
                    
                    # Solve with visual updates
                    game.solve(screen, box_x, box_y, cell_size, True)
                    solving_active = False
                elif new_puzzle_rect.collidepoint(event.pos):
                    # Generate a new puzzle of the same difficulty
                    current_difficulty = "medium"  # Default
                    # Determine current difficulty based on empty cells
                    if game.original_grid:
                        empty_count = sum(1 for row in game.original_grid for cell in row if cell == 0)
                        if empty_count <= 40:
                            current_difficulty = "easy"
                        elif empty_count <= 50:
                            current_difficulty = "medium"
                        else:
                            current_difficulty = "hard"
                    
                    game.generate_puzzle(current_difficulty)

        pygame.display.flip()
        
# Start the game
landing_screen()