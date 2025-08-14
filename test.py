import pyaes, pbkdf2, binascii, os, secrets
import base64

def getKey(): #generating AES key based on Diffie common secret shared key
    password = "s3cr3t*c0d3"
    passwordSalt = str("0986543")#get AES key using diffie
    key = pbkdf2.PBKDF2(password, passwordSalt).read(32)
    return key

def encrypt(plaintext): #AES data encryption
    aes = pyaes.AESModeOfOperationCTR(getKey(), pyaes.Counter(31129547035000047302952433967654195398124239844566322884172163637846056248223))
    ciphertext = aes.encrypt(plaintext)
    return ciphertext

def decrypt(enc): #AES data decryption
    aes = pyaes.AESModeOfOperationCTR(getKey(), pyaes.Counter(31129547035000047302952433967654195398124239844566322884172163637846056248223))
    decrypted = aes.decrypt(enc)
    return decrypted

text = "hello world"
encrypted = encrypt(text.encode())
print(encrypted)
encrypted = base64.b64encode(encrypted).decode()
print(encrypted)

encrypted = base64.b64decode(encrypted)
decrypt = decrypt(encrypted)
print(decrypt.decode())
