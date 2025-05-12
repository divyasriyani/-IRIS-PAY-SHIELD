# Import required libraries
import streamlit as st
import os
import json
import numpy as np
from PIL import Image
import cv2
from tensorflow.keras.models import load_model
from sklearn.metrics.pairwise import cosine_similarity

# === Constants ===
UPLOAD_FOLDER = 'uploads'                      # Folder to save enrolled images
USER_DATA_FILE = 'user_data.json'              # File to store user info
MODEL_PATH = 'C:/Users/Desktop/iris/model/IRISRecognizer.h5'  # Trained model path
IMAGE_SIZE = (224, 224)                        # Target size for model input

# Create upload folder if not exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# === Load Pretrained Model ===
model = load_model(MODEL_PATH)

# === Load or Initialize User Data ===
if os.path.exists(USER_DATA_FILE):
    with open(USER_DATA_FILE, 'r') as f:
        user_data = json.load(f)  # Load existing user data
else:
    user_data = {}  # Start fresh if file doesn't exist

# === Save User Data to JSON ===
def save_user_data():
    with open(USER_DATA_FILE, 'w') as f:
        json.dump(user_data, f)

# === Preprocess Image Function ===
def preprocess_image(image_bytes):
    image = Image.open(image_bytes).convert('L')         # Convert to grayscale
    image = image.resize(IMAGE_SIZE)                     # Resize to model input size
    img_array = np.array(image).astype('float32') / 255.0  # Normalize pixel values
    img_array = np.expand_dims(img_array, axis=(0, -1))  # Shape: (1, 224, 224, 1)
    return img_array

# === Get Embedding from Model ===
def get_embedding(image_array):
    return model.predict(image_array)  # Forward pass through model to get features

# === Streamlit UI Config ===
st.set_page_config(page_title="Iris Recognition App", layout="centered")
st.title("🔐 Iris Recognition System")

# === Sidebar Options: Enroll or Authenticate ===
option = st.sidebar.selectbox("Choose Action", ["Enroll", "Authenticate"])

# === Enroll Section ===
if option == "Enroll":
    st.header("👁️ Enroll New User")
    username = st.text_input("Enter Username")
    iris_image = st.file_uploader("Upload Iris Image", type=['jpg', 'jpeg'])

    if st.button("Enroll"):
        if not username:
            st.warning("Please enter a username.")
        elif username in user_data:
            st.warning(f"{username} is already enrolled.")
        elif not iris_image:
            st.error("Please upload an image.")
        else:
            try:
                # Try to open and validate image
                image = Image.open(iris_image)
                image.verify()  # Check if image is valid
                iris_image.seek(0)  # Reset file pointer

                filename = f"{username}_iris.jpg"
                filepath = os.path.join(UPLOAD_FOLDER, filename)

                # Save image
                with open(filepath, 'wb') as f:
                    f.write(iris_image.read())

                user_data[username] = filename
                save_user_data()
                st.success(f"User {username} enrolled successfully!")

            except Exception as e:
                st.error("Invalid photo. Please upload a valid iris image (.jpg/.jpeg only).")

# === Authenticate Section ===
elif option == "Authenticate":
    st.header("🔍 Authenticate User")
    username = st.text_input("Enter Username for Authentication")
    auth_image = st.file_uploader("Upload Iris Image for Authentication", type=['jpg', 'jpeg'])

    if st.button("Authenticate"):
        if not username:
            st.warning("Please enter a username.")
        elif username not in user_data:
            st.error("User not found!")
        elif not auth_image:
            st.error("Please upload an authentication image.")
        else:
            try:
                # Validate uploaded image
                image = Image.open(auth_image)
                image.verify()
                auth_image.seek(0)

                # Load enrolled image and preprocess
                enrolled_path = os.path.join(UPLOAD_FOLDER, user_data[username])
                with open(enrolled_path, 'rb') as f:
                    enrolled_array = preprocess_image(f)

                # Preprocess authentication image
                auth_array = preprocess_image(auth_image)

                # Get model embeddings
                enrolled_embed = get_embedding(enrolled_array)
                auth_embed = get_embedding(auth_array)

                # Compare using cosine similarity
                similarity = cosine_similarity(enrolled_embed, auth_embed)[0][0]
                st.metric(label="Cosine Similarity", value=f"{similarity:.4f}")

                if similarity > 0.95:
                    st.success(f"Authentication successful for {username} ✅")
                else:
                    st.error(f"Authentication failed for {username} ❌")

            except Exception as e:
                st.error("Invalid photo. Please upload a valid iris image (.jpg/.jpeg only).")
