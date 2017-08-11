from cbc import CBC_encrypt, CBC_decrypt
from padPKCS7 import pad, unpad
import random
from cpt5 import data

key = int.to_bytes(random.getrandbits(16*8),16,'big')
def cyphered_comment(comment):
  comment = '"comment1=cooking%20MCs;userdata="'+data(comment).ascii().replace("=","\=").replace(";","\;")+'";comment2=%20like%20a%20pound%20of%20bacon"'
  return CBC_encrypt(pad(data(comment).bytes),key)

def is_admin(comment):
  # print(data(unpad(CBC_decrypt(comment,key))).bytes)
  return ";admin=true;" in data(unpad(CBC_decrypt(comment,key))).ascii()

def fake_admin():
  return (data(cyphered_comment("\x00"*320))^data("\x00"*320+";admin=true;")).bytes

print(is_admin(fake_admin()))