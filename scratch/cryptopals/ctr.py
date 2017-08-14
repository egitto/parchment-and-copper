from cbc import CBC_encrypt
from ecb import ECB_encrypt
from bytestring_tools import xor, data
from math import ceil

def counter_function(n):
  return int.to_bytes(n,9,'big')+b'\x00'*7

def CTR_keystream(key,counter_function,length,start):
  # start = nonce = first byte we haven't generated keystream for yet
  # I have a feeling this isn't how I should use nonces, but
  # this matches the problem specification. Should have more flexible way, though
  block_n = start//16
  n = start%16
  accum = ECB_encrypt(counter_function(block_n),key)[n:]
  for _ in range(ceil((length)/16)):
    block_n += 1
    accum += ECB_encrypt(counter_function(block_n),key)
  return accum[:length]

def CTR_encrypt(_bytes,key,counter_function=counter_function,nonce=0):
  return xor(_bytes,CTR_keystream(key,counter_function,len(_bytes),nonce))

class CTR_cypher():
  def __init__(self,key,counter_function=counter_function,nonce=0):
    self.key = key
    self.counter_function = counter_function
    self.zero = nonce
    self.n = nonce

  def set_offset(self,offset):
    self.n = self.zero + offset

  def encrypt(self,_bytes):
    x = CTR_encrypt(_bytes,self.key,self.counter_function,self.n)
    self.n += len(_bytes)
    return x

# a = CTR_cypher(b'yellow submarine',counter_function,0)
# b = a.encrypt(b'some stuff')
# a.set_offset(0)
# print(a.encrypt(b))

# cyphertext = data('L77na/nrFsKvynd6HzOoG7GHTLXsTVu9qvY/2syLXzhPweyyMTJULu/6/kXX0KSvoOLSFQ==','b64').bytes
# print(CTR_encrypt(cyphertext,"YELLOW SUBMARINE",counter_function,0))
