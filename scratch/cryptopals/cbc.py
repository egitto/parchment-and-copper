from ecb import *
from padPKCS7 import pad

def CBC_decrypt(encrypted_bytes,key=b'YELLOW SUBMARINE',iv=bytes(16)):
  blocks = chunk(encrypted_bytes,len(key))
  decrypted = b''
  a = data(iv)
  for cypherblock in blocks:
    decrypted += (data(ECB_decrypt(cypherblock,key)) ^ a).bytes
    a = data(cypherblock)
  return decrypted

def CBC_encrypt(plaintext_bytes,key=b'YELLOW SUBMARINE',iv=bytes(16)):
  blocks = chunk(plaintext_bytes,len(key))
  if len(plaintext_bytes)%len(key) != 0: raise ValueError('Input strings must be a multiple of keylength in length')
  encrypted = b''
  a = data(iv)
  for plainblock in blocks:
    a = ECB_encrypt((data(plainblock) ^ a).bytes,key)
    encrypted += a
    a = data(a)
  return encrypted

# text = b64_file_to_bytes('cryptopals_10.txt')
# print(CBC_decrypt(text)) 
# print(apply(text,[CBC_decrypt]+[CBC_encrypt]*250+[CBC_decrypt]*250))
