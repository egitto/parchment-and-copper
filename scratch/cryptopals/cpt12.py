from ecb import *
from cbc import *
from math import ceil
from padPKCS7 import pad, unpad

def oracle(input_bytes):
  unknown_string = data("Um9sbGluJyBpbiBteSA1LjAKV2l0aCBteSByYWctdG9wIGRvd24gc28gbXkgaGFpciBjYW4gYmxvdwpUaGUgZ2lybGllcyBvbiBzdGFuZGJ5IHdhdmluZyBqdXN0IHRvIHNheSBoaQpEaWQgeW91IHN0b3A/IE5vLCBJIGp1c3QgZHJvdmUgYnkK",'b64').bytes
  key = data("sdfKJH432480hnfidjanf430q9fa",'b64').bytes[0:16] # I'm pretending not to know what either of these are
  plaintext = input_bytes+unknown_string
  plaintext = pad(plaintext,16)
  return ECB_encrypt(plaintext,key)

def find_block_size(oracle):
  l = len(oracle(b""))
  padding = block_size = 0
  while l == len(oracle(b"1"*padding)): padding += 1
  while len(oracle(b"1"*padding)) == len(oracle(b"1"*(padding+block_size))): block_size += 1
  return {'block_size':block_size,'padding':padding-1}

# decrypt first byte of first block, then next, etc
def decrypt_next(prefix,next_index,all_chunked_frames,oracle=oracle,block_size=16):
  if prefix == b'':
    prefix = b'a'*(block_size-1)
  blocks_to_test = [(prefix+int.to_bytes(x,1,'big'))[-block_size:] for x in range(256)]
  try: next_char = {test_block(block,next_index,oracle,all_chunked_frames): block[-1] for block in blocks_to_test}[True]
  except(KeyError): 
    print('could not find next block',prefix)
    return b'\x00'
  return int.to_bytes(next_char,1,'big')

def generate_all_chunked_frames(block_size,oracle):
  return [chunk(oracle(b'a'*x),block_size) for x in range(block_size)][::-1]

def test_block(block,test_character_index,oracle,all_chunked_frames):
  block_size = len(all_chunked_frames[0][0])
  f = test_character_index % block_size
  b = test_character_index // block_size
  return oracle(block)[:block_size] == all_chunked_frames[f][b]

def decrypt_all(oracle=oracle):
  block_size = find_block_size(oracle)['block_size']
  accum = b'a'*block_size
  padding = find_block_size(oracle)['padding'] # padding on the actual message
  all_chunked_frames = generate_all_chunked_frames(block_size,oracle)
  for i in range(len(oracle(b''))-padding):
    accum += decrypt_next(accum,i,all_chunked_frames,oracle,block_size)
  return accum[block_size:]

# print(decrypt_all(oracle))