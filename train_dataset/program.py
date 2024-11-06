from ultralytics import YOLO

# Initialize a new YOLO model without pretrained weights
model = YOLO()  # This will initialize a model with random weights

# Train the model on your dataset
model.train(data='/Users/university/Documents/Robotics_cwk1/train_dataset/UnoCards.v2i.yolov8-obb/data.yaml', epochs=50, imgsz=640)
