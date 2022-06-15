import os

from Crypto.Protocol.KDF import PBKDF2

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

from dotenv import load_dotenv

load_dotenv() # For ENV variables


############# SIMPLE AES ENCRYPTION AND DECRYPTION  #############
def encrypt(data_to_encrypt, key):
    cipher = AES.new(key, AES.MODE_ECB)
    return cipher.encrypt(pad(data_to_encrypt, AES.block_size))

def decrypt(data_to_decrypt, key):
    cipher = AES.new(key, AES.MODE_ECB)
    return unpad(cipher.decrypt(data_to_decrypt), AES.block_size)


############### OTHER FUNCTIONS ###############

def generate_key():
    return  PBKDF2(os.getenv('MASTER_KEY'), salt=os.getenv('MASTER_KEY'), dkLen=32)


    