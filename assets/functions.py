from Cryptodome.Cipher import AES
from secrets import token_bytes
import hashlib
from pyDes import *

############# ENCRYPTION AND DECRYPTION FOR PASSWORDS #############
def encrypt_password(string_to_encrypt,key):
    key = sha_256hash(key)
    cipher = AES.new(key,AES.MODE_EAX)
    nonce = cipher.nonce
    cipher_text,tag = cipher.encrypt_and_digest(string_to_encrypt.encode())
    return nonce,cipher_text,tag

def decrypt_password(nonce, encrypted_text, tag, key):
    key = sha_256hash(key)
    cipher = AES.new(key,AES.MODE_EAX,nonce)
    plain_text = cipher.decrypt_and_verify(encrypted_text,tag)
    return plain_text.decode()


############# ENCRYPTION AND DECRYPTION FOR MASTER KEY #############
def encrypt_master_key(string_to_encrypt,key):
    return triple_des(string_to_encrypt.encrypt(key),padmode=2)

def decrypt_master_key(string_to_decrypt,key):
    return triple_des(string_to_decrypt.decrypt(key),padmode=2)
    
############### OTHER FUNCTIONS ###############
def sha_256hash(string_to_hash):
    return hashlib.sha256(string_to_hash.encode('utf-8')).digest()
