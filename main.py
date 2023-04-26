import os
import cv2
from PIL import Image
import app as app
from classes import LSB, DCT
from flask import Flask, flash, request, redirect, url_for,jsonify,session
from flask_cors import CORS
from io import BytesIO
from werkzeug.utils import secure_filename
APP_ROOT = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLD = 'F:/disserApplication/backend'

UPLOAD_FOLDER = os.path.join(APP_ROOT, UPLOAD_FOLD)

# os.path.abspath("C:/example/cwd/mydir/myfile.txt")

ALLOWED_EXTENSIONS = {"MP3", "WAV","JPEG", "PNG", "GIF"}

app = Flask(__name__)
CORS(app)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
data =""
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/uploadMessage', methods=['POST'])
def upload_msg():
    global data
    try:
        data = request.json
        return "Success"
    except Exception as e:
        print(f"((((()))))")
    return "Something wrong"

@app.route('/upload', methods=['POST'])
def upload_file():
    target=os.path.join(UPLOAD_FOLDER,'uploads')
    if not os.path.isdir(target):
        os.mkdir(target)
    d = ""
    try:
        # file = request.files['file_from_react']
        # filename = "upl.png"
        # # print(f"Uploading file {filename}")
        # destination = "/".join([target, filename])
        # file.save(destination)
        #
        # original_image_file = f'F:/disserApplication/backend/uploads/upl.png'
        # lsb_img = Image.open(original_image_file)
        # dct_img = cv2.imread(original_image_file, cv2.IMREAD_UNCHANGED)
        # print(f"Uploading file {dct_img}")
        #
        # secret_msg = data
        # print("The message length is: ", len(secret_msg))
        # lsb_img_encoded = LSB().encode_image(lsb_img, secret_msg)
        # # dct_img_encoded = DCT().encode_image(dct_img, secret_msg)
        # # lsb_encoded_image_file ="lsb_" + original_image_file
        #
        # lsb_img_encoded.save(f'F:/disserApplication/backend/uploads/stego_image.png')
        # # lsb_img_encoded.save(lsb_encoded_image_file)
        # dct_encoded_image_file = "dct_" + original_image_file
        # # cv2.imwrite(dct_encoded_image_file, dct_img_encoded)


        encoded_image_file = f'F:/disserApplication/backend/uploads/stego_image.png'
        lsb_img = Image.open(encoded_image_file)
        lsb_hidden_text = LSB().decode_image(lsb_img)

        print(f"!!!!!!!!!!!!!!!!!!!! {lsb_hidden_text}")

        d = "Success"

    except Exception as e:
        print(f"Couldn't upload file {e}")
        d = "(("

    return jsonify(d)









