import pygame as py
import random
import time

py.init()

# Constants
WIDTH, HEIGHT = 800, 600
FPS = 60

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
DARK_BLUE = (0, 0, 139)

screen = py.display.set_mode((WIDTH, HEIGHT), py.RESIZABLE)
py.display.set_caption('Limbo!')

# Fonts
py.font.init()
font = py.font.Font(None, 50)  # Default font, size 50

# Define main square properties
square_size = 500
square_x = (WIDTH - square_size) // 2
square_y = (HEIGHT - square_size) // 2

# Grid properties
rows, cols = 4, 4  # 4x4 grid
cell_size = square_size // rows  # Each smaller square's size

# Game variables
sequence = []  # Stores the correct sequence of boxes
player_index = 0  # Tracks player's position in sequence
score = 0
waiting_for_input = False  # Determines if the game is waiting for player input


def draw_grid():
    """Draws the main grid, outer square, and score."""
    screen.fill(WHITE)

    # Draw outer square
    py.draw.rect(screen, BLACK, (square_x, square_y, square_size, square_size), 5)

    # Draw grid lines inside the big square
    for i in range(1, rows):  # Vertical lines
        x = square_x + i * cell_size
        py.draw.line(screen, BLACK, (x, square_y), (x, square_y + square_size), 3)

    for j in range(1, cols):  # Horizontal lines
        y = square_y + j * cell_size
        py.draw.line(screen, BLACK, (square_x, y), (square_x + square_size, y), 3)

    # Draw score at the top center
    score_text = font.render(f"Score: {score}", True, BLACK)
    text_rect = score_text.get_rect(center=(WIDTH // 2, 30))
    screen.blit(score_text, text_rect)


def flash_sequence():
    """Flashes the sequence of boxes for the player to remember."""
    for (row, col) in sequence:
        draw_grid()
        flash_x = square_x + col * cell_size
        flash_y = square_y + row * cell_size
        py.draw.rect(screen, RED, (flash_x, flash_y, cell_size, cell_size))
        py.display.flip()
        time.sleep(0.5)  # Flash for 0.5 seconds
        draw_grid()
        py.display.flip()
        time.sleep(0.3)  # Pause before next flash


def vibrate_screen():
    """Simulates screen vibration when the player makes a mistake."""
    for _ in range(10):  # Vibrate 10 times
        offset_x = random.randint(-5, 5)
        offset_y = random.randint(-5, 5)
        screen.fill(WHITE)
        py.display.set_mode((WIDTH + offset_x, HEIGHT + offset_y))
        draw_grid()
        py.display.flip()
        time.sleep(0.02)
    py.display.set_mode((WIDTH, HEIGHT))  # Reset screen


def generate_new_sequence():
    """Creates a completely new randomized sequence based on the current score."""
    global sequence
    sequence = [(random.randint(0, rows - 1), random.randint(0, cols - 1)) for _ in range(score + 1)]
    random.shuffle(sequence)  # Shuffle to make it more unpredictable


def highlight_player_click(row, col):
    """Highlights the player's clicked box with Dark Blue for 0.5 seconds."""
    draw_grid()
    click_x = square_x + col * cell_size
    click_y = square_y + row * cell_size
    py.draw.rect(screen, DARK_BLUE, (click_x, click_y, cell_size, cell_size))
    py.display.flip()
    time.sleep(0.5)  # Show Dark Blue for 0.5 seconds
    draw_grid()
    py.display.flip()


def main():
    global sequence, player_index, score, waiting_for_input

    clock = py.time.Clock()
    run = True

    # Start with 1 random box
    score = 0
    generate_new_sequence()
    waiting_for_input = False  # Show sequence first

    while run:
        draw_grid()

        if not waiting_for_input:
            time.sleep(0.5)
            flash_sequence()
            player_index = 0  # Reset player input tracker
            waiting_for_input = True  # Now wait for player clicks

        for event in py.event.get():
            if event.type == py.QUIT:
                run = False

            if event.type == py.MOUSEBUTTONDOWN and waiting_for_input:
                mx, my = py.mouse.get_pos()

                # Check which grid cell was clicked
                clicked_col = (mx - square_x) // cell_size
                clicked_row = (my - square_y) // cell_size

                # Ignore clicks outside the grid
                if not (0 <= clicked_row < rows and 0 <= clicked_col < cols):
                    continue

                # Highlight player's click
                highlight_player_click(clicked_row, clicked_col)

                # Check if the player clicked the correct box in sequence
                if (clicked_row, clicked_col) == sequence[player_index]:
                    player_index += 1
                    if player_index == len(sequence):  # Completed sequence correctly
                        score += 1
                        generate_new_sequence()  # Create a new randomized sequence
                        waiting_for_input = False  # Show new sequence
                else:
                    # Player clicked the wrong box
                    score = 0
                    generate_new_sequence()  # Restart with new first box
                    vibrate_screen()
                    waiting_for_input = False  # Restart game from 1

        py.display.flip()
        clock.tick(FPS)

    py.quit()

if __name__ == "__main__":
    main()