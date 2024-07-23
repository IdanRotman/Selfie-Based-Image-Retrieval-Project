# Face Recognition Web Application

This project is a web application that allows users to upload a photo of a face and retrieves all photos from a database where the face appears. The application uses advanced facial recognition technologies to provide accurate results.

## Table of Contents

- [Introduction](#introduction)
- [Technologies Used](#technologies-used)
- [Project Structure](#project-structure)


## Introduction

The main goal of this project is to create a facial recognition system that can identify and match faces from a given photo with faces in a database. Initially, VGG Face model was used, but due to performance issues, it was replaced by the `face_recognition` library in Python for faster and more efficient processing.

## Technologies Used

- **Frontend:**
  - HTML
  - CSS
  - JavaScript

- **Backend:**
  - Python
  - Flask

- **Libraries:**
  - `face_recognition`: Used for face detection and encoding
  - `MTCNN`: Used for face detection

## Project Structure
    project-directory/
│
├── original_images/ # Directory with original images
├── processed_faces/ # Directory to store processed face images
│ └── encodings.pkl # Encoded face data
├── static/
│ ├── script.js # JavaScript file for frontend logic
│ └── styles.css # CSS file for styling
├── templates/
│ └── index.html # HTML template for the web application
├── app.py # Flask application
└── preprocess_faces.py # Script to preprocess and encode faces

