import os
from PIL import Image

# Paths to your image and label folders
input_image_folder = '/Users/university/Documents/Robotics_cwk1/final_dataset/UnoCards.v1i.yolov8-obb/train/images'
input_label_folder = '/Users/university/Documents/Robotics_cwk1/final_dataset/UnoCards.v1i.yolov8-obb/train/labels'
output_image_folder = '/Users/university/Documents/Robotics_cwk1/test_dataset/images'
output_label_folder = '/Users/university/Documents/Robotics_cwk1/test_dataset/labels'

# Ensure output directories exist
os.makedirs(output_image_folder, exist_ok=True)
os.makedirs(output_label_folder, exist_ok=True)

# New dimensions
new_width, new_height = 640, 640

for image_file in os.listdir(input_image_folder):
    if image_file.endswith(('.jpg', '.jpeg', '.png')):
        # Load image and get original dimensions
        img_path = os.path.join(input_image_folder, image_file)
        img = Image.open(img_path)
        original_width, original_height = img.size

        # Resize image
        img_resized = img.resize((new_width, new_height), Image.LANCZOS)
        img_resized.save(os.path.join(output_image_folder, image_file), 'JPEG', quality=85)

        # Process corresponding label file
        label_file = os.path.splitext(image_file)[0] + '.txt'
        label_path = os.path.join(input_label_folder, label_file)
        if os.path.exists(label_path):
            with open(label_path, 'r') as file:
                lines = file.readlines()

            # Adjust label bounding boxes
            with open(os.path.join(output_label_folder, label_file), 'w') as file:
                for line in lines:
                    label_data = line.strip().split()
                    class_id = label_data[0]
                    x_center = float(label_data[1]) * original_width
                    y_center = float(label_data[2]) * original_height
                    bbox_width = float(label_data[3]) * original_width
                    bbox_height = float(label_data[4]) * original_height

                    # Scale the bounding box values to the new image dimensions
                    x_center = (x_center * new_width) / original_width
                    y_center = (y_center * new_height) / original_height
                    bbox_width = (bbox_width * new_width) / original_width
                    bbox_height = (bbox_height * new_height) / original_height

                    # Normalize the new bounding box values
                    x_center /= new_width
                    y_center /= new_height
                    bbox_width /= new_width
                    bbox_height /= new_height

                    # Write adjusted labels to file
                    file.write(f"{class_id} {x_center} {y_center} {bbox_width} {bbox_height}\n")

print("Image and label resizing complete!")
