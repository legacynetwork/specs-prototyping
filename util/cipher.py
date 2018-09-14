from hashlib import sha256
from Crypto.Cipher import AES
import base64

class AESCipher:

    def __init__(self, key):        
        self.key = sha256(key.encode()).digest()
        self.BLOCK_SIZE = 16 # AES operates on block multiples of 16 bytes (128 bits)

    def encrypt(self, raw):
        raw = self.pad(raw)        
        encryption_suite = AES.new(self.key, AES.MODE_ECB)
        return base64.b64encode(encryption_suite.encrypt(raw)) 

    def decrypt(self, enc):
        enc = base64.b64decode(enc)
        iv = enc[:16]
        cipher = AES.new(self.key, AES.MODE_CBC, iv )
        return unpad(cipher.decrypt( enc[16:] )) # TODO

    def pad(self, s):
        return s + (self.BLOCK_SIZE - len(s) % self.BLOCK_SIZE) * chr(self.BLOCK_SIZE - len(s) % self.BLOCK_SIZE)