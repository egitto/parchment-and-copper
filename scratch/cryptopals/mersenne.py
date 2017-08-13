from bytestring_tools import data, xor

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
    print(y,'actual state')
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
      self.MT[i] = self.MT[(i+m)%n]^xA
    self.index = 0


def undo_xor_lshift_mask(val,shift,mask):
  x = val
  print('starting undo')
  i = 1
  while mask != 0:
    # print(x,'   val')
    # pp(mask, 'mask')
    # print((x<<(shift*i))&mask,'   val&mask')
    x = x^((x<<(shift*i))&mask)
    mask = (mask<<shift)&mask
    i *= 2 # I don't really understand _why_ this works # that's because it doesn't
  return x

def pp(x,s=''):
  x = bin(x)[2:]
  print( '0'*(32-len(x))+x,s)

def bitmask(i,f):
  f = min(32,f)
  return 0xFFFFFFFF >> (32-f+i) << (32-f)

print(bitmask(1,36))

def undo_xor_lshift_mask(y,shift,mask=0xAAAAAAAA):
  views = [bitmask(i,i+shift) for i in range(0,32,shift)][::-1]
  acc = 0
  for view in views:
    pp(acc)
    acc |= ((acc << shift)&mask ^ y)&view
  return acc

def undo_xor_rshift_mask(y,shift,mask=0xAAAAAAAA):
  views = [bitmask(i,i+shift) for i in range(0,32,shift)]
  acc = 0
  for view in views:
    pp(acc)
    acc |= ((acc >> shift)&mask ^ y)&view
  return acc 

# [twister(i).extract_number() for i in range(40)]

def retrieve_state(y):
  u, d = 11, 0xFFFFFFFF
  s, b = 7, 0x9D2C5680
  t, c = 15, 0xEFC60000
  y = (y^(y<<18))>>18
  y ^= (y<<15)&c # this step is the same forwards as backwards
  y = undo_xor_lshift_mask(y,7,b) # this step _isn't
  y = undo_xor_rshift_mask(y,11,d) # this step _isn't
  return(y)

print(retrieve_state(twister(0).extract_number()))
