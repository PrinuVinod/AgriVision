from flask import Flask, render_template

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
    try:
        # Run your detect.py script using subprocess
        result = subprocess.run(['python', 'detect.py'], capture_output=True, text=True)
        print("Detection output:", result.stdout)
        return 'Detection started successfully'
    except Exception as e:
        print("Error starting detection:", str(e))
        return 'Error starting detection'

if __name__ == '__main__':
    app.run(debug=True)
