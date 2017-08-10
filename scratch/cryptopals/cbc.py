from ecb import *

def CBC_decrypt(encrypted_bytes,key=b'YELLOW SUBMARINE',iv=bytes(16)):
  blocks = chunk(encrypted_bytes,16)
  decrypted = b''
  a = data(iv)
  for cypherblock in blocks:
    decrypted += (data(ECB_decrypt(cypherblock,key)) ^ a).bytes
    a = data(cypherblock)
  return decrypted

def CBC_encrypt(plaintext_bytes,key=b'YELLOW SUBMARINE',iv=bytes(16)):
  blocks = chunk(plaintext_bytes,16)
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
