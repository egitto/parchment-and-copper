from mersenne import *

def untwist(state):
  n, m, r, = 624, 397, 31
  a = 0x9908B0DF                    # notice that the first bit of a is 1
  upper_mask = (1<<r)               # 0x80000000
  lower_mask = upper_mask-1         # 0x7FFFFFFF
  MT = list(state)
  def retrieve_x(i):                # this code is a lot easier to understand when it's next to the forward version
    xA = MT[i]^MT[(i+m)%n]          # undoing: self.MT[i] = self.MT[(i+m)%n]^xA 
    was_xored = xA&0x80000000 != 0  # did 'if x%2: xA^=a' happen? first bit of xA was originally 0 ('xA = x>>1')
    if was_xored: xA ^=a            # if so, undo it
    x = (xA<<1)+was_xored           # if was_xored, then x%2==1
    return x                        # x = (MT[i]&uppermask)+(MT[(i+1)%n]&lowermask)
  for i in range(n-1,0,-1):         # has to be done in reverse, of course
    MT[i] = (retrieve_x(i)&upper_mask) + (retrieve_x((i-1)%n)&lower_mask)
  return MT

def pp(x,s=''):
  x = bin(x)[2:]
  print( '0'*(32-len(x))+x,s)

def bitmask(i,f):
  f = min(32,f)
  return 0xFFFFFFFF >> (32-f+i) << (32-f)

def undo_xor_lshift_mask(y,shift,mask=0xAAAAAAAA):
  views = [bitmask(i,i+shift) for i in range(0,32,shift)][::-1]
  acc = 0
  for view in views:
    acc |= ((acc << shift)&mask ^ y)&view
  return acc

def undo_xor_rshift_mask(y,shift,mask=0xAAAAAAAA):
  views = [bitmask(i,i+shift) for i in range(0,32,shift)]
  acc = 0
  for view in views:
    acc |= ((acc >> shift)&mask ^ y)&view
  return acc 

def retrieve_state(y):
  u, d = 11, 0xFFFFFFFF
  s, b = 7, 0x9D2C5680
  t, c = 15, 0xEFC60000
  y = (y^(y<<18))>>18
  y = undo_xor_lshift_mask(y,15,c)
  y = undo_xor_lshift_mask(y,7,b)
  y = undo_xor_rshift_mask(y,11,d) 
  return(y)

def mersenne_with_known_values(state):
  return twister(0).set_state(state)

def clone_mersenne(output_list):
  """Output_list ideally has len(625) or more"""
  n = 624
  def verify_clone(a,future):
    print(future)
    return all([x == a.extract_number() for x in future])
  state = [retrieve_state(x) for x in output_list[:n]]
  a = mersenne_with_known_values(state)
  if verify_clone(a,output_list[n:]): return a
  print('cloning failed')

a = twister(100)
a.extract_numbers(50)
v = a.extract_numbers(624)
b = clone_mersenne(v)
print(a.extract_numbers(6000) == b.extract_numbers(6000))
print(a.index,b.index)