import pygame
import sys

pygame.init()

# Screen dimensions and colors
SCREEN_WIDTH, SCREEN_HEIGHT = 900, 473
FONT_COLOR = (255, 255, 255)
BUTTON_COLOR = (255, 100, 50)
BUTTON_HOVER_COLOR = (255, 70, 30)
BUTTON_CLICK_COLOR = (200, 50, 20)
BUTTON_SHADOW_COLOR = (100, 50, 20)
BUTTON_WIDTH, BUTTON_HEIGHT = 200, 60

# Version and developer info
VERSION_TEXT = "v1.0.0"
DEVELOPER_NOTES = "Developed by BOT_MATRIX"

# Initialize Pygame screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("UNO Cards By BOT_MATRIX")

# Load fonts
font = pygame.font.Font(None, 48)
small_font = pygame.font.Font(None, 24)

# Load background image and scale it
background_image = pygame.image.load("game_background.jpg")
background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Load sounds and music
pygame.mixer.music.load("game_background.mp3")
pygame.mixer.music.set_volume(0.5)
click_sound = pygame.mixer.Sound("button-click.mp3")
transition_sound = pygame.mixer.Sound("transition.wav")

# Play background music
pygame.mixer.music.play(-1)

# Function to draw text on the screen
def draw_text(text, pos, color=FONT_COLOR, font=font):
    rendered_text = font.render(text, True, color)
    screen.blit(rendered_text, pos)

# Function to handle button drawing and hover states
def draw_button(text, pos, mouse_pos, is_clicked):
    button_rect = pygame.Rect(0, 0, BUTTON_WIDTH, BUTTON_HEIGHT)
    button_rect.center = pos

    # Check hover and click state
    color = BUTTON_HOVER_COLOR if button_rect.collidepoint(mouse_pos) else BUTTON_COLOR
    if is_clicked and button_rect.collidepoint(mouse_pos):
        color = BUTTON_CLICK_COLOR

    # Draw shadow for button
    shadow_rect = button_rect.copy()
    shadow_rect.move_ip(5, 5)
    pygame.draw.rect(screen, BUTTON_SHADOW_COLOR, shadow_rect, border_radius=15)

    # Draw main button with rounded corners
    pygame.draw.rect(screen, color, button_rect, border_radius=15)

    # Render and center the button text
    text_render = font.render(text, True, FONT_COLOR)
    text_rect = text_render.get_rect(center=button_rect.center)
    screen.blit(text_render, text_rect)

    return button_rect

# Function for fading the screen
def fade_out(duration=1000):
    fade_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    fade_surface.fill((0, 0, 0))
    for alpha in range(0, 255):
        fade_surface.set_alpha(alpha)
        screen.blit(background_image, (0, 0))
        screen.blit(fade_surface, (0, 0))
        pygame.display.update()
        pygame.time.delay(duration // 255)

def fade_in(duration=1000):
    fade_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    fade_surface.fill((0, 0, 0))
    for alpha in range(255, -1, -1):
        fade_surface.set_alpha(alpha)
        screen.blit(background_image, (0, 0))
        screen.blit(fade_surface, (0, 0))
        pygame.display.update()
        pygame.time.delay(duration // 255)

# Main menu function
def main_menu():
    menu_running = True
    while menu_running:
        screen.blit(background_image, (0, 0))

        # Draw version and developer info
        draw_text(VERSION_TEXT, (10, 10), (180, 180, 180), small_font)
        draw_text(DEVELOPER_NOTES, (10, SCREEN_HEIGHT - 30), (180, 180, 180), small_font)

        # Get mouse position
        mouse_pos = pygame.mouse.get_pos()
        is_clicked = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                is_clicked = True  # Only register a click on MOUSEBUTTONDOWN

        # Draw buttons and handle clicks
        start_button = draw_button("Start Game", (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50), mouse_pos, is_clicked)
        if start_button.collidepoint(mouse_pos) and is_clicked:
            click_sound.play()
            fade_out(700)
            transition_sound.play()
            fade_in(700)
            game_screen()  # Transition to game screen

        quit_button = draw_button("Quit", (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50), mouse_pos, is_clicked)
        if quit_button.collidepoint(mouse_pos) and is_clicked:
            click_sound.play()
            fade_out(700)
            pygame.quit()
            sys.exit()

        pygame.display.flip()

# Game screen with transition effect
def game_screen():
    game_running = True
    while game_running:
        screen.blit(background_image, (0, 0))

        # Get mouse position
        mouse_pos = pygame.mouse.get_pos()
        is_clicked = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                is_clicked = True  # Only register a click on MOUSEBUTTONDOWN

        # Draw buttons and handle clicks
        camera_button = draw_button("Camera", (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 70), mouse_pos, is_clicked)
        if camera_button.collidepoint(mouse_pos) and is_clicked:
            click_sound.play()
            print("Camera Capture selected")

        upload_button = draw_button("Image", (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2), mouse_pos, is_clicked)
        if upload_button.collidepoint(mouse_pos) and is_clicked:
            click_sound.play()
            print("Image Upload selected")

        exit_button = draw_button("Back", (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 70), mouse_pos, is_clicked)
        if exit_button.collidepoint(mouse_pos) and is_clicked:
            click_sound.play()
            fade_out(700)
            transition_sound.play()
            fade_in(700)
            main_menu()

        pygame.display.flip()

# Start the menu, then the game
main_menu()

# Stop the music and exit Pygame
pygame.mixer.music.stop()
pygame.quit()
sys.exit()
