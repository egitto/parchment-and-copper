from mersenne import *
from bytestring_tools import data, xor
from math import ceil
import random
import time
 
# You can create a trivial stream cipher out of any PRNG; use it to generate a sequence of 8 bit outputs and call those outputs a keystream. XOR each byte of plaintext with each successive byte of keystream.
# Write the function that does this for MT19937 using a 16-bit seed. Verify that you can encrypt and decrypt properly. This code should look similar to your CTR code.
class MT_cypher():
  def __init__(self,seed):
    self.mt = twister(int.from_bytes(seed,'big'))
    self.i = 0  # bytes extracted so far
    self.dword = int.to_bytes(self.mt.extract_number(),4,'big')

  def encrypt(self,_bytes):
    return xor(_bytes,self.keystream(len(_bytes)))

  def clone(self):
    x = MT_cypher(b'aaaa')
    x.mt = self.mt.clone()
    x.i = self.i
    x.dword = self.dword
    return x

  def keystream(self,n):
    di = self.i%4
    more_dwords = ceil((n-(3-di))/4)
    accum = self.dword
    accum += b''.join([int.to_bytes(x,4,'big') for x in self.mt.extract_numbers(more_dwords)])
    self.dword = accum[-4:]
    self.i += n
    return accum[di:n+di]

# Use your function to encrypt a known plaintext (say, 14 consecutive 'A' characters) prefixed by a random number of random characters.
def two_byte_MT_encode(plaintext):
  prefix = int.to_bytes(random.getrandbits(160*8),160,'big')[:random.randint(1,50)]
  key = int.to_bytes(random.getrandbits(2*8),2,'big')
  return MT_cypher(key).encrypt(prefix+plaintext)

def possible_bytes(length):
  return [int.to_bytes(x,length,'big') for x in range(2**(8*length))]

# From the ciphertext, recover the "key" (the 16 bit seed).
def brute_force_MT(cypher_funct,keysize):
  # it's only 2 bytes; this still takes suprisingly long, b/c inefficient implementations, but it works.
  plaintext = b'm'*16
  cyphertext = cypher_funct(plaintext)
  for key in possible_bytes(keysize):
    if plaintext == MT_cypher(key).encrypt(cyphertext)[-len(plaintext):]: return key
  return None

# Use the same idea to generate a random "password reset token" using MT19937 seeded from the current time.
def password_token_generate():
  key = int.to_bytes(int(time.time())%(2**16),2,'big')
  return MT_cypher(key).keystream(64)

# Write a function to check if any given password token is actually the product of an MT19937 PRNG seeded with the current time.
def is_MT_seeded_with_time(cyphertext):
  t = int(time.time())%2**16
  l = len(cyphertext)
  for t in range(t,t-600,-1): # lets check the last 10 seconds too
    key = int.to_bytes(t,2,'big')
    if MT_cypher(key).keystream(l) == cyphertext: return True
  return False

print(is_MT_seeded_with_time(password_token_generate()))
# print(brute_force_MT(two_byte_MT_encode,2))


