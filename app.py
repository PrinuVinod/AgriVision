from flask import Flask, render_template

app = Flask(__name__)

@app.route('/index')
def home():
    return render_template('index.html')


@app.route('/detection')
def detection():
    return render_template('detection.html')

if __name__ == '__main__':
    app.run(debug=True)
