from ctr import CTR_encrypt
from padPKCS7 import pad, unpad
import random
from bytestring_tools import data

key = int.to_bytes(random.getrandbits(16*8),16,'big')
def cyphered_comment(comment):
  comment = '"comment1=cooking%20MCs;userdata="'+data(comment).ascii().replace("=","\=").replace(";","\;")+'";comment2=%20like%20a%20pound%20of%20bacon"'
  return CTR_encrypt(pad(data(comment).bytes),key) #counterfunction and nonce have default values

def is_admin(comment):
  # print(data(unpad(CTR_encrypt(comment,key))).bytes)
  return ";admin=true;" in data(unpad(CTR_encrypt(comment,key))).ascii()

def fake_admin():
  return (data(cyphered_comment("\x00"*12))^data("\x00"*34+";admin=true;")).bytes

print(is_admin(fake_admin()))