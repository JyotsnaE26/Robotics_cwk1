import cv2
from ultralytics import YOLO

def recognize_card(image, model):
    """Predict the UNO card in the given image."""
    results = model(image)
    
    # Loop through each detection
    for result in results:
        for box in result.boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])  # Coordinates of the bounding box
            label = int(box.cls.item())  # Convert label to int if needed
            confidence = float(box.conf.item())  # Convert confidence to float
            
            # Draw bounding box and label
            cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(image, f"{label} ({confidence:.2f})", (x1, y1 - 10), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
    
    return image

def process_camera(model):
    """Process video stream from the camera to recognize UNO cards in real-time."""
    cap = cv2.VideoCapture(0)
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        frame = recognize_card(frame, model)
        cv2.imshow("UNO Card Recognition", frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    # Load the trained model
    model = YOLO('online.pt')  # Load your trained model
    
    # Run the camera mode
    process_camera(model)
