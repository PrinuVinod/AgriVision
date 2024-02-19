from flask import Flask, render_template, request, jsonify
import subprocess
import os
from pymongo import MongoClient

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/detection')
def detection():
    return render_template('detection.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/gallery')
def gallery():
    return render_template('gallery.html')

@app.route('/service')
def service():
    return render_template('service.html')

@app.route('/start_detection', methods=['POST'])
def start_detection():
    # Specify the directory for saving images
    upload_folder = 'uploads'
    os.makedirs(upload_folder, exist_ok=True)

    # Check if the 'file' key is in the request.files dictionary
    if 'file' not in request.files:
        return "No file part"

    uploaded_image = request.files['file']
    if uploaded_image.filename == '':
        return "No selected file"

    # Save the uploaded image with a unique name
    image_path = os.path.join(upload_folder, 'user_image.jpg')
    uploaded_image.save(image_path)

    # Perform detection using the saved image
    detection_script_path = 'detect.py'
    subprocess.run(['python', detection_script_path, image_path])

    # Return a response (you may customize the response based on your needs)
    return "Detection started successfully"

if __name__ == '__main__':
    app.run(debug=False,host='0.0.0.0')
