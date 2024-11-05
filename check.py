import cv2
import os

# Directories for images, annotations, and output
image_dir = "/Users/university/Documents/Robotics_cwk1/test_dataset/images"
annotation_dir = "/Users/university/Documents/Robotics_cwk1/test_dataset/labels"
output_dir = "/Users/university/Documents/Robotics_cwk1/test_dataset/output_with_bboxes"
os.makedirs(output_dir, exist_ok=True)

# Function to load and display images with bounding boxes
def display_image_with_bboxes(image_path, annotation_path, output_path):
    # Load image
    image = cv2.imread(image_path)

    # Read bounding boxes from annotation file
    with open(annotation_path, 'r') as file:
        for line in file:
            class_id, x, y, width, height = map(float, line.strip().split())

            # Convert YOLO format (normalized center x, y, width, height) to bounding box coordinates
            img_h, img_w = image.shape[:2]
            x1 = int((x - width / 2) * img_w)
            y1 = int((y - height / 2) * img_h)
            x2 = int((x + width / 2) * img_w)
            y2 = int((y + height / 2) * img_h)

            # Draw the bounding box
            cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(image, f"Class {int(class_id)}", (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    # Save the image with bounding boxes
    cv2.imwrite(output_path, image)
    print(f"Saved annotated image to {output_path}")

# Process all images in the directory
for image_file in os.listdir(image_dir):
    if image_file.endswith(('.jpg', '.jpeg', '.png')):
        # Construct file paths
        image_path = os.path.join(image_dir, image_file)
        annotation_path = os.path.join(annotation_dir, os.path.splitext(image_file)[0] + '.txt')
        output_path = os.path.join(output_dir, f"annotated_{image_file}")

        # Check if annotation file exists
        if os.path.exists(annotation_path):
            display_image_with_bboxes(image_path, annotation_path, output_path)
        else:
            print(f"Annotation file not found for {image_file}")
