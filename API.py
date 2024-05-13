from flask import Flask, request, jsonify
from functions import return_all_images_with_face, image_to_base64  # Adjust these imports based on your actual module setup
from PIL import Image
from io import BytesIO
from flask_cors import CORS


app = Flask(__name__)
CORS(app)


@app.route('/process_image', methods=['POST'])
def process_image():
    # Retrieve the image from the request
    app.logger.info("received a request!")
    data = request.files['image']
    if data:
        user_img = Image.open(BytesIO(data.read()))
        relevant_imgs = return_all_images_with_face(user_img)  # Assuming your function can now directly handle the PIL Image
        # Convert the results to base64 to send back to the client
        results_base64 = [image_to_base64(img) for img in relevant_imgs]
        return jsonify({'images': results_base64})
    else:
        return jsonify({'error': 'No image provided'}), 400


if __name__ == '__main__':
    app.run(debug=True)  # Runs the server in debug mode
