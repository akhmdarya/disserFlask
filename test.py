from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

# Define the key and message to encrypt
key = b'abcdefghijklmnop'
message = b'This is a secret message.'

# Create the AES cipher object and encrypt the message
cipher = AES.new(key, AES.MODE_ECB)
ciphertext = cipher.encrypt(pad(message, AES.block_size))

# Convert the ciphertext to hexadecimal format
hex_ciphertext = ciphertext.hex()

# Print the hexadecimal ciphertext
print(hex_ciphertext)


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


# Convert the hexadecimal ciphertext to bytes
ciphertext = bytes.fromhex(hex_ciphertext)

# Create the AES cipher object and decrypt the message
cipher = AES.new(key, AES.MODE_ECB)
plaintext = unpad(cipher.decrypt(ciphertext), AES.block_size)

# Print the decrypted message
print(plaintext.decode())