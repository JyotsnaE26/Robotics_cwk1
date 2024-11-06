import cv2
from ultralytics import YOLO

# Define card types and colors based on the labels in your model
card_types = {
    5: "0", 6: "1", 7: "2", 8: "3", 9: "4",
    10: "5", 11: "6", 12: "7", 13: "8", 14: "9",
    16: "Reverse", 17: "Skip", 18: "Wild", 19: "Wild Draw 4"
}

card_colors = {
    1: "Black", 2: "Blue", 4: "Green", 15: "Red", 20: "Yellow"
}

class CameraCapture:
    def __init__(self, model_path):
        # Initialize the camera capture with the specified YOLO model
        self.model = YOLO(model_path)

    def detect_cards(self, image):
        # Detect UNO cards in the provided image and annotate them
        results = self.model(image)
        
        # Iterate through the detection results
        for result in results:
            for box in result.boxes:
                # Get the bounding box coordinates
                x1, y1, x2, y2 = map(int, box.xyxy[0])  
                class_id = int(box.cls.item())  # Get the class ID
                confidence_score = float(box.conf.item())  # Get the confidence score
                
                # Get color and type based on the class ID
                color = card_colors.get(class_id)
                card_type = card_types.get(class_id)
                
                # Construct the label based on available information
                if color and card_type:
                    card_label = f"{color} {card_type}"
                elif color:
                    card_label = color
                elif card_type:
                    card_label = card_type
                else:
                    continue  # Skip if neither color nor type is recognized
                
                # Draw a rectangle around the detected card
                cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
                # Annotate the image with the card label and confidence score
                cv2.putText(image, f"{card_label} ({confidence_score:.2f})", (x1, y1 - 10), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
        
        return image

    def start_camera(self):
        # Capture video from the camera and recognize UNO cards in real-time
        video_capture = cv2.VideoCapture(0)
        
        while True:
            # Read a frame from the camera
            success, frame = video_capture.read()
            if not success:
                break
            
            # Detect cards in the current frame
            annotated_frame = self.detect_cards(frame)
            cv2.imshow("UNO Card Recognition", annotated_frame)
            
            # Exit if the 'q' key is pressed
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        
        # Release the camera and close the window
        video_capture.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    # Create an instance of CameraCapture with the trained model path
    camera_capture = CameraCapture('best.pt')
    # Start the camera for card recognition
    camera_capture.start_camera()
