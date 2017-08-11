from cpt5 import data
from cbc import CBC_encrypt, CBC_decrypt
from padPKCS7 import pad, unpad, PaddingError
import random

key = int.to_bytes(random.getrandbits(16*8),16,'big') # I really need to put this in a library somewhere
def encrypt_one_token():
  tokens = ['MDAwMDAwTm93IHRoYXQgdGhlIHBhcnR5IGlzIGp1bXBpbmc=',
  'MDAwMDAxV2l0aCB0aGUgYmFzcyBraWNrZWQgaW4gYW5kIHRoZSBWZWdhJ3MgYXJlIHB1bXBpbic=','MDAwMDAyUXVpY2sgdG8gdGhlIHBvaW50LCB0byB0aGUgcG9pbnQsIG5vIGZha2luZw==','MDAwMDAzQ29va2luZyBNQydzIGxpa2UgYSBwb3VuZCBvZiBiYWNvbg==','MDAwMDA0QnVybmluZyAnZW0sIGlmIHlvdSBhaW4ndCBxdWljayBhbmQgbmltYmxl','MDAwMDA1SSBnbyBjcmF6eSB3aGVuIEkgaGVhciBhIGN5bWJhbA==','MDAwMDA2QW5kIGEgaGlnaCBoYXQgd2l0aCBhIHNvdXBlZCB1cCB0ZW1wbw==','MDAwMDA3SSdtIG9uIGEgcm9sbCwgaXQncyB0aW1lIHRvIGdvIHNvbG8=','MDAwMDA4b2xsaW4nIGluIG15IGZpdmUgcG9pbnQgb2g=','MDAwMDA5aXRoIG15IHJhZy10b3AgZG93biBzbyBteSBoYWlyIGNhbiBibG93']
  token = data(random.sample(tokens,1)[0]).bytes
  iv = int.to_bytes(random.getrandbits(16*8),16,'big')
  return (iv,CBC_encrypt(pad(token,16),key,iv))

def check_padding(iv,token):
  decrypted = CBC_decrypt(token,key,iv)
  try: unpad(decrypted)
  except(PaddingError): return False
  return True

# print(check_padding(*encrypt_one_token()))

