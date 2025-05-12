# app.py
from flask import Flask, render_template, request, redirect, url_for, session
import os
import json
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'secretkey'
UPLOAD_FOLDER = 'uploads'
USER_DATA_FILE = 'user_data.json'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Load user data from file if it exists
if os.path.exists(USER_DATA_FILE):
    with open(USER_DATA_FILE, 'r') as f:
        user_data = json.load(f)
else:
    user_data = {}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/enroll', methods=['GET', 'POST'])
def enroll():
    if request.method == 'POST':
        username = request.form['username']
        if username in user_data:
            return redirect(url_for('already_enrolled', username=username))

        image = request.files['iris_image']
        filename = secure_filename(f'{username}_iris.jpg')
        image.save(os.path.join(UPLOAD_FOLDER, filename))
        user_data[username] = filename

        # Save updated user data to file
        with open(USER_DATA_FILE, 'w') as f:
            json.dump(user_data, f)

        return redirect(url_for('welcome', username=username))
    return render_template('enroll.html')

@app.route('/already_enrolled/<username>')
def already_enrolled(username):
    return render_template('already_enrolled.html', username=username)

@app.route('/welcome/<username>')
def welcome(username):
    return render_template('welcome.html', username=username)

@app.route('/authenticate', methods=['GET', 'POST'])
def authenticate():
    if request.method == 'POST':
        username = request.form['username']
        if username not in user_data:
            return "User not found!"

        auth_image = request.files['auth_image']
        enrolled_path = os.path.join(UPLOAD_FOLDER, user_data[username])
        auth_path = os.path.join(UPLOAD_FOLDER, f'{username}_auth_attempt.jpg')
        auth_image.save(auth_path)

        if os.path.getsize(enrolled_path) == os.path.getsize(auth_path):
            return redirect(url_for('auth_success', username=username))
        else:
            return redirect(url_for('auth_fail', username=username))
    return render_template('authenticate.html')

@app.route('/auth_success/<username>')
def auth_success(username):
    return render_template('auth_success.html', username=username)

@app.route('/auth_fail/<username>')
def auth_fail(username):
    return render_template('auth_fail.html', username=username)

if __name__ == '__main__':
    app.run(debug=True)
