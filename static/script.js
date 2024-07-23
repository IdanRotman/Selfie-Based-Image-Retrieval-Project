// Handles the image upload form submission
document.getElementById('uploadForm').addEventListener('submit', async function(event) {
    event.preventDefault();
    
    const formData = new FormData();
    const imageFile = document.getElementById('imageInput').files[0];
    if (imageFile) {
        formData.append('image', imageFile);
        await uploadImage(formData);
    }
});

// Uploads the image to the server and processes the response
async function uploadImage(formData) {
    const loader = document.getElementById('loader');
    const resultDiv = document.getElementById('result');
    loader.style.display = 'block'; // Show the loader
    resultDiv.innerHTML = ''; // Clear previous results

    try {
        const response = await fetch('/process_image', {
            method: 'POST',
            body: formData
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const result = await response.json();
        loader.style.display = 'none'; // Hide the loader

        if (result.images) {
            result.images.forEach(image => {
                const imgElement = document.createElement('img');
                imgElement.src = `/original_images/${image}`;
                const resultItem = document.createElement('div');
                resultItem.className = 'result-item';
                resultItem.appendChild(imgElement);
                resultDiv.appendChild(resultItem);
            });
        } else {
            resultDiv.innerHTML = `<p>${result.error}</p>`;
        }
    } catch (error) {
        loader.style.display = 'none'; // Hide the loader
        resultDiv.innerHTML = `<p>There was an error processing the image: ${error.message}</p>`;
        console.error('Error during fetch:', error); // Log the error for debugging
    }
}

// Starts the camera for capturing a photo
document.getElementById('startCamera').addEventListener('click', async function() {
    const cameraContainer = document.getElementById('cameraContainer');
    const video = document.getElementById('camera');
    const startButton = document.getElementById('startCamera');
    
    startButton.style.display = 'none';
    cameraContainer.style.display = 'block';
    
    try {
        const stream = await navigator.mediaDevices.getUserMedia({ video: true });
        video.srcObject = stream;
    } catch (error) {
        console.error('Error accessing the camera: ', error);
    }
});

// Captures a photo from the video stream and uploads it
document.getElementById('capturePhoto').addEventListener('click', function() {
    const video = document.getElementById('camera');
    const canvas = document.getElementById('photoCanvas');
    const context = canvas.getContext('2d');
    
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    context.drawImage(video, 0, 0, canvas.width, canvas.height);
    
    canvas.toBlob(async function(blob) {
        const formData = new FormData();
        formData.append('image', blob, 'captured_photo.jpg');
        await uploadImage(formData);
    }, 'image/jpeg');
});
    