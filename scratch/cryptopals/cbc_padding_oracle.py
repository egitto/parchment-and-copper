from cpt5 import data, xor
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

def break_block(block,oracle):
  right_bytes = b'' # invariant: rightbytes is the rightmost known bytes of plaintext.
  def l(): return len(right_bytes)
  # to check if the last byte is '\x01': 
  def leftpad(_bytes):
    return b'\x00'*(16-len(_bytes))+_bytes
  all_bytes = [int.to_bytes(x,1,'big') for x in range(256)]
  while l() < 16:
    padmask1 = pad(b'\x00'*(15-l()))[:16] # both padmasks have correct padding
    padmask2 = pad(b'\xFF'*(15-l()))[:16] # therefore, (padmask ^ plaintext ^ (leftpad(right_bytes))) has correct padding
    for x in all_bytes:
      test_bytes = leftpad(x+right_bytes)
      if oracle(xor(test_bytes,padmask1),block) and oracle(xor(test_bytes,padmask2),block):
        right_bytes = x+right_bytes
        break
  return xor(right_bytes,(b'\xFF'*16))

print(break_block(encrypt_one_token()[1][:16],check_padding))