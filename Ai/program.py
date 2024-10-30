import cv2
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential # type: ignore
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense # type: ignore
from tensorflow.keras.preprocessing.image import ImageDataGenerator # type: ignore
import os

# Constants
IMG_SIZE = 128  # Size to which each card image will be resized
NUM_CLASSES = 108  # Total number of different UNO cards

# 1. Build the CNN Model
def build_model():
    """Construct a convolutional neural network (CNN) for card recognition."""
    model = Sequential([
        Conv2D(32, (3, 3), activation='relu', input_shape=(IMG_SIZE, IMG_SIZE, 3)),
        MaxPooling2D(2, 2),
        Conv2D(64, (3, 3), activation='relu'),
        MaxPooling2D(2, 2),
        Conv2D(128, (3, 3), activation='relu'),
        MaxPooling2D(2, 2),
        Flatten(),
        Dense(128, activation='relu'),
        Dense(NUM_CLASSES, activation='softmax')  # Softmax layer for multi-class classification
    ])
    
    model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
    return model

# 2. Preprocess Image (Resize, Normalize)
def preprocess_image(img):
    """Resize and normalize the input image for the model."""
    img = cv2.resize(img, (IMG_SIZE, IMG_SIZE))
    img = img / 255.0  # Normalize pixel values to [0, 1]
    return np.reshape(img, (1, IMG_SIZE, IMG_SIZE, 3))  # Reshape for model input

# 3. Load and Preprocess Dataset for Training
def load_data(data_dir):
    """Load and preprocess image data from the specified directory."""
    datagen = ImageDataGenerator(validation_split=0.2, rescale=1.0/255)  # Rescale images
    
    train_generator = datagen.flow_from_directory(
        data_dir, 
        target_size=(IMG_SIZE, IMG_SIZE), 
        batch_size=32, 
        class_mode='sparse', 
        subset='training'
    )
    
    validation_generator = datagen.flow_from_directory(
        data_dir, 
        target_size=(IMG_SIZE, IMG_SIZE), 
        batch_size=32, 
        class_mode='sparse', 
        subset='validation'
    )
    
    return train_generator, validation_generator

# 4. Train the Model
def train_model(model, train_gen, val_gen, epochs=10):
    """Train the CNN model on the provided training data."""
    model.fit(train_gen, epochs=epochs, validation_data=val_gen)  # Train model
    model.save('uno_card_model.h5')  # Save trained model to file

# 5. Load Model and Predict Card
def predict_card(model, img):
    """Predict the class of the given image using the trained model."""
    processed_img = preprocess_image(img)  # Preprocess the input image
    predictions = model.predict(processed_img)  # Get predictions
    return np.argmax(predictions)  # Return the class with the highest score

# 6. Real-time Camera or File Mode
def main(input_source='camera', data_dir=None, model_path='uno_card_model.h5'):
    """Main function to run the card recognition system."""
    # Load model
    if os.path.exists(model_path):
        model = tf.keras.models.load_model(model_path)  # Load existing model
    else:
        print("Training model...")
        model = build_model()  # Build a new model
        train_gen, val_gen = load_data(data_dir)  # Load training data
        train_model(model, train_gen, val_gen)  # Train the model
    
    if input_source == 'camera':
        # Use camera stream for real-time prediction
        cap = cv2.VideoCapture(0)
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            card_class = predict_card(model, frame)  # Predict card class
            print(f"Detected UNO card: {card_class}")  # Output detected card class
            
            cv2.imshow("Camera", frame)  # Display camera feed
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break  # Exit on 'q' key press
                
        cap.release()
        cv2.destroyAllWindows()
    else:
        # Use an image file for prediction
        img = cv2.imread(input_source)
        card_class = predict_card(model, img)  # Predict card class
        print(f"Detected UNO card: {card_class}")  # Output detected card class
        cv2.imshow("Image", img)  # Display the image
        cv2.waitKey(0)
        cv2.destroyAllWindows()

if __name__ == "__main__":
    import argparse
    # Argument parser for command line inputs
    parser = argparse.ArgumentParser(description="UNO Card Recognition using CNN")
    parser.add_argument('--input', type=str, default='camera', help="Input source: 'camera' or image file path")
    parser.add_argument('--data', type=str, help="Directory of images to train the model")
    args = parser.parse_args()
    
    main(input_source=args.input, data_dir=args.data)  # Start the program
