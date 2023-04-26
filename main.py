import os

import app as app
from flask import Flask, flash, request, redirect, url_for,jsonify,session
from flask_cors import CORS
from io import BytesIO
from werkzeug.utils import secure_filename
APP_ROOT = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLD = 'F:/disserApplication/backend'
UPLOAD_FOLDER = os.path.join(APP_ROOT, UPLOAD_FOLD)

ALLOWED_EXTENSIONS = {"MP3", "WAV","JPEG", "PNG", "GIF"}

app = Flask(__name__)
CORS(app)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['POST'])
def upload_file():
    target=os.path.join(UPLOAD_FOLDER,'uploads')
    if not os.path.isdir(target):
        os.mkdir(target)
    d = ""
    try:
        file = request.files['file_from_react']
        filename = "upl.png"
        print(f"Uploading file {filename}")
        destination = "/".join([target, filename])
        file.save(destination)


        d = "Success"

    except Exception as e:
        print(f"Couldn't upload file {e}")
        d = "(("

    return jsonify(d)