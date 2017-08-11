from cbc import CBC_encrypt, CBC_decrypt
from padPKCS7 import pad, unpad
import random
from cpt5 import data

key = int.to_bytes(random.getrandbits(16*8),16,'big')
def cyphered_comment(comment_string):
  comment = '"comment1=cooking%20MCs;userdata="'+comment_string.replace("=","\=").replace(";","\;")+'";comment2=%20like%20a%20pound%20of%20bacon"'
  return CBC_encrypt(pad(data(comment).bytes),key)

def is_admin(comment):
  # print(data(unpad(CBC_decrypt(comment,key))).bytes)
  return ";admin=true;" in data(unpad(CBC_decrypt(comment,key))).ascii()

print(is_admin((data(cyphered_comment("\x00"*32))^data("\x00"*32+";admin=true;")).bytes))