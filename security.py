from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.serialization import load_pem_private_key, load_pem_public_key
import re
import os
import base64

PRIVATE_KEY_PATH = 'keys/private.pem'
PUBLIC_KEY_PATH = 'keys/public.pem'

def normalize_name(name):
    return re.sub(r'[^a-zA-Z0-9._-]', '_', name)

def store_public_key(key, name = 'public'):
    name = normalize_name(name)
    
    if isinstance(key, str):
        key = load_pem_public_key(key.encode('utf-8'))
    
    public_pem = key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    )
    
    with open(f"keys/{name}.pem", 'wb') as file:
        file.write(public_pem)

def generate_keys():
    os.makedirs(os.path.dirname(PRIVATE_KEY_PATH), exist_ok=True)
    
    private_key = rsa.generate_private_key(
        public_exponent=65537, 
        key_size=2048
    )
    
    private_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )
    
    with open(PRIVATE_KEY_PATH, 'wb') as file:
        file.write(private_pem)
        
    store_public_key(private_key.public_key())
        
def get_private_key():
    return get_private_key_obj().private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    ).decode('utf-8')

def get_private_key_obj():
    key = None
    with open(PRIVATE_KEY_PATH, 'rb') as file:
        key = load_pem_private_key(file.read(), password=None)
    return key

# Loads system if none passed
def get_public_key(file = 'public'):
    return get_public_key_obj(file).public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    ).decode('utf-8')

def get_public_key_obj(file = 'public'):
    key = None
    file_name = normalize_name(file)
    
    with open(f"keys/{file_name}.pem", 'rb') as file:
        key = load_pem_public_key(file.read())
    return key
    

def encrypt_message(message, public_key):
    bytes = public_key.encrypt(
        message.encode(),
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    
    return base64.b64encode(bytes).decode('utf-8')
    
def decrypt_message(message):    
    bytes =  get_private_key_obj().decrypt(
        base64.b64decode(message),
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    
    return bytes.decode('utf-8')