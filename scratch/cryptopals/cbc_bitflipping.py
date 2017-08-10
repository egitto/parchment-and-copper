from cbc import CBC_encrypt, CBC_decrypt
from padPKCS7 import pad, unpad
import random
from cpt5 import data

key = int.to_bytes(random.getrandbits(16*8),16,'big')
def cyphered_comment(comment_text):
  comment = '"comment1=cooking%20MCs;userdata="'+comment_text.replace("=","\=").replace(";","\;")+'";comment2=%20like%20a%20pound%20of%20bacon"'
  return CBC_encrypt(pad(data(comment).bytes),key)

def is_admin(comment):
  print(data(unpad(CBC_decrypt(comment,key))).ascii())
  return ";admin=true;" in data(unpad(CBC_decrypt(comment,key))).ascii()

class fake_string(str):  #this is not the solution they had in mind :P
  def __init__(self, contents):
    str.__init__(self)
  def replace(self,a,b):
    return self

print(is_admin(cyphered_comment(fake_string(";admin=true;"))))
