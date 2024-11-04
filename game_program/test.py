import pygame
import sys
import cv2
from tkinter import Tk, filedialog

# Initialize Pygame
pygame.init()

# Screen dimensions and colors
SCREEN_WIDTH, SCREEN_HEIGHT = 900, 473  # Adjusted to match background image size
FONT_COLOR = (255, 255, 255)
BUTTON_COLOR = (50, 150, 255)
BUTTON_HOVER_COLOR = (30, 120, 230)

# Set up the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("UNO Card Recognition")

# Load font
font = pygame.font.Font(None, 48)

# Load and scale the background image
background_image = pygame.image.load("game_background.jpg")  # Change this to your image path
background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Function to draw text on the screen
def draw_text(text, pos, color=FONT_COLOR):
    rendered_text = font.render(text, True, color)
    screen.blit(rendered_text, pos)

# Function to create buttons with animations
def draw_button(text, pos, color, hover_color, scale_factor=1.1):
    mouse = pygame.mouse.get_pos()
    button_rect = pygame.Rect(pos[0], pos[1], 200, 50)

    # Check for hover effect
    if button_rect.collidepoint(mouse):
        scaled_rect = button_rect.inflate((button_rect.width * (scale_factor - 1), button_rect.height * (scale_factor - 1)))
        pygame.draw.rect(screen, hover_color, scaled_rect, border_radius=10)
    else:
        pygame.draw.rect(screen, color, button_rect, border_radius=10)

    draw_text(text, (pos[0] + 20, pos[1] + 10))

    return button_rect  # Return the button rectangle for click detection

# Function to upload an image
def upload_image():
    Tk().withdraw()  # Hide the root Tkinter window
    file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
    if file_path:
        return cv2.imread(file_path)  # Read the image using OpenCV
    return None

# Function to capture an image from the camera
def capture_image():
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    cap.release()
    if ret:
        return frame
    return None

# Main game loop
running = True
current_image = None
recognized_card = "No card recognized yet."

while running:
    screen.blit(background_image, (0, 0))  # Draw the background image

    # Draw header
    draw_text("UNO Card Recognition", (SCREEN_WIDTH // 2 - 180, 20), (255, 255, 0))

    # Create buttons for uploading and capturing images with animations
    upload_button = draw_button("Upload Image", (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 30), BUTTON_COLOR, BUTTON_HOVER_COLOR)
    capture_button = draw_button("Capture from Camera", (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 30), BUTTON_COLOR, BUTTON_HOVER_COLOR)

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                mouse_pos = pygame.mouse.get_pos()
                if upload_button.collidepoint(mouse_pos):
                    current_image = upload_image()
                    if current_image is not None:
                        # Add card recognition logic here
                        recognized_card = "Card recognized!"  # Placeholder message

                elif capture_button.collidepoint(mouse_pos):
                    current_image = capture_image()
                    if current_image is not None:
                        # Add card recognition logic here
                        recognized_card = "Card recognized!"  # Placeholder message

    pygame.display.flip()  # Update display

# Exit Pygame
pygame.quit()
sys.exit()
