import cv2
import numpy as np
import os

# Paths to your images
card_image_path = '/Users/university/Documents/Robotics_cwk1/dataset/wild_draw_4/original.jpg'  # Update this line with the correct path
output_folder = os.getcwd()  # Save generated images in the current working directory

# Load the card image
card_image = cv2.imread(card_image_path)
if card_image is None:
    raise FileNotFoundError(f"Could not load image at {card_image_path}. Please check the path.")

card_height, card_width = card_image.shape[:2]

# Number of variations to generate
num_variations = 10

# Function to create a solid color background
def create_solid_color_background(color, height, width):
    return np.full((height, width, 3), color, dtype=np.uint8)

# Function to create a gradient background
def create_gradient_background(start_color, end_color, height, width):
    gradient = np.zeros((height, width, 3), dtype=np.uint8)
    for i in range(width):
        gradient[:, i] = np.array(start_color) * (1 - i / width) + np.array(end_color) * (i / width)
    return gradient

# Function to create random noise background
def create_noise_background(height, width):
    return np.random.randint(0, 256, (height, width, 3), dtype=np.uint8)

# Generate variations
for i in range(num_variations):
    # Ensure that the background is at least as large as the card
    background_height = np.random.randint(card_height, card_height + 200)  # Random height between card height and card height + 200
    background_width = np.random.randint(card_width, card_width + 200)  # Random width between card width and card width + 200

    # Generate a blank background with random dimensions
    background = np.zeros((background_height, background_width, 3), dtype=np.uint8)

    # Choose a background type randomly
    background_type = np.random.choice(['solid', 'gradient', 'noise'])

    if background_type == 'solid':
        # Generate a solid color background with random color
        color = np.random.randint(0, 256, size=(3,), dtype=np.uint8)
        background = create_solid_color_background(color, background_height, background_width)

    elif background_type == 'gradient':
        # Generate a gradient background with random start and end colors
        start_color = np.random.randint(0, 256, size=(3,), dtype=np.uint8)
        end_color = np.random.randint(0, 256, size=(3,), dtype=np.uint8)
        background = create_gradient_background(start_color, end_color, background_height, background_width)

    else:
        # Generate a noise background
        background = create_noise_background(background_height, background_width)

    # Ensure that the offsets are valid
    max_x_offset = background.shape[1] - card_width
    max_y_offset = background.shape[0] - card_height

    # Check if offsets are valid to avoid ValueError
    if max_x_offset < 0 or max_y_offset < 0:
        print(f"Background size is smaller than the card size for variation {i + 1}. Skipping.")
        continue

    # Create a random position for the card within the background
    x_offset = np.random.randint(0, max_x_offset + 1)
    y_offset = np.random.randint(0, max_y_offset + 1)

    # Overlay the card image onto the background
    background[y_offset:y_offset + card_height, x_offset:x_offset + card_width] = card_image

    # Save the new image
    output_image_path = os.path.join(output_folder, f'card_variation_{i + 1}.jpg')
    cv2.imwrite(output_image_path, background)

print(f'Generated {num_variations} variations of the card image.')
