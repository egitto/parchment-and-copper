from bytestring_tools import data, xor
import time
from random import random

class twister():
  def __init__(self,seed):
    n = 624
    self.MT = [0]*n
    self.seed_mt(seed)

  def seed_mt(self,seed):
    f = 1812433253
    w = 32
    n = 624
    self.index = n
    self.MT[0] = seed
    for i in range(1,len(self.MT)):
      self.MT[i] = (f*(self.MT[i-1]^(self.MT[i-1]>>(w-2)))+i)&((1<<32)-1)
    # print(self.MT[:5],'initialized')

  class SeedError(Exception):
    pass

  def extract_number(self):
    n = 624
    w, l = 32, 18
    u, d = 11, 0xFFFFFFFF
    s, b = 7, 0x9D2C5680
    t, c = 15, 0xEFC60000
    if self.index >= n:
      if self.index > n: raise SeedError("Generator never seeded")
      self.twist()
    y = self.MT[self.index]
    # print(y,'actual state')
    # pp(y, 'actual')
    # aa = y
    y ^= (y>>11)&d #is the masking necessary at all?
    # pp(y, 'encoded')
    # bb = y
    # bb = undo_xor_rshift_mask(y,11,d)
    # print(bin(bb),aa==bb,bin(aa^bb))
    y ^= (y<<7)&b
    y ^= (y<<15)&c
    y ^= (y>>18)
    y = y&((1<<w)-1)
    self.index += 1
    return y

  def twist(self):
    n, m, r, = 624, 397, 31
    a = 0x9908B0DF
    upper_mask = (1<<r)
    lower_mask = upper_mask-1
    for i in range(n):
      x = (self.MT[i]&upper_mask)+((self.MT[(i+1)%n])&lower_mask)
      xA = x>>1
      if x%2: xA^=a
      self.MT[i] = self.MT[(i+m)%n]^xA # the lower_mask part of MT[0] gets thrown away completely?? irretrievable
    # print(self.MT[:5],'twisted')
    self.index = 0

  def state(self):
    return list(self.MT)

def get_seed(ith_output,i,_range):
  for x in _range:
    a = twister(x)
    if [a.extract_number() for y in range(0,i+1)][-1] == ith_output:
      return x
  return 'seed not in range'

time.sleep(50*random())
a = twister(int(time.time()))
time.sleep(50*random())
def find_when_seeded(x):
  print(get_seed(x.extract_number(),0,range(int(time.time()-2000),int(time.time()))))

# first_state = a.state()
# print(first_state[:5])
# a.twist()
# state = [retrieve_state(a.extract_number()) for _ in range(624)]
# retrieved_state = untwist(state)
# print(retrieved_state[:5])
# print(''.join(['1' if x==y else '.' for x,y in zip(first_state,retrieved_state)]))
# print(sum([1 if x==y else 0 for x,y in zip(first_state,retrieved_state)]))
# 