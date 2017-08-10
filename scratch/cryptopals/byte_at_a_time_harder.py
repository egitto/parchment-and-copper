# Take your oracle function from #12. Now generate a random count of random bytes and prepend this string to every plaintext. You are now doing:
# AES-128-ECB(random-prefix || attacker-controlled || target-bytes, random-key)
# Same goal: decrypt the target-bytes. 
from cpt12 import find_block_size
import cpt12
from cpt11 import random_key
from ecb import *
from cbc import *
from math import ceil
from padPKCS7 import pad, unpad
from cpt5 import chunk
import random

prefix_length = random.randint(1,32)
prefix = int.to_bytes(random.getrandbits(prefix_length*8),prefix_length,'big')
def oracle(input_bytes):
  return cpt12.oracle(prefix+input_bytes)

def find_prefix_length(oracle):
  block_size = find_block_size(oracle)

print(find_block_size(oracle))

def histogram_blocks(blocks):
  histogram = {block: 0 for block in blocks}
  for block in blocks: histogram[block] += 1
  return histogram

def find_cypherblock_of_filler(oracle,block_size):
  filler = b'a'*block_size
  more_filler_hist = histogram(chunk(oracle(filler*8),block_size))
  less_filler_hist = histogram(chunk(oracle(filler*7),block_size))
  return {more_filler_hist[block]-less_filler_hist[block]: block for block in more_filler_hist.keys()}[1]

filler_cyphered = find_cypherblock_of_filler(oracle,16)

def wrapped_oracle(input_bytes):