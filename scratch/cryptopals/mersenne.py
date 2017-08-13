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
    y ^= (y>>11)&d #is the masking necessary at all?
    print(bin(y))
    aa = y
    y ^= (y<<7)&b
    print(bin(y))
    bb = y
    bb = (bb^((bb<<7)&b))
    bb = (bb^((bb<<7)&(b&(b<<7))))
    # bb = (bb^((bb<<7)&(b&(b<<14)&(b<<7))))
    bb = undo_xor_lshift_mask(y,7,b)
    print(bin(bb),aa==bb,bin(aa^bb))
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
    i *= 2 # I don't really understand _why_ this works
  return x

def pp(x,s=''):
  x = bin(x)[2:]
  print( '0'*(32-len(x))+x,s)


# [twister(i).extract_number() for i in range(40)]


def retrieve_state(y):
  u, d = 11, 0xFFFFFFFF
  s, b = 7, 0x9D2C5680
  t, c = 15, 0xEFC60000
  y = (y^(y<<18))>>18
  y ^= (y<<15)&c # this step is the same forwards as backwards
  y = undo_xor_lshift_mask(y,7,b) # this step _isn't
  y = undo_xor_lshift_mask(y,7,b) # this step _isn't
  y ^= (y>>11)&d
  return(y)
