import os
import cv2
from Crypto.Cipher import AES
from PIL import Image
import secrets
import app as app
from classes import LSB, DCT, Compare, ModMLSB
from flask import Flask, flash, request, redirect, url_for,jsonify,session
from flask_cors import CORS

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import base64
from io import BytesIO

from modifiedclasses import Median

key = b'abcdefghijklmnop'
from werkzeug.utils import secure_filename
APP_ROOT = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLD = 'F:/disserApplication/backend'

flagLSB=0
flagAESLSB=0
flagMedian=0
flagGauss=0

UPLOAD_FOLDER = os.path.join(APP_ROOT, UPLOAD_FOLD)

# os.path.abspath("C:/example/cwd/mydir/myfile.txt")

ALLOWED_EXTENSIONS = {"MP3", "WAV","JPEG", "PNG", "JPG"}

app = Flask(__name__)
CORS(app)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
data =""


# key = secrets.token_bytes(16)  # generates a 16-byte (128-bit) key
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
# =============================================LSB
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
        file = request.files['file_from_react']
        filename = "uplLSB.png"
        destination = "/".join([target, filename])
        file.save(destination)
        original_image_file = f'F:/disserApplication/backend/uploads/uplLSB.png'
        lsb_img = Image.open(original_image_file)
        secret_msg = data
        print("The message length is: ", len(secret_msg))
        lsb_img_encoded = LSB().encode_image(lsb_img, secret_msg)
        lsb_img_encoded.save(f'F:/disserApplication/backend/uploads/stego_imageLSB.png')
        d = "Success"
        return jsonify(d)

    except Exception as e:
        print(f"Couldn't upload file {e}")
        d = "(("
        return jsonify(e)


@app.route('/uploadDecode', methods=['POST'])
def decode_file():

    try:
        fileToDecode = request.files['file_from_react_toDecode']
        lsb_img = Image.open(fileToDecode)
        lsb_hidden_text = LSB().decode_image(lsb_img)
        print(f"!!!!!!!!!!!!!!!!!!!! {lsb_hidden_text}")
        d = lsb_hidden_text
        return jsonify(d)
    except Exception as e:
        print(f"Couldn't upload file {e}")
        d = "(("
        return jsonify(e)
# =============================================DCT
@app.route('/uploadMessageDCT', methods=['POST'])
def upload_msgDCT():
    global data
    try:
        data = request.json
        return "Success"
    except Exception as e:
        print(f"((((()))))")
    return "Something wrong"

@app.route('/uploadDCT', methods=['POST'])
def upload_fileDCT():
    target=os.path.join(UPLOAD_FOLDER,'uploads')
    if not os.path.isdir(target):
        os.mkdir(target)
    d = ""
    try:
        file = request.files['file_from_react']
        filename = "uplDCT.png"
        # print(f"Uploading file {filename}")
        destination = "/".join([target, filename])
        file.save(destination)
        image = Image.open(f'F:/disserApplication/backend/uploads/uplDCT.png')
        image = image.convert('RGB')
        image.save(destination)
        original_image_file = f'F:/disserApplication/backend/uploads/uplDCT.png'
        dct_img = cv2.imread(original_image_file, cv2.IMREAD_UNCHANGED)
        secret_msg = data
        print("The message length is: ", len(secret_msg))
        dct_img_encoded, flagDCT = DCT().encode_image(dct_img, secret_msg)
        print(f"flagDCT {flagDCT}")

        dct_encoded_image_file = f'F:/disserApplication/backend/uploads/stego_imageDCT.png'
        cv2.imwrite(dct_encoded_image_file, dct_img_encoded)
        d = "Success"
        return jsonify(d)

    except Exception as e:
        print(f"Couldn't upload file {e}")
        d = e
        return jsonify(d)


@app.route('/uploadDecodeDCT', methods=['POST'])

def decode_fileDCT():
    target = os.path.join(UPLOAD_FOLDER, 'uploads')
    if not os.path.isdir(target):
        os.mkdir(target)

    try:
        fileToDecode = request.files['file_from_react_toDecode']
        filename = "stego_imageDCT.png"
        # print(f"Uploading file {filename}")
        destination = "/".join([target, filename])
        fileToDecode.save(destination)

        original_image_file = f'F:/disserApplication/backend/uploads/stego_imageDCT.png'
        dct_img = cv2.imread(original_image_file, cv2.IMREAD_UNCHANGED)
        dct_hidden_text = DCT().decode_image(dct_img)
        d = dct_hidden_text
        return jsonify(d)

    except Exception as e:
        print(f"Couldn't upload file {e}")
        d = e
        return jsonify(d)

# =============================================MOD M LSB
@app.route('/uploadMessageModM', methods=['POST'])
def upload_msgModM():
    global data
    try:
        data = request.json
        return "Success"
    except Exception as e:
        print(f"((((()))))")
    return "Something wrong"

@app.route('/uploadModM', methods=['POST'])
def upload_fileModM():
    target=os.path.join(UPLOAD_FOLDER,'uploads')
    if not os.path.isdir(target):
        os.mkdir(target)
    d = ""
    try:
        file = request.files['file_from_react']
        filename = "uplModMLSB.png"
        destination = "/".join([target, filename])
        file.save(destination)
        original_image_file = f'F:/disserApplication/backend/uploads/uplModMLSB.png'
        lsb_img = Image.open(original_image_file)
        secret_msg = data
        secret_msg = secret_msg.encode('utf-8')
        cipher = AES.new(key, AES.MODE_ECB)
        ciphertext = cipher.encrypt(pad(secret_msg, AES.block_size))

        # Convert the ciphertext to hexadecimal format
        secret_msg = ciphertext.hex()

        print(secret_msg)
        lsb_img_encoded = ModMLSB().encode_image(lsb_img, secret_msg)
        lsb_img_encoded.save(f'F:/disserApplication/backend/uploads/stego_imageModMLSB.png')
        d = "Success"
        return jsonify((f"Decrypted AES message : {secret_msg}"))

    except Exception as e:
        print(f"Couldn't upload file {e}")
        d = "(("
        return e


@app.route('/uploadDecodeModM', methods=['POST'])
def decode_fileModM():

    try:
        fileToDecode = request.files['file_from_react_toDecode']
        lsb_img = Image.open(fileToDecode)
        lsb_hidden_text = ModMLSB().decode_image(lsb_img)
        print(f"!!!!!!!!!!!!!!!!!!!! {lsb_hidden_text}")
        d = lsb_hidden_text
        ciphertext = bytes.fromhex(d)

        # Create the AES cipher object and decrypt the message
        cipher = AES.new(key, AES.MODE_ECB)
        decrypted_message = unpad(cipher.decrypt(ciphertext), AES.block_size)
        message = decrypted_message.decode('utf-8')

        # Print the decrypted message
        print(f"DECODEEE {message}")
        return jsonify(message)
    except Exception as e:
        print(f"Couldn't upload file {e}")
        d = "(("
        return jsonify(e)

# =============================================LSB MEDIAN
@app.route('/uploadMessageMedian', methods=['POST'])
def upload_median():
    global data
    try:
        data = request.json
        return "Success"
    except Exception as e:
        print(f"((((()))))")
    return "Something wrong"

@app.route('/uploadMedian', methods=['POST'])
def upload_file_median():
    target=os.path.join(UPLOAD_FOLDER,'uploads')
    if not os.path.isdir(target):
        os.mkdir(target)
    d = ""
    try:
        file = request.files['file_from_react']
        filename = "uplMedian.png"
        destination = "/".join([target, filename])
        file.save(destination)
        original_image_file = f'F:/disserApplication/backend/uploads/uplMedian.png'
        lsb_img = Image.open(original_image_file)
        secret_msg = data
        print("The message length is: ", len(secret_msg))
        lsb_img_encoded = Median().encode_image(lsb_img, secret_msg)
        lsb_img_encoded.save(f'F:/disserApplication/backend/uploads/stego_imageMedian.png')
        d = "Success"
        return jsonify(d)

    except Exception as e:
        print(f"Couldn't upload file {e}")
        d = "(("
        return jsonify(e)


@app.route('/uploadDecodeMedian', methods=['POST'])
def decode_file_median():

    try:
        fileToDecode = request.files['file_from_react_toDecode']
        lsb_img = Image.open(fileToDecode)
        lsb_hidden_text = Median().decode_image(lsb_img)
        print(f"!!!!!!!!!!!!!!!!!!!! {lsb_hidden_text}")
        d = lsb_hidden_text
        return jsonify(d)
    except Exception as e:
        print(f"Couldn't upload file {e}")
        d = "(("
        return jsonify(e)

    # =============================================LSB Gauss
@app.route('/uploadMessageGauss', methods=['POST'])
def upload_gauss():
    global data
    try:
        data = request.json
        return "Success"
    except Exception as e:
        print(f"((((()))))")
    return "Something wrong"

@app.route('/uploadGauss', methods=['POST'])
def upload_file_gauss():
    target = os.path.join(UPLOAD_FOLDER, 'uploads')
    if not os.path.isdir(target):
        os.mkdir(target)
    d = ""
    try:
        file = request.files['file_from_react']
        filename = "uplGauss.png"
        destination = "/".join([target, filename])
        file.save(destination)
        original_image_file = f'F:/disserApplication/backend/uploads/uplGauss.png'
        lsb_img = Image.open(original_image_file)
        secret_msg = data
        print("The message length is: ", len(secret_msg))
        lsb_img_encoded = Median().encode_image(lsb_img, secret_msg)
        lsb_img_encoded.save(f'F:/disserApplication/backend/uploads/stego_imageGauss.png')
        d = "Success"
        return jsonify(d)

    except Exception as e:
        print(f"Couldn't upload file {e}")
        d = "(("
        return jsonify(e)

@app.route('/uploadDecodeGauss', methods=['POST'])
def decode_file_gauss():

    try:
        fileToDecode = request.files['file_from_react_toDecode']
        lsb_img = Image.open(fileToDecode)
        lsb_hidden_text = Median().decode_image(lsb_img)
        print(f"!!!!!!!!!!!!!!!!!!!! {lsb_hidden_text}")
        d = lsb_hidden_text
        return jsonify(d)
    except Exception as e:
        print(f"Couldn't upload file {e}")
        d = "(("
        return jsonify(e)


# =============================================Report

@app.route('/generateReport', methods=['GET'])
def report():
    try:
        originalDCT = cv2.imread(f'F:/disserApplication/backend/uploads/uplDCT.png')
        originalModLSB = cv2.imread(f'F:/disserApplication/backend/uploads/uplModMLSB.png')
        originalLSB = cv2.imread(f'F:/disserApplication/backend/uploads/uplLSB.png')
        originalMedian = cv2.imread(f'F:/disserApplication/backend/uploads/uplMedian.png')
        originalGauss = cv2.imread(f'F:/disserApplication/backend/uploads/uplGauss.png')
        medianEncoded = cv2.imread(f'F:/disserApplication/backend/uploads/stego_imageMedian.png')
        gaussEncoded = cv2.imread(f'F:/disserApplication/backend/uploads/stego_imageGauss.png')
        lsbEncoded = cv2.imread(f'F:/disserApplication/backend/uploads/stego_imageLSB.png')
        lsbModEncoded = cv2.imread(f'F:/disserApplication/backend/uploads/stego_imageModMLSB.png')
        dctEncoded = cv2.imread(f'F:/disserApplication/backend/uploads/stego_imageDCT.png')

#
        originalLSB = cv2.cvtColor(originalLSB, cv2.COLOR_BGR2RGB)
        originalMedian = cv2.cvtColor(originalMedian, cv2.COLOR_BGR2RGB)
        originalGauss = cv2.cvtColor(originalGauss, cv2.COLOR_BGR2RGB)
        originalModLSB = cv2.cvtColor(originalModLSB, cv2.COLOR_BGR2RGB)
        originalDCT = cv2.cvtColor(originalDCT, cv2.COLOR_BGR2RGB)
        median_encoded_img = cv2.cvtColor(medianEncoded, cv2.COLOR_BGR2RGB)
        gauss_encoded_img = cv2.cvtColor(gaussEncoded, cv2.COLOR_BGR2RGB)
        lsb_encoded_img = cv2.cvtColor(lsbEncoded, cv2.COLOR_BGR2RGB)
        lsb_mod_encoded_img = cv2.cvtColor(lsbModEncoded, cv2.COLOR_BGR2RGB)
        dct_encoded_img = cv2.cvtColor(dctEncoded, cv2.COLOR_BGR2RGB)


        list = [{
            "type":"LSB",
            "MSE": Compare().meanSquareError(originalLSB, lsb_encoded_img),
            "PSNR": Compare().psnr(originalLSB, lsb_encoded_img)},
            # "flag": flagDCT ,

            { "type":"DCT",
                "MSE": Compare().meanSquareError(originalDCT, dct_encoded_img),
            "PSNR": Compare().psnr(originalDCT, dct_encoded_img)},
            {"type": "AES LSB",
             "MSE": Compare().meanSquareError(originalModLSB, lsb_mod_encoded_img),
             "PSNR": Compare().psnr(originalModLSB, lsb_mod_encoded_img)}
            ,
            {"type": "Gauss LSB",
             "MSE": Compare().meanSquareError(originalGauss, gauss_encoded_img),
             "PSNR": Compare().psnr(originalGauss, gauss_encoded_img)}
            ,
            {"type": "Median LSB",
             "MSE": Compare().meanSquareError(originalMedian, median_encoded_img),
             "PSNR": Compare().psnr(originalMedian, median_encoded_img)}



        ]

        d = "success"
        return jsonify(list)
    except Exception as e:
        print(f"Couldn't upload file {e}")
        d = e
        return jsonify(d)






