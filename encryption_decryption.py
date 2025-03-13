import os
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Protocol.KDF import PBKDF2
import base64
import json

class EncryptionDecryption:
    def __init__(self, password: str):
        self.salt = get_random_bytes(16)
        self.password = password
        self.key = self.derive_key()

    def derive_key(self) -> bytes:
        return PBKDF2(self.password, self.salt, dkLen=32)

    def encrypt(self, data: str) -> str:
        cipher = AES.new(self.key, AES.MODE_GCM)
        ciphertext, tag = cipher.encrypt_and_digest(data.encode('utf-8'))
        return base64.b64encode(self.salt + cipher.nonce + tag + ciphertext).decode('utf-8')

    def decrypt(self, encrypted_data: str) -> str:
        raw_data = base64.b64decode(encrypted_data.encode('utf-8'))
        salt = raw_data[:16]
        nonce = raw_data[16:32]
        tag = raw_data[32:48]
        ciphertext = raw_data[48:]
        key = PBKDF2(self.password, salt, dkLen=32)
        cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
        return cipher.decrypt_and_verify(ciphertext, tag).decode('utf-8')

    def save_to_file(self, filename: str, data: str):
        encrypted_data = self.encrypt(data)
        with open(filename, 'w') as f:
            f.write(json.dumps({'data': encrypted_data}))

    def load_from_file(self, filename: str) -> str:
        with open(filename, 'r') as f:
            data = json.load(f)
            return self.decrypt(data['data'])

def main():
    print("Encryption and Decryption System")
    password = input("Enter a password for encryption/decryption: ")
    ed = EncryptionDecryption(password)

    while True:
        choice = input("Choose an option: 1) Encrypt data 2) Decrypt data 3) Save to file 4) Load from file 5) Exit: ")

        if choice == '1':
            data = input("Enter data to encrypt: ")
            encrypted_data = ed.encrypt(data)
            print(f"Encrypted Data: {encrypted_data}")

        elif choice == '2':
            encrypted_data = input("Enter data to decrypt: ")
            try:
                decrypted_data = ed.decrypt(encrypted_data)
                print(f"Decrypted Data: {decrypted_data}")
            except Exception as e:
                print(f"Decryption failed: {str(e)}")

        elif choice == '3':
            data = input("Enter data to save: ")
            filename = input("Enter filename to save data: ")
            ed.save_to_file(filename, data)
            print(f"Data saved to {filename}")

        elif choice == '4':
            filename = input("Enter filename to load data: ")
            try:
                loaded_data = ed.load_from_file(filename)
                print(f"Loaded Data: {loaded_data}")
            except Exception as e:
                print(f"Failed to load data: {str(e)}")

        elif choice == '5':
            print("Exiting...")
            break
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main()