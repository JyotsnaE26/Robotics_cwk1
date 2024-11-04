import pygame
import sys
import cv2
from tkinter import Tk, filedialog

# Initialize Pygame
pygame.init()

# Screen dimensions and colors
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
BACKGROUND_COLOR = (34, 139, 34)  # Green background
FONT_COLOR = (255, 255, 255)

# Set up the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("UNO Card Recognition")

# Load font
font = pygame.font.Font(None, 36)

# Function to draw text on the screen
def draw_text(text, pos):
    rendered_text = font.render(text, True, FONT_COLOR)
    screen.blit(rendered_text, pos)

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
    screen.fill(BACKGROUND_COLOR)  # Set background color

    # Display options to the user
    draw_text("Press 'U' to upload an image", (20, 20))
    draw_text("Press 'C' to capture from camera", (20, 60))
    draw_text("Recognized Card: " + recognized_card, (20, SCREEN_HEIGHT - 40))

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_u:  # Upload image
                current_image = upload_image()
                if current_image is not None:
                    # Here you can add the card recognition logic
                    recognized_card = "Card recognized!"  # Placeholder message
            elif event.key == pygame.K_c:  # Capture from camera
                current_image = capture_image()
                if current_image is not None:
                    # Here you can add the card recognition logic
                    recognized_card = "Card recognized!"  # Placeholder message

    pygame.display.flip()  # Update display

# Exit Pygame
pygame.quit()
sys.exit()
