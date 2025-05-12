import os
import numpy as np
from flask import Flask, request, render_template, jsonify
from PIL import Image
import pandas as pd
from keras.models import load_model
from keras.preprocessing.image import img_to_array
import cv2
from werkzeug.utils import secure_filename


app = Flask(__name__)

# Path to the dataset and trained model
DATASET_PATH = os.path.join(os.getcwd(), 'static', 'datasets', 'CASIA-Iris-Thousand')
CSV_FILE_PATH = os.path.join(os.getcwd(), 'data', 'iris_thousands_dataset.csv')
MODEL_PATH = os.path.join(os.getcwd(), 'model', 'IRISRecognizer.h5')

# Load the dataset and model
iris_labels_df = pd.read_csv(CSV_FILE_PATH)
model = load_model(MODEL_PATH)

# Ensure the uploads directory exists
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Allowed file extensions for uploads
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

# Function to check if the file has an allowed extension
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/recognize', methods=['POST'])
def recognize_iris():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if file and allowed_file(file.filename):
        # Secure the filename and save it temporarily
        filename = secure_filename(file.filename)
        uploaded_image_path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(uploaded_image_path)

        try:
            # Process and recognize the image
            recognized_subject = compare_image_to_dataset(uploaded_image_path)

            # Return the result in a JSON response
            return jsonify({'recognized_subject': recognized_subject})
        except Exception as e:
            # Return error if recognition fails
            return jsonify({'error': f'Error during recognition: {str(e)}'}), 500
    else:
        return jsonify({'error': 'Invalid file type'}), 400

def compare_image_to_dataset(uploaded_image_path):
    # Read and preprocess the uploaded image
    uploaded_image = cv2.imread(uploaded_image_path)
    uploaded_image = cv2.cvtColor(uploaded_image, cv2.COLOR_BGR2RGB)
    
    # Preprocess the image for the model
    image = preprocess_image(uploaded_image)
    
    # Get the predicted class index from the model
    predicted_class_index = np.argmax(model.predict(np.expand_dims(image, axis=0)))
    print(f"Predicted class index: {predicted_class_index}")  # Debug log

    # Get the predicted label from the dataset using the predicted class index
    predicted_label = iris_labels_df.iloc[predicted_class_index]['Label']
    print(f"Predicted label: {predicted_label}")  # Debug log
    
    # Extract the label from the uploaded image filename (assuming it's part of the name)
    uploaded_image_label = os.path.basename(uploaded_image_path).split('.')[0]
    print(f"Uploaded image label: {uploaded_image_label}")  # Debug log

    # Extract the relevant part of both labels for comparison (adjust as necessary)
    uploaded_subject_id = uploaded_image_label.split('L')[0].replace('S', '')  # Extract "5006" from "S5006L02"
    predicted_subject_id = predicted_label.split('-')[0]  # Extract "446" from "446-L"
    
    print(f"Formatted uploaded label: {uploaded_subject_id}")  # Debug log
    print(f"Formatted predicted label: {predicted_subject_id}")  # Debug log
    
    # Example custom mapping (you may need to adapt this)
    label_mapping = {
        "5006": "446",  # map subject 5006 to predicted label 446
        # Add other mappings as needed
    }
    
    # Check if there's a mapped label for the uploaded subject
    if uploaded_subject_id in label_mapping and label_mapping[uploaded_subject_id] == predicted_subject_id:
        return f"Recognized: {predicted_label}"
    else:
        return "Not Recognized"


def preprocess_image(image):
    # Convert the image to grayscale if it's not already (3 channels to 1 channel)
    if len(image.shape) == 3:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Resize the image to match the model's expected input size
    image = cv2.resize(image, (224, 224))
    
    # Normalize the image (scale pixel values between 0 and 1)
    image = image.astype('float32') / 255.0
    
    # Expand dimensions to match the model's expected input shape
    image = np.expand_dims(image, axis=-1)  # Add the channel dimension
    
    return img_to_array(image)

if __name__ == '__main__':
    app.run(debug=True)
