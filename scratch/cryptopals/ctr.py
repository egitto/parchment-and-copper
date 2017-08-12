from cbc import CBC_encrypt
from ecb import ECB_encrypt
from bytestring_tools import xor, data
from math import ceil

def counter_function(n,nonce):
  return int.to_bytes(n+nonce,9,'big')+b'\x00'*7

def CTR_keystream(key,counter_function,length,nonce):
  accum = b''
  for i in range(ceil(length/len(key))):
    accum += ECB_encrypt(counter_function(i,nonce),key)
  return accum[:length]

def CTR_encrypt(_bytes,key,counter_function,nonce):
  return xor(_bytes,CTR_keystream(key,counter_function,len(_bytes),nonce))

cyphertext = data('L77na/nrFsKvynd6HzOoG7GHTLXsTVu9qvY/2syLXzhPweyyMTJULu/6/kXX0KSvoOLSFQ==','b64').bytes
print(CTR_encrypt(cyphertext,"YELLOW SUBMARINE",counter_function,0))
