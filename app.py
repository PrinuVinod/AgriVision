#app.py

import subprocess
from flask import Flask, render_template, Response
import cv2

app = Flask(__name__)

@app.route('/index')
def home():
    return render_template('index.html')

@app.route('/detection')
def detection():
    return render_template('detection.html')

@app.route('/start_detection')
def start_detection():
    try:
        subprocess.run(['python', 'detect.py'], check=True)
        return "Detection started!"
    except subprocess.CalledProcessError as e:
        return f"Error: {e}"
    

if __name__ == '__main__':
    app.run(debug=True)
