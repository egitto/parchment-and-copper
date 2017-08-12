#!/bin/python
from Crypto.Cipher import AES 
from bytestring_tools import *
import base64

def apply(initial_value,fxns):
  a = initial_value
  for f in fxns: a = f(a)
  return a

def ECB_decrypt(encrypted_bytes,key=b'YELLOW SUBMARINE'):
  # text2 = base64.decodebytes(bytes(text,"UTF-8"))
  encryption = AES.new(key, AES.MODE_ECB)
  return encryption.decrypt(encrypted_bytes)

def ECB_encrypt(plaintext_bytes,key=b'YELLOW SUBMARINE'):
  encryption = AES.new(key, AES.MODE_ECB)
  return encryption.encrypt(plaintext_bytes)

# key = data("YELLOW SUBMARINE")
# text = open("cryptopals_7.txt").readlines()
# text = "".join([x.strip() for x in text])
# text2 = base64.decodebytes(bytes(text,"UTF-8"))
# text = data(text,"b64")
# # print(bytes(text.ascii(),"UTF-8"))
# # print(text2 == text)

# encryption = AES.new(b"YELLOW SUBMARINE", AES.MODE_ECB)
# print(encryption.decrypt(text2))

def b64_file_to_bytes(path):
  text = open(path).readlines()
  text = "".join([x.strip() for x in text])
  return data(text,'b64').bytes

# text = b64_file_to_bytes('cryptopals_7.txt')
# print(ECB_decrypt(text,b'YELLOW SUBMARINE'))
# print(ECB_decrypt(ECB_encrypt(ECB_decrypt(text))))
# print(apply(text,[ECB_encrypt,ECB_encrypt,ECB_decrypt,ECB_decrypt,ECB_decrypt]))