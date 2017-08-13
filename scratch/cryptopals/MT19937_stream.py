from mersenne import *
from bytestring_tools import data, xor
from math import ceil

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


