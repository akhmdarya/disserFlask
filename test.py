from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

# Define the key and message to encrypt
key = b'abcdefghijklmnop'
message = b'Th'

# Create the AES cipher object and encrypt the message
cipher = AES.new(key, AES.MODE_ECB)
ciphertext = cipher.encrypt(pad(message, AES.block_size))

# Convert the ciphertext to hexadecimal format
hex_ciphertext = ciphertext.hex()

# Print the hexadecimal ciphertext
print(hex_ciphertext)




# Convert the hexadecimal ciphertext to bytes
ciphertext = bytes.fromhex(hex_ciphertext)

# Create the AES cipher object and decrypt the message
cipher = AES.new(key, AES.MODE_ECB)
plaintext = unpad(cipher.decrypt(ciphertext), AES.block_size)

# Print the decrypted message
print(plaintext.decode())