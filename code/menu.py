from settings import *
from level import Level
from main import Gameplay
from pytmx.util_pygame import load_pygame
from os.path import join
from data import Data
import os

pygame.init() # Initialize all imported Pygame modules
pygame.mixer.init()

screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
clock = pygame.time.Clock()

# Initialize screen
class Game:
    def __init__(self):
        pygame.init()
        # Create the main display surface with the specified window width and height

        pygame.mixer.music.load('menu_music.wav')
        pygame.mixer.music.play(-1)  # -1 loops forever
        
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Platformer Panic") # Set the window title
        self.clock = pygame.time.Clock()

        
    def run(self):
        running = True  # Flag to control the main game loop
        while running:  # Main game loop
            screen.blit(menu_bg, (0, 0))  # Draw the background image
            draw_title("Platformer Panic", 100, "rockybilly.ttf", 48, WHITE)  # Draw the game title
            # Draw menu buttons
            start_button.draw(screen)
            instructions_button.draw(screen)
            quit_button.draw(screen)
            # Process events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False  # Exit the game loop if window is closed
                if event.type == pygame.MOUSEBUTTONDOWN:  # Check for mouse click
                    # Check if any button is clicked and perform the corresponding action
                    if start_button.is_clicked(event.pos):
                        level_select()
                    elif instructions_button.is_clicked(event.pos):
                        instructions_screen()
                    elif quit_button.is_clicked(event.pos):
                        running = False  # Exit the game loop

            pygame.display.update() # Update the contents of the entire display

# Load images and scale them
menu_bg = pygame.transform.scale(pygame.image.load("menu_bg.jpg"), (WINDOW_WIDTH, WINDOW_HEIGHT))
button_img = pygame.transform.scale(pygame.image.load("button.png"), (200, 60))

# Load custom font
font = pygame.font.Font("cool_font.ttf", 36)

# Function to draw a title text at a specific vertical position (y)
def draw_title(text, y, font, size, colour):
    title_font = pygame.font.Font(font, size) # Load the custom font from the specified path and size
    title_surface = title_font.render(text, True, colour) # Render the text with a specific color
    title_rect = title_surface.get_rect(center=(WINDOW_WIDTH // 2, y)) # Get the rectangle of the rendered text and center it horizontally
    screen.blit(title_surface, title_rect) # Draw the text surface onto the screen

# Button Class
class Button:
    def __init__(self, x, y, image, text, color, scale=1.5):
        # Scale the image to increase button size
        width = int(image.get_width() * scale)
        height = int(image.get_height() * scale)
        self.image = pygame.transform.scale(image.copy(), (width, height))
        self.image.fill(color, special_flags=pygame.BLEND_MULT)

        self.rect = self.image.get_rect(center=(x, y))
        self.text = text
        self.color = color

    def draw(self, surface):
        surface.blit(self.image, self.rect)
        text_surface = font.render(self.text, True, WHITE)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

class IconButton:
    def __init__(self, x, y, size, color, text):
        # Create the button surface with given size and fill it with the color
        self.image = pygame.Surface((size, size))
        self.image.fill(color)
        # Get the rectangle for positioning and center it at (x, y)
        self.rect = self.image.get_rect(center=(x, y))
        self.text = text
        # Use a simple font sized to fit nicely inside the button
        self.font = pygame.font.Font(None, size - 10)

    def draw(self, surface):
        # Draw the button rectangle
        surface.blit(self.image, self.rect)
        text_surface = self.font.render(self.text, True, BLACK)
        # Center the text on the button
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

# Main Menu
start_button = Button(WINDOW_WIDTH // 2, 250, button_img, "Start", GREEN)
instructions_button = Button(WINDOW_WIDTH // 2, 400, button_img, "Instructions", (0, 0, 255))
quit_button = Button(WINDOW_WIDTH // 2, 550, button_img, "Quit", WHITE)

# Level Select Menu
def level_select():
    running = True

    # Create level buttons shifted left for spacing
    level1_button = Button(WINDOW_WIDTH // 2 , 150, button_img, "Phobia 1", WHITE)
    level2_button = Button(WINDOW_WIDTH // 2 , 250, button_img, "Phobia 2", WHITE)
    level3_button = Button(WINDOW_WIDTH // 2 , 350, button_img, "Phobia 3", WHITE)
    level4_button = Button(WINDOW_WIDTH // 2 , 450, button_img, "Phobia 4", WHITE)
    level5_button = Button(WINDOW_WIDTH // 2 , 550, button_img, "Phobia 5", WHITE)

    # Add small trophy icon buttons (yellow squares)
    leaderboard1_icon = IconButton(WINDOW_WIDTH // 2 + 200, 150, 40, YELLOW, "L")
    leaderboard2_icon = IconButton(WINDOW_WIDTH // 2 + 200, 250, 40, YELLOW, "L")
    leaderboard3_icon = IconButton(WINDOW_WIDTH // 2 + 200, 350, 40, YELLOW, "L")
    leaderboard4_icon = IconButton(WINDOW_WIDTH // 2 + 200, 450, 40, YELLOW, "L")
    leaderboard5_icon = IconButton(WINDOW_WIDTH // 2 + 200, 550, 40, YELLOW, "L")

    back_button = Button(WINDOW_WIDTH // 2, 650, button_img, "Back", WHITE)

    while running:
        screen.blit(menu_bg, (0, 0))
        draw_title("Select a Level", 50, "Dearly.otf", 48, WHITE)

        # Draw level buttons
        level1_button.draw(screen)
        level2_button.draw(screen)
        level3_button.draw(screen)
        level4_button.draw(screen)
        level5_button.draw(screen)

        # Draw trophy icon buttons
        leaderboard1_icon.draw(screen)
        leaderboard2_icon.draw(screen)
        leaderboard3_icon.draw(screen)
        leaderboard4_icon.draw(screen)
        leaderboard5_icon.draw(screen)

        back_button.draw(screen)

        for event in pygame.event.get(): # Handle user input events
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if level1_button.is_clicked(event.pos):
                    info_screen(level_index=1)  
                elif leaderboard1_icon.is_clicked(event.pos):
                    show_leaderboard(level_index=1)
                elif level2_button.is_clicked(event.pos):
                    info_screen(level_index=2)
                elif leaderboard2_icon.is_clicked(event.pos):
                    show_leaderboard(level_index=2)
                elif level3_button.is_clicked(event.pos):
                    info_screen(level_index=3)
                elif leaderboard3_icon.is_clicked(event.pos):
                    show_leaderboard(level_index=3)
                elif level4_button.is_clicked(event.pos):
                    info_screen(level_index=4)
                elif leaderboard4_icon.is_clicked(event.pos):
                    show_leaderboard(level_index=4)
                elif level5_button.is_clicked(event.pos):
                    info_screen(level_index=5)
                elif leaderboard5_icon.is_clicked(event.pos):
                    show_leaderboard(level_index=5)
                elif back_button.is_clicked(event.pos):
                    return
              
        pygame.display.flip()  # Update the screen with all drawings

# Instructions Screen
def instructions_screen():
    running = True # Keeps the instruction screen active
    back_button = Button(WINDOW_WIDTH // 2, 500, button_img, "Back", WHITE)
    # List of instruction lines to display
    instructions_text = [ 
        "Use arrow keys to move left and right",
        "Press up arrow to jump",
        "Press X to deflect",
        "Press down arrow to move through platforms"
    ] 

    while running:
        screen.fill(WHITE) # Clear the screen with white background
        draw_title("Instructions", 100, "Dearly.otf", 48, BLACK) # Draw the title at the top
        # Render each instruction line
        for i, line in enumerate(instructions_text):
            text_surface = font.render(line, True, BLACK) # Create text surface
            text_rect = text_surface.get_rect(center=(WINDOW_WIDTH // 2, 200 + i * 50)) # Center it vertically
            screen.blit(text_surface, text_rect) # Draw the text on screen
        back_button.draw(screen) # Draw the back button
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_button.is_clicked(event.pos):
                    return # Exit the instructions screen and return to previous menu
        
        pygame.display.flip() # Update the display

def info_screen(level_index):
    # Display an information screen for the selected level before difficulty selection.
    # Shows level-specific text and an optional image.
    running = True

    # Text for each level index
    level_info = [
        "This is a test level ._.",
        "Acrophobia\nFace your fear of heights by traversing platforms.\nThe prescribed relaxant can heal you. (Treatment for acrophobia)",
        "Arachnophobia\nConquer your fear of spiders! (A common fear)\nPress the X key to repel them (whilst facing them).",
        "Thalassophobia\nEscape the clutches of the ocean.\nPanic attacks, anxiety, and physical symptoms when near deep water.",
        "Coulrophobia\nWho likes clowns?\n(Not a lot of people!)",
        "Thanatophobia\nFear of Death\nTreatment: Therapy"
    ]

    # Load different images or None for each level
    level_images = [
        None,
        pygame.transform.scale(pygame.image.load("relax.png"), (100, 100)),
        pygame.transform.scale(pygame.image.load("spider.png"), (100, 100)),
        pygame.transform.scale(pygame.image.load("boat.png"), (300, 100)),
        pygame.transform.scale(pygame.image.load("clown.png"), (200, 150)),  
        None # No image for this level
    ]

    info_image = level_images[level_index]
    text_lines = level_info[level_index].split('\n')
    info_font = pygame.font.Font("cool_font.ttf", 32)

    # Buttons
    continue_button = Button(WINDOW_WIDTH // 2, 550, button_img, "Continue", GREEN)
    back_button = Button(WINDOW_WIDTH // 2, 650, button_img, "Back", (255, 0, 0))  # Red back button

    while running:
        screen.fill(WHITE)  # White background for readability

        # Draw the title
        draw_title("Information", 50, "Dearly.otf", 48, BLACK)

         # Draw the image if it exists
        if info_image:
            screen.blit(info_image, (WINDOW_WIDTH // 2 - info_image.get_width() // 2, 120))

        # Calculate starting Y to vertically center the block
        line_height = font.get_height()
        total_height = len(text_lines) * line_height + (len(text_lines) - 1) * 10  # 10px spacing

        start_y = (WINDOW_HEIGHT // 2) - (total_height // 2)

        for i, line in enumerate(text_lines):
            text_surface = font.render(line, True, BLACK)
            text_rect = text_surface.get_rect(center=(WINDOW_WIDTH // 2, start_y + i * (line_height + 10)))
            screen.blit(text_surface, text_rect)

        # Draw buttons
        continue_button.draw(screen)
        back_button.draw(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if continue_button.is_clicked(event.pos):
                    difficulty_select(level_index)  # Go to difficulty select
                    return
                elif back_button.is_clicked(event.pos):
                    return  # Go back to level select

        pygame.display.flip()


def difficulty_select(level_index):
    running = True
    difficulty = "Easy"  # Default difficulty
    # Define inactive (greyed out) color
    GRAY = (128, 128, 128)
    # Create buttons for each difficulty level
    easy_button = Button(WINDOW_WIDTH // 2, 250, button_img, "Easy", GREEN)  # Active
    normal_button = Button(WINDOW_WIDTH // 2, 350, button_img, "Normal", YELLOW)  # Inactive for now
    hard_button = Button(WINDOW_WIDTH // 2, 450, button_img, "Hard", GRAY)  # Inactive
    confirm_button = Button(WINDOW_WIDTH // 2, 550, button_img, "Confirm", WHITE)  # Confirm selection
    confirm_button.image.fill(WHITE, special_flags=pygame.BLEND_RGB_ADD) # Apply white tint
    while running:
        screen.fill(BLACK)  # Clear the screen with black background
        # Draw the title
        draw_title("Select Difficulty", 100, "cs_dumber.otf", 60, WHITE)
        # Draw all buttons on the screen
        easy_button.draw(screen)
        normal_button.draw(screen)
        hard_button.draw(screen)
        confirm_button.draw(screen)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Only Easy is interactable
                if easy_button.is_clicked(event.pos):
                    difficulty = "Easy"
                    # Visually highlight Easy and reset others to dim
                    easy_button.image.fill(GREEN, special_flags=pygame.BLEND_MULT)
                    normal_button.image.fill(GRAY, special_flags=pygame.BLEND_MULT)
                    hard_button.image.fill(GRAY, special_flags=pygame.BLEND_MULT)
                elif normal_button.is_clicked(event.pos):
                    difficulty = "Normal"
                    easy_button.image.fill(GRAY, special_flags=pygame.BLEND_MULT)
                    normal_button.image.fill(YELLOW, special_flags=pygame.BLEND_MULT)
                    hard_button.image.fill(GRAY, special_flags=pygame.BLEND_MULT)
                elif confirm_button.is_clicked(event.pos):
                    if difficulty == "Easy":
                        level_index = level_index
                    elif difficulty == "Normal":
                        level_index = level_index + 0.5
                    else:
                        level_index = level_index
                    # Proceed only if a difficulty is selected (default: Easy for now)
                    start_level(level_index, difficulty)

        pygame.display.flip()  # Update the display

def game_over_screen(final_score):
    # Initialize pygame and create the game over screen window
    pygame.init()
    screen = pygame.display.set_mode((1280, 720))

    # Load fonts for the main title and score text
    font = pygame.font.Font("rockybilly.ttf", 50)
    small_font = pygame.font.Font("cool_font.ttf", 36)

    pygame.mixer.music.stop()
    pygame.mixer.music.load('menu_music.wav')
    pygame.mixer.music.play(-1)

    # Render text surfaces
    game_over_text = font.render("GAME OVER", True, (255, 0, 0))
    score_text = small_font.render(f"Score: {final_score}", True, (255, 255, 255))

    # Create buttons
    retry_button = Button(WINDOW_WIDTH // 2, 300,button_img, "Retry",  WHITE)
    menu_button = Button(WINDOW_WIDTH // 2, 380,button_img, "Main Menu",  WHITE)
    quit_button = Button(WINDOW_WIDTH // 2, 460,button_img, "Quit",  WHITE)

    clock = pygame.time.Clock()
    running = True
    while running:
        screen.fill((0, 0, 0)) # Fill screen with black background
        # Draw game over and score text centered
        screen.blit(game_over_text, (screen.get_width() // 2 - game_over_text.get_width() // 2, 0))
        screen.blit(score_text, (screen.get_width() // 2 - score_text.get_width() // 2, 200))
        # Draw buttons
        retry_button.draw(screen)
        menu_button.draw(screen)
        quit_button.draw(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if retry_button.is_clicked(event.pos):
                    return "retry"
                if menu_button.is_clicked(event.pos):
                    return "menu"
                if quit_button.is_clicked(event.pos):
                    pygame.quit()
                    sys.exit()

        pygame.display.flip()

def win_screen(level_index, coins, health):
    # Displays the win screen after the player completes a level.
    # Shows coins, health, and score = coins * (health / 2).
    running = True

    # Calculate final score
    score = int(coins * (health / 2))

    pygame.mixer.music.stop()
    pygame.mixer.music.load('menu_music.wav')
    pygame.mixer.music.play(-1)

    # Create fonts
    title_font = pygame.font.Font("rockybilly.ttf", 60)
    info_font = pygame.font.Font("cool_font.ttf", 36)
    input_font = pygame.font.Font(None, 40)

    # Continue button
    continue_button = Button(WINDOW_WIDTH // 2, 400, button_img, "Continue", GREEN)

    # Name input
    entering_name = False
    player_name = ""

    while running:
        screen.fill((128, 128, 128))  # Grey background

        # Draw title
        title_surface = title_font.render("Level Complete!", True, BLACK)
        title_rect = title_surface.get_rect(center=(WINDOW_WIDTH // 2, 100))
        screen.blit(title_surface, title_rect)

        # Draw stats
        coins_surface = info_font.render(f"Coins: {coins}", True, BLACK)
        coins_rect = coins_surface.get_rect(center=(WINDOW_WIDTH // 2, 200))
        screen.blit(coins_surface, coins_rect)

        health_surface = info_font.render(f"Health: {health}", True, BLACK)
        health_rect = health_surface.get_rect(center=(WINDOW_WIDTH // 2, 250))
        screen.blit(health_surface, health_rect)

        score_surface = info_font.render(f"Score: {score}", True, BLACK)
        score_rect = score_surface.get_rect(center=(WINDOW_WIDTH // 2, 300))
        screen.blit(score_surface, score_rect)

        # Show name input prompt if needed
        if entering_name:
            prompt_surface = input_font.render("Enter your name:", True, BLACK)
            prompt_rect = prompt_surface.get_rect(center=(WINDOW_WIDTH // 2, 450))
            screen.blit(prompt_surface, prompt_rect)

            name_surface = input_font.render(player_name, True, BLACK)
            name_rect = name_surface.get_rect(center=(WINDOW_WIDTH // 2, 500))
            screen.blit(name_surface, name_rect)
        else:
            continue_button.draw(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if entering_name:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        # Save to level-specific leaderboard
                        leaderboard_file = f"leaderboard_level_{level_index}.txt"
                        with open(leaderboard_file, "a") as f:
                            f.write(f"{player_name},{score}\n")
                        show_leaderboard(level_index)
                    elif event.key == pygame.K_BACKSPACE:
                        player_name = player_name[:-1]
                    else:
                        if len(player_name) < 12:
                            player_name += event.unicode
            else:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if continue_button.is_clicked(event.pos):
                        entering_name = True

        pygame.display.flip()

def show_leaderboard(level_index):
    running = True

    leaderboard_file = f"leaderboard_level_{level_index}.txt"
    leaderboard = []
    if os.path.exists(leaderboard_file):
        with open(leaderboard_file, 'r') as file:
            for line in file:
                player_name, score = line.strip().split(',')
                leaderboard.append((player_name, int(score)))

    leaderboard.sort(key=lambda x: x[1], reverse=True)

    title_font = pygame.font.Font(None, 60)
    entry_font = pygame.font.Font(None, 40)

    # Only make Next Level button if not the final level
    max_level_index = 5  # Set your maximum level index here!
    show_next_level = level_index < max_level_index

    button_width = 250
    button_height = 60
    next_level_button_rect = pygame.Rect(
        (WINDOW_WIDTH // 2 - button_width // 2, 550),
        (button_width, button_height)
    )

    retry_level_button_rect = pygame.Rect(
    (WINDOW_WIDTH // 2 - button_width // 2, 450),
    (button_width, button_height)
    )

    while running:
        screen.fill(GREY)

        # Draw title
        title_surface = title_font.render(f"Leaderboard - Level {level_index}", True, BLACK)
        title_rect = title_surface.get_rect(center=(WINDOW_WIDTH // 2, 50))
        screen.blit(title_surface, title_rect)

        # Draw leaderboard entries
        for i, (player_name, score) in enumerate(leaderboard[:5]):
            entry_text = f"{i+1}. {player_name} - {score}"

            if i < 3:
                box_width = 400
                box_height = 50
                box_rect = pygame.Rect(0, 0, box_width, box_height)
                box_rect.center = (WINDOW_WIDTH // 2, 150 + i * 70)
                pygame.draw.rect(screen, GREEN, box_rect, border_radius=10)

                text_color = (255, 215, 0) if i == 0 else BLACK
            else:
                text_color = BLACK

            entry_surface = entry_font.render(entry_text, True, text_color)
            entry_rect = entry_surface.get_rect(center=(WINDOW_WIDTH // 2, 150 + i * 70))
            screen.blit(entry_surface, entry_rect)

        # Draw Next Level button if applicable
        if show_next_level:
            pygame.draw.rect(screen, GREEN, next_level_button_rect, border_radius=10)
            button_font = pygame.font.Font(None, 40)
            button_text = button_font.render("Next Level", True, BLACK)
            button_rect = button_text.get_rect(center=next_level_button_rect.center)
            screen.blit(button_text, button_rect)

        # Draw Retry Level button
        pygame.draw.rect(screen, RED, retry_level_button_rect, border_radius=10)
        button_font = pygame.font.Font(None, 40)
        retry_text = button_font.render("Retry Level", True, BLACK)
        retry_rect = retry_text.get_rect(center=retry_level_button_rect.center)
        screen.blit(retry_text, retry_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if show_next_level and event.type == pygame.MOUSEBUTTONDOWN:
                if retry_level_button_rect.collidepoint(event.pos):
                    if (level_index*10) % 2 == 0: 
                        difficulty_select(level_index) 
                    else:
                        difficulty_select(int(level_index - 0.5))
                    return
                elif next_level_button_rect.collidepoint(event.pos):
                    if (level_index*10) % 0.5 == 0: 
                        next_level_index = int(level_index + 1)
                        if next_level_index <= max_level_index:
                            info_screen(next_level_index)
                        else:
                            print("No more levels!")
                        return
                    else:
                        next_level_index = int(level_index + 0.5)
                        if next_level_index <= max_level_index:
                            info_screen(next_level_index)
                        else:
                            print("No more levels!")
                        return

        pygame.display.flip()

def start_level(level_index, difficulty):
    pygame.mixer.music.stop()

    gameplay = Gameplay(level_index=level_index)  # Pass index!
    gameplay.run()
    
# This ensures the following code only runs when the script is executed directly,and not when it's imported as a module in another script.
if __name__ == '__main__':
    game = Game() # Create an instance of the Game class
    game.run() # Start the game loop
