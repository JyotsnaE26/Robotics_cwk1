import cv2
import numpy as np
import os

# Paths to your images
card_image_path = 'path_to_your_card_image.jpg'  # Replace with your card image path
output_folder = os.getcwd()  # Save generated images in the current working directory

# Load the card image
card_image = cv2.imread(card_image_path)
if card_image is None:
    raise FileNotFoundError(f"Could not load image at {card_image_path}. Please check the path.")

card_height, card_width = card_image.shape[:2]

# Number of variations to generate
num_variations = 5

# Function to create a solid color background
def create_solid_color_background(color):
    return np.full((card_height, card_width, 3), color, dtype=np.uint8)

# Function to create a gradient background
def create_gradient_background(start_color, end_color):
    gradient = np.zeros((card_height, card_width, 3), dtype=np.uint8)
    for i in range(card_width):
        gradient[:, i] = np.linspace(start_color, end_color, card_width)
    return gradient

# Function to create random noise background
def create_noise_background():
    return np.random.randint(0, 256, (card_height, card_width, 3), dtype=np.uint8)

# Generate variations
for i in range(num_variations):
    # Choose a background type randomly
    background_type = np.random.choice(['solid', 'gradient', 'noise'])

    if background_type == 'solid':
        # Generate a solid color background with random color
        color = np.random.randint(0, 256, size=(3,), dtype=np.uint8)
        background = create_solid_color_background(color)

    elif background_type == 'gradient':
        # Generate a gradient background with random start and end colors
        start_color = np.random.randint(0, 256, size=(3,), dtype=np.uint8)
        end_color = np.random.randint(0, 256, size=(3,), dtype=np.uint8)
        background = create_gradient_background(start_color, end_color)

    else:
        # Generate a noise background
        background = create_noise_background()

    # Create a random position for the card
    x_offset = np.random.randint(0, background.shape[1] - card_width)
    y_offset = np.random.randint(0, background.shape[0] - card_height)

    # Overlay the card image onto the background
    background[y_offset:y_offset + card_height, x_offset:x_offset + card_width] = card_image

    # Save the new image
    output_image_path = os.path.join(output_folder, f'card_variation_{i + 1}.jpg')
    cv2.imwrite(output_image_path, background)

print(f'Generated {num_variations} variations of the card image.')
