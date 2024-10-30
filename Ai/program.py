import cv2
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import os

# Constants
IMG_SIZE = 128  # Size to which each card image will be resized
NUM_CLASSES = 108  # Number of different UNO cards

# 1. Build the CNN Model
def build_model():
    model = Sequential([
        Conv2D(32, (3, 3), activation='relu', input_shape=(IMG_SIZE, IMG_SIZE, 3)),
        MaxPooling2D(2, 2),
        Conv2D(64, (3, 3), activation='relu'),
        MaxPooling2D(2, 2),
        Conv2D(128, (3, 3), activation='relu'),
        MaxPooling2D(2, 2),
        Flatten(),
        Dense(128, activation='relu'),
        Dense(NUM_CLASSES, activation='softmax')  # One class for each UNO card
    ])
    
    model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
    return model

# 2. Preprocess Image (Resize, Normalize)
def preprocess_image(img):
    img = cv2.resize(img, (IMG_SIZE, IMG_SIZE))
    img = img / 255.0  # Normalize pixel values
    return np.reshape(img, (1, IMG_SIZE, IMG_SIZE, 3))

# 3. Load and Preprocess Dataset for Training
def load_data(data_dir):
    datagen = ImageDataGenerator(validation_split=0.2, rescale=1.0/255)
    
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
    model.fit(train_gen, epochs=epochs, validation_data=val_gen)
    model.save('uno_card_model.h5')

# 5. Load Model and Predict Card
def predict_card(model, img):
    processed_img = preprocess_image(img)
    predictions = model.predict(processed_img)
    return np.argmax(predictions)

# 6. Real-time Camera or File Mode
def main(input_source='camera', data_dir=None, model_path='uno_card_model.h5'):
    # Load model
    model = build_model()
    
    if os.path.exists(model_path):
        model = tf.keras.models.load_model(model_path)
    else:
        print("Training model...")
        train_gen, val_gen = load_data(data_dir)
        train_model(model, train_gen, val_gen)
    
    if input_source == 'camera':
        # Use camera stream
        cap = cv2.VideoCapture(0)
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            card_class = predict_card(model, frame)
            print(f"Detected UNO card: {card_class}")
            
            cv2.imshow("Camera", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
                
        cap.release()
        cv2.destroyAllWindows()
    else:
        # Use an image file
        img = cv2.imread(input_source)
        card_class = predict_card(model, img)
        print(f"Detected UNO card: {card_class}")
        cv2.imshow("Image", img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="UNO Card Recognition using CNN")
    parser.add_argument('--input', type=str, default='camera', help="Input source: 'camera' or image file path")
    parser.add_argument('--data', type=str, help="Directory of images to train the model")
    args = parser.parse_args()
    
    main(input_source=args.input, data_dir=args.data)
