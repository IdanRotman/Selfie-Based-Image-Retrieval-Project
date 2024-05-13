import numpy as np
from mtcnn.mtcnn import MTCNN
from deepface import DeepFace
from PIL import Image
import base64
from io import BytesIO
import os


def image_to_base64(img):
    buffered = BytesIO()
    img.save(buffered, format="JPEG")
    img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
    return "data:image/jpeg;base64," + img_str


def extract_img_faces(full_img, bounding_boxes):
    extracted_faces = []
    for bounding_box in bounding_boxes:
        x1, y1, width, height = bounding_box['box']
        x2, y2 = x1 + width, y1 + height
        extracted_face = Image.fromarray(full_img[y1:y2, x1:x2])
        extracted_faces.append(extracted_face)
    return extracted_faces


def person_in_img(full_img, person_face_img):
    full_img = np.array(full_img)
    person_face_img = np.array(person_face_img)
    detector = MTCNN(min_face_size=40)
    face_bounding_boxes = detector.detect_faces(full_img)

    extracted_faces = extract_img_faces(full_img, face_bounding_boxes)

    # Convert person_face_img to base64 if it's a PIL image
    if isinstance(person_face_img, Image.Image):
        person_face_img = image_to_base64(person_face_img)

    for extracted_face in extracted_faces:
        # Convert each extracted face to base64
        face_base64 = image_to_base64(extracted_face)

        # Use DeepFace.verify with the correct parameter structure
        try:
            result = DeepFace.verify(img1_path=face_base64, img2_path=person_face_img, enforce_detection=False)
            if result['verified']:
                return True
        except Exception as e:
            print("Verification error:", e)

    return False




#this function gets an image path
def return_all_images_with_face(user_img_path):
    all_imgs = []
    imgs_dir = r"C:\Users\idanr\OneDrive\תמונות\test for project\Photos Database"
    for img_name in os.listdir(imgs_dir):
        img_path = os.path.join(imgs_dir, img_name)
        img = Image.open(img_path)
        all_imgs.append(img)

    user_img = Image.open(user_img_path)
    relevant_imgs = []
    for img in all_imgs:
        if(person_in_img(img, user_img)):
            relevant_imgs.append(img)
    return relevant_imgs