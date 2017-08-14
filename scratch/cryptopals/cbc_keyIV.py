from cbc import CBC_encrypt, CBC_decrypt
from padPKCS7 import pad, unpad
import random
from bytestring_tools import data, random_bytes

# Recover the key from CBC with IV=Key

# Using the key as an IV is insecure; an attacker that can modify ciphertext in flight can get the receiver to decrypt a value that will reveal the key.

# The CBC code from exercise 16 encrypts a URL string. Verify each byte of the plaintext for ASCII compliance (ie, look for high-ASCII values). Noncompliant messages should raise an exception or return an error that includes the decrypted plaintext (this happens all the time in real systems, for what it's worth).

# Use your code to encrypt a message that is at least 3 blocks long:
# AES-CBC(P_1, P_2, P_3) -> C_1, C_2, C_3


class ASCII_noncompliance(Exception):
  pass

key = random_bytes(16)
def cyphered_comment(comment):
  comment = '"comment1=cooking%20MCs;userdata="'+data(comment).ascii().replace("=","\=").replace(";","\;")+'";comment2=%20like%20a%20pound%20of%20bacon"'
  return CBC_encrypt(pad(data(comment).bytes),key,iv=key)
  
def verify_ascii_compliance(bytestring):
  for i in bytestring:
    if i >= 127: raise ASCII_noncompliance('improper value in '+str(bytestring))

def is_admin(comment):
  # print(data(unpad(CBC_decrypt(comment,key))).bytes)
  unencrypted = data(unpad(CBC_decrypt(comment,key,iv=key)))
  verify_ascii_compliance(unencrypted.bytes)
  return ";admin=true;" in unencrypted.ascii()




# Modify the message (you are now the attacker):
# C_1, C_2, C_3 -> C_1, 0, C_1

# Decrypt the message (you are now the receiver) and raise the appropriate error if high-ASCII is found.
# As the attacker, recovering the plaintext from the error, extract the key:
# P'_1 XOR P'_3

def fake_admin():
  return (data(cyphered_comment("\x00"*32))^data("\x00"*32+";admin=true;")).bytes

print(is_admin(fake_admin()))