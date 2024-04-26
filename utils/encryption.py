from Crypto.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Random import get_random_bytes
from base64 import b64encode, b64decode

def derive_key(password: str, salt: bytes, iterations=100000) -> bytes:
    """
    Derive a cryptographic key from a password using PBKDF2.
    
    Args:
    - password (str): The password to derive from.
    - salt (bytes): A random salt.
    - iterations (int): Number of iterations to use for key derivation.
    
    Returns:
    - bytes: The derived key.
    """
    key = PBKDF2(password, salt, dkLen=32, count=iterations)  # AES-256 requires a 32-byte key
    return key

def encrypt(plain_text: str, password: str) -> dict:
    """
    Encrypt the plaintext using AES encryption in GCM mode.
    
    Args:
    - plain_text (str): Text to encrypt.
    - password (str): Password to derive the encryption key from.
    
    Returns:
    - dict: Dictionary containing encrypted text and its associated data.
    """
    salt = get_random_bytes(16)  # Generate a 128-bit salt
    key = derive_key(password, salt)
    cipher = AES.new(key, AES.MODE_GCM)
    ciphertext, tag = cipher.encrypt_and_digest(plain_text.encode('utf-8'))
    return {
        'ciphertext': b64encode(ciphertext).decode('utf-8'),
        'salt': b64encode(salt).decode('utf-8'),
        'nonce': b64encode(cipher.nonce).decode('utf-8'),
        'tag': b64encode(tag).decode('utf-8')
    }

def decrypt(enc_dict: dict, password: str) -> str:
    """
    Decrypt the ciphertext using AES decryption in GCM mode.
    
    Args:
    - enc_dict (dict): Dictionary containing the encrypted text and associated data.
    - password (str): Password to derive the decryption key from.
    
    Returns:
    - str: The decrypted plaintext.
    """
    salt = b64decode(enc_dict['salt'])
    key = derive_key(password, salt)
    nonce = b64decode(enc_dict['nonce'])
    tag = b64decode(enc_dict['tag'])
    cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
    decrypted_text = cipher.decrypt_and_verify(b64decode(enc_dict['ciphertext']), tag)
    return decrypted_text.decode('utf-8')

# Example usage:
if __name__ == '__main__':
    password_to_encrypt = 'mypassword'
    user_password = 'userpassword123' 

    encrypted = encrypt(password_to_encrypt, user_password)
    print(f"Encrypted: {encrypted}")

    decrypted = decrypt(encrypted, user_password)
    print(f"Decrypted: {decrypted}")
