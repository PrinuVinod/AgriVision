from flask import Flask, render_template, request, jsonify, url_for
import subprocess
import os
from pymongo import MongoClient
from bson import ObjectId
import datetime
import base64

app = Flask(__name__)

# Connect to MongoDB
try:
    client = MongoClient("mongodb+srv://prinuvinod:blahblah123@cluster0.nlgfvz1.mongodb.net/?retryWrites=true&w=majority")
    db = client["AgriVision"]
    uploads_collection = db["uploads"]
    output_collection = db["output"]

    # Check if MongoDB is connected
    if client.server_info():
        print("Connected to MongoDB successfully")
    else:
        print("Failed to connect to MongoDB")

except Exception as e:
    print(f"Error connecting to MongoDB: {e}")

# Specify the directory for saving images in the static folder
static_folder = 'static'
upload_folder = os.path.join(static_folder, 'uploads')
output_folder = os.path.join(static_folder, 'output')

os.makedirs(upload_folder, exist_ok=True)
os.makedirs(output_folder, exist_ok=True)

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
    try:
        # Check if the 'file' key is in the request.files dictionary
        if 'file' not in request.files:
            return "No file part"

        uploaded_image = request.files['file']
        if uploaded_image.filename == '':
            return "No selected file"

        # Save the uploaded image with a unique name in the static/uploads folder
        image_path = os.path.join(upload_folder, 'user_image.jpg')
        uploaded_image.save(image_path)

        # Save uploaded image to MongoDB
        with open(image_path, 'rb') as image_file:
            image_data = image_file.read()
            uploaded_image_id = str(ObjectId())
            uploads_collection.insert_one({
                '_id': uploaded_image_id,
                'type': 'uploaded',
                'data': image_data,
                'timestamp': datetime.datetime.utcnow()
            })

        # Perform detection using the saved image
        detection_script_path = 'detect.py'
        subprocess.run(['python', detection_script_path, image_path])

        # Save annotated output image to MongoDB
        with open(os.path.join(output_folder, 'annotated_image.jpg'), 'rb') as output_image_file:
            output_image_data = output_image_file.read()
            output_image_id = str(ObjectId())
            output_collection.insert_one({
                '_id': output_image_id,
                'type': 'output',
                'data': output_image_data,
                'timestamp': datetime.datetime.utcnow()
            })

        # Convert images to base64 for displaying in HTML
        uploaded_image_base64 = base64.b64encode(image_data).decode('utf-8')
        output_image_base64 = base64.b64encode(output_image_data).decode('utf-8')

        return jsonify({
            'uploaded_image_base64': uploaded_image_base64,
            'output_image_base64': output_image_base64,
            'uploaded_image_url': url_for('static', filename=f'uploads/user_image.jpg'),
            'output_image_url': url_for('static', filename=f'output/annotated_image.jpg')
        })

    except Exception as e:
        print(f"Error processing detection: {e}")
        return jsonify({'error': 'An error occurred during detection.'}), 500

if __name__ == '__main__':
    app.run(debug=True)