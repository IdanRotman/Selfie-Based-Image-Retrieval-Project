import os
import cv2
import pickle
from mtcnn.mtcnn import MTCNN
import face_recognition

# Directory containing the original images
ORIGINAL_IMAGE_DIR = 'original_images'
# Directory to store processed face encodings
PROCESSED_IMAGE_DIR = 'processed_faces'
# Path to the file to store face encodings
ENCODINGS_FILE = os.path.join(PROCESSED_IMAGE_DIR, 'encodings.pkl')

def detect_and_encode_faces(image_path):
    """
    Detects faces in the image and encodes them using face_recognition.

    Args:
        image_path (str): The path to the image file.

    Returns:
        list: A list of face encodings.
    """
    # Read the image
    image = cv2.imread(image_path)
    # Initialize the MTCNN face detector
    detector = MTCNN()
    # Detect faces in the image
    detections = detector.detect_faces(image)
    encodings = []

    for detection in detections:
        x, y, width, height = detection['box']
        x, y = abs(x), abs(y)
        # Extract the face region
        face = image[y:y+height, x:x+width]
        # Use face_recognition to get face encodings
        face_locations = [(y, x+width, y+height, x)]
        face_encodings = face_recognition.face_encodings(image, face_locations)
        if face_encodings:
            encodings.append(face_encodings[0])

    return encodings

def process_images():
    """
    Processes all images in the original images directory, detects and encodes faces,
    and saves the encodings to a file.
    """
    # Create the processed faces directory if it doesn't exist
    if not os.path.exists(PROCESSED_IMAGE_DIR):
        os.makedirs(PROCESSED_IMAGE_DIR)

    encodings = []
    # Iterate over all files in the original images directory
    for image_file in os.listdir(ORIGINAL_IMAGE_DIR):
        original_image_path = os.path.join(ORIGINAL_IMAGE_DIR, image_file)
        # Detect and encode faces in the image
        face_encodings = detect_and_encode_faces(original_image_path)
        for encoding in face_encodings:
            # Append the encoding and the corresponding image file name to the list
            encodings.append((image_file, encoding))

    # Save the encodings to a file using pickle
    with open(ENCODINGS_FILE, 'wb') as f:
        pickle.dump(encodings, f)

if __name__ == '__main__':
    process_images()
