from flask import Flask, render_template, jsonify
import subprocess

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
    script_path = 'detect.py'

    try:
        subprocess.run(['python', script_path], check=True)
        return jsonify({'status': 'success', 'message': 'Detection started successfully'})
    except subprocess.CalledProcessError as e:
        return jsonify({'status': 'error', 'message': f'Error starting detection: {e}'})

if __name__ == '__main__':
    app.run(debug=True)
