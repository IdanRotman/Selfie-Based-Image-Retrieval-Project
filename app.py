from flask import Flask, request, jsonify, send_from_directory, render_template
import face_recognition
import os
import pickle
import numpy as np
from PIL import Image
import io

app = Flask(__name__)

# Path to the file containing face encodings
ENCODINGS_FILE = 'processed_faces/encodings.pkl'
# Directory containing the original images
ORIGINAL_IMAGE_DIR = 'original_images'

def load_encodings():
    """Loads the face encodings from 'encodings.pkl' file into memory."""
    with open(ENCODINGS_FILE, 'rb') as f:
        return pickle.load(f)

def encode_face(image):
    """Takes an image and returns the face encoding.
    If no faces are found in the image, returns None.
    """
    image = np.array(image)
    face_encodings = face_recognition.face_encodings(image)
    if len(face_encodings) > 0:
        return face_encodings[0]
    return None

@app.route('/')
def index():
    """Displays the home page (index.html)."""
    return render_template('index.html')

@app.route('/process_image', methods=['POST'])
def process_image():
    """Handles POST request for image upload, processes the image, and returns matching images from the database."""
    file = request.files['image']
    image = Image.open(io.BytesIO(file.read()))
    
    # Encode the face from the uploaded image
    uploaded_face_encoding = encode_face(image)
    if uploaded_face_encoding is None:
        return jsonify({"error": "No faces found in the uploaded image."})

    # Load precomputed encodings
    precomputed_encodings = load_encodings()
    matches = []

    for image_file, stored_encoding in precomputed_encodings:
        match = face_recognition.compare_faces([stored_encoding], uploaded_face_encoding)
        if match[0]:
            matches.append(image_file)

    return jsonify({"images": list(set(matches))})

@app.route('/original_images/<filename>')
def get_image(filename):
    """Serves an image file from the 'original_images' directory."""
    return send_from_directory(ORIGINAL_IMAGE_DIR, filename)

if __name__ == '__main__':
    app.run(debug=True)
