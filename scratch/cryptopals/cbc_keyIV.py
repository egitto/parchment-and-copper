from cbc import CBC_encrypt, CBC_decrypt
from padPKCS7 import pad, unpad
import random
from bytestring_tools import data, random_bytes, xor
import codecs

# Recover the key from CBC with IV=Key

# Using the key as an IV is insecure; an attacker that can modify ciphertext in flight can get the receiver to decrypt a value that will reveal the key.

# The CBC code from exercise 16 encrypts a URL string. Verify each byte of the plaintext for ASCII compliance (ie, look for high-ASCII values). Noncompliant messages should raise an exception or return an error that includes the decrypted plaintext (this happens all the time in real systems, for what it's worth).

# Use your code to encrypt a message that is at least 3 blocks long:
# AES-CBC(P_1, P_2, P_3) -> C_1, C_2, C_3

class ASCII_noncompliance(Exception):
  pass

key = b'\xcb\xe5\xe1F\xc6x\x9ajk\xc4\xe3\xd3\x9f\xc3O\x14'
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
def get_iv():
  cyphertext = cyphered_comment(b'')
  try: is_admin(cyphertext[:16]+b'\x00'*16+cyphertext)
  except Exception as e: plain = (e.args[0][20:-1]) # 18 is the length of the cruft
  plain = codecs.escape_decode(bytes(plain, "utf-8"))[0] 
  return xor(plain[:16],plain[32:48])

def fake_admin():
  key = iv = get_iv()
  return CBC_encrypt(pad(b';admin=true;'),key,iv)

print(is_admin(fake_admin()))
