from cpt5 import data, xor
from cbc import CBC_encrypt, CBC_decrypt
from padPKCS7 import pad, unpad, PaddingError
import random

key = data(b"YELLOW SUBMARINE").bytes
# key = int.to_bytes(random.getrandbits(16*8),16,'big') # I really need to put this in a library somewhere
def encrypt_one_token():
  tokens = ['AAAAAAAAAAAAAAAAAAAAAAAAAAAAA','MDAwMDAwTm93IHRoYXQgdGhlIHBhcnR5IGlzIGp1bXBpbmc=',
  'MDAwMDAxV2l0aCB0aGUgYmFzcyBraWNrZWQgaW4gYW5kIHRoZSBWZWdhJ3MgYXJlIHB1bXBpbic=','MDAwMDAyUXVpY2sgdG8gdGhlIHBvaW50LCB0byB0aGUgcG9pbnQsIG5vIGZha2luZw==','MDAwMDAzQ29va2luZyBNQydzIGxpa2UgYSBwb3VuZCBvZiBiYWNvbg==','MDAwMDA0QnVybmluZyAnZW0sIGlmIHlvdSBhaW4ndCBxdWljayBhbmQgbmltYmxl','MDAwMDA1SSBnbyBjcmF6eSB3aGVuIEkgaGVhciBhIGN5bWJhbA==','MDAwMDA2QW5kIGEgaGlnaCBoYXQgd2l0aCBhIHNvdXBlZCB1cCB0ZW1wbw==','MDAwMDA3SSdtIG9uIGEgcm9sbCwgaXQncyB0aW1lIHRvIGdvIHNvbG8=','MDAwMDA4b2xsaW4nIGluIG15IGZpdmUgcG9pbnQgb2g=','MDAwMDA5aXRoIG15IHJhZy10b3AgZG93biBzbyBteSBoYWlyIGNhbiBibG93']
  token = data(tokens[0]).bytes
  # token = data(random.sample(tokens,1)[0]).bytes
  iv = key[::-1]
  # iv = int.to_bytes(random.getrandbits(16*8),16,'big')
  return (iv,CBC_encrypt(pad(token,16),key,iv))

def check_padding(iv,token):
  decrypted = CBC_decrypt(token,key,iv)
  try: unpad(decrypted)
  except(PaddingError): return False
  return True

# print(check_padding(*encrypt_one_token()))

def break_block(block,previous_block,oracle):
  """Decrypts a block encrypted with CBC using a padding oracle. written to use check_padding.
  """
  right_bytes = b'' # invariant: rightbytes is the rightmost known bytes of plaintext.
  l = 0
  def leftpad(_bytes): return b'\x00'*(16-len(_bytes))+_bytes
  all_bytes = [int.to_bytes(x,1,'big') for x in range(256)]
  while l < 16:
    padmask1 = pad(b'\x00'*(15-l)) # both padmasks have correct padding
    padmask2 = pad(b'\xFF'*(15-l)) # therefore, (padmask ^ plaintext ^ (leftpad(right_bytes))) has correct padding
    for x in all_bytes:
      test_bytes = xor(leftpad(x+right_bytes),previous_block) #DUH
      if oracle(xor(test_bytes,padmask1),block) and oracle(xor(test_bytes,padmask2),block):
        right_bytes = x+right_bytes
        print(l)
        break
    l += 1
  return xor(right_bytes,(b'\x00'*16))

def steal_last_byte(block,oracle):
  all_bytes = [int.to_bytes(x,1,'big') for x in range(256)]
  def lp(_bytes): return b'\x00'*(16-len(_bytes))+_bytes
  for x in all_bytes:
    # when plaintext = b'A'*16 and x = lp(b'A'): x ^ plaintext ^ lp('\x01') == 
    if oracle(xor(lp(x),lp(b'\x01')),block): return x
  return 'Failure'


print(break_block(encrypt_one_token()[1][:16],check_padding))
print(steal_last_byte(encrypt_one_token()[1][:16],check_padding))