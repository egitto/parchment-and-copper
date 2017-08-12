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
    u, d = 11, 4294967295
    s, b = 7, 2636928640
    t, c = 15, 4022730752
    if self.index >= n:
      if self.index > n: raise SeedError("Generator never seeded")
      self.twist()
    y = self.MT[self.index]
    y ^= ((y>>u)&d)
    y ^= ((y<<s)&b)
    y ^= ((y<<t)&c)
    y ^= (y>>l)
    self.index += 1
    return y&((1<<w)-1)

  def twist(self):
    n, m, r, = 624, 397, 31
    a = 657275805462
    upper_mask = (1<<r)
    lower_mask = upper_mask-1
    for i in range(n):
      x = (self.MT[i]&upper_mask)+((self.MT[(i+1)%n])&lower_mask)
      xA = x>>1
      if x%2: xA^=a
      self.MT[i] = self.MT[(i+m)%n]^xA
    self.index = 0

a = twister(0)
# print(a.extract_number()/(1<<32))
# print(a.extract_number()/(1<<32))
# print(a.extract_number()/(1<<32))
# print(a.extract_number()/(1<<32))
# print(a.extract_number()/(1<<32))