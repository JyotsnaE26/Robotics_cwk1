import cv2
from ultralytics import YOLO
import tkinter as tk
from tkinter import filedialog

class ImageCapture:
    def __init__(self, model_path):
        """Initialize the image capture with the specified YOLO model."""
        self.model = YOLO(model_path)

    def detect_cards_in_image(self, image):
        """Detect UNO cards in the provided image and annotate them."""
        results = self.model(image)
        
        # Define font and color for annotation
        font = cv2.FONT_HERSHEY_SIMPLEX
        color = (0, 255, 0)  # Green color for bounding boxes and text
        
        # Check if any results were found
        if results:
            for result in results:
                for box in result.boxes:
                    # Get the bounding box coordinates
                    x1, y1, x2, y2 = map(int, box.xyxy[0])
                    card_label = int(box.cls.item())  # Get the label for the detected card
                    confidence_score = float(box.conf.item())  # Get the confidence score

                    # Draw a rectangle around the detected card
                    cv2.rectangle(image, (x1, y1), (x2, y2), color, 2)
                    # Annotate the image with the card label and confidence score
                    cv2.putText(image, f"{card_label} ({confidence_score:.2f})", (x1, y1 - 10), 
                                font, 0.6, color, 2)
        else:
            print("No UNO cards detected in the image.")
        
        return image

    def process_image(self, image_path):
        """Load an image, detect UNO cards, and display the annotated image."""
        # Load the image from the specified path
        image = cv2.imread(image_path)
        if image is None:
            print("Error: Could not load image.")
            return
        
        # Detect cards in the loaded image
        annotated_image = self.detect_cards_in_image(image)
        cv2.imshow("UNO Card Detection", annotated_image)
        
        # Wait for a key press and close the window
        cv2.waitKey(0)
        cv2.destroyAllWindows()

def select_image():
    """Open a file dialog to select an image and return its path."""
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    image_path = filedialog.askopenfilename(title="Select an Image",
                                            filetypes=[("Image files", "*.jpg *.jpeg *.png")])
    if not image_path:
        print("No image selected.")
    return image_path

if __name__ == "__main__":
    # Create an instance of ImageCapture with the trained model path
    image_capture = ImageCapture('online.pt')
    
    # Open a dialog box to select an image
    selected_image_path = select_image()
    if selected_image_path:  # Check if a file was selected
        image_capture.process_image(selected_image_path)
