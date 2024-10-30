import os

# Define all cards in UNO for each color and the wild cards
colors = ["red", "blue", "green", "yellow"]

# Number cards 0-9, and action cards: Draw Two, Reverse, Skip
number_cards = [f"{color}_{i}" for color in colors for i in range(10)]
action_cards = [f"{color}_draw_2" for color in colors] + \
               [f"{color}_reverse" for color in colors] + \
               [f"{color}_skip" for color in colors]

# Wild cards (not tied to any color)
wild_cards = ["wild", "wild_draw_4"]

# Combine all cards into one list
all_cards = number_cards + action_cards + wild_cards

# Parent directory where folders will be created
parent_dir = "dataset"

# Function to create the folders
def create_folders():
    # Check if the parent directory exists, if not, create it
    if not os.path.exists(parent_dir):
        os.makedirs(parent_dir)

    # Loop through the card names and create folders for each card
    for card in all_cards:
        card_folder_path = os.path.join(parent_dir, card)
        try:
            os.makedirs(card_folder_path, exist_ok=True)
            print(f"Folder created: {card_folder_path}")
        except OSError as error:
            print(f"Error creating folder {card_folder_path}: {error}")

if __name__ == "__main__":
    create_folders()
