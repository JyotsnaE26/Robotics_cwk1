import pygame
import sys

pygame.init()

# Screen dimensions and colors
SCREEN_WIDTH, SCREEN_HEIGHT = 900, 473
FONT_COLOR = (255, 255, 255)
BUTTON_COLOR = (255, 100, 50)  # Warm reddish-orange button color
BUTTON_HOVER_COLOR = (255, 70, 30)  # Darker red-orange for hover effect
BUTTON_CLICK_COLOR = (200, 50, 20)  # Even darker color for click effect
BUTTON_SHADOW_COLOR = (100, 50, 20)  # Shadow color
BUTTON_WIDTH, BUTTON_HEIGHT = 200, 60

# Version and developer info
VERSION_TEXT = "v1.0.0"
DEVELOPER_NOTES = "Developed by BOT_MATRIX"

# Initialize Pygame screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("UNO Cards By BOT_MATRIX")

# Load font
font = pygame.font.Font(None, 48)
small_font = pygame.font.Font(None, 24)

# Load and scale background image
background_image = pygame.image.load("game_background.jpg")
background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Load background music
pygame.mixer.music.load("game_background.mp3")
pygame.mixer.music.set_volume(0.5)  # Set volume (0.0 to 1.0)
pygame.mixer.music.play(-1)  # Loop the music indefinitely

# Function to draw text on the screen
def draw_text(text, pos, color=FONT_COLOR, font=font):
    rendered_text = font.render(text, True, color)
    screen.blit(rendered_text, pos)

# Button setup
def draw_button(text, pos, mouse_pos, mouse_click):
    button_rect = pygame.Rect(0, 0, BUTTON_WIDTH, BUTTON_HEIGHT)
    button_rect.center = pos

    # Check hover and click state
    if button_rect.collidepoint(mouse_pos):
        color = BUTTON_CLICK_COLOR if mouse_click[0] else BUTTON_HOVER_COLOR
    else:
        color = BUTTON_COLOR

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

# Main menu function
def main_menu():
    menu_running = True
    while menu_running:
        screen.blit(background_image, (0, 0))  # Draw the background image

        # Draw version info at the extreme left
        draw_text(VERSION_TEXT, (10, 10), (180, 180, 180), small_font)

        # Draw developer notes at the bottom corner
        draw_text(DEVELOPER_NOTES, (10, SCREEN_HEIGHT - 30), (180, 180, 180), small_font)

        # Get mouse position and button press
        mouse_pos = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()

        # Draw Start button and check if clicked
        start_button = draw_button("Start Game", (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50), mouse_pos, mouse_click)
        if start_button.collidepoint(mouse_pos) and mouse_click[0]:
            game_screen()  # Open game screen when Start Game is clicked

        # Draw Quit button and check if clicked
        quit_button = draw_button("Quit", (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50), mouse_pos, mouse_click)
        if quit_button.collidepoint(mouse_pos) and mouse_click[0]:
            pygame.quit()
            sys.exit()  # Exit the game when clicked

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.flip()  # Update display

# Game screen function with "Camera Capture," "Image Upload," and "Exit" buttons
def game_screen():
    game_running = True
    while game_running:
        screen.blit(background_image, (0, 0))  # Draw the background image

        # Get mouse position and button press
        mouse_pos = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()

        # Draw Camera Capture button and check if clicked
        camera_button = draw_button("Camera", (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 70), mouse_pos, mouse_click)
        if camera_button.collidepoint(mouse_pos) and mouse_click[0]:
            print("Camera Capture selected")  # Placeholder action for Camera Capture

        # Draw Image Upload button and check if clicked
        upload_button = draw_button("Image", (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2), mouse_pos, mouse_click)
        if upload_button.collidepoint(mouse_pos) and mouse_click[0]:
            print("Image Upload selected")  # Placeholder action for Image Upload

        # Draw Exit button and check if clicked
        exit_button = draw_button("Exit", (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 70), mouse_pos, mouse_click)
        if exit_button.collidepoint(mouse_pos) and mouse_click[0]:
            pygame.quit()
            sys.exit()  # Exit the game when Exit is clicked

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.flip()  # Update display

# Start the menu, then the game
main_menu()

# Stop the music and exit Pygame
pygame.mixer.music.stop()
pygame.quit()
sys.exit()
