# from h2b import *
from math import ceil
import base64
import random

def chunk(a,chunksize):
  return [a[i*chunksize:(i+1)*chunksize] for i in range(0,ceil(len(a)/chunksize))]

def right_pad_chunk(a,chunksize):
  b = chunk(a,chunksize)
  b[-1] == b[-1]+'0'*(chunksize-len(b[-1]))
  return b

class data():
  def __init__(self,contents,data_type=''):
    """data(contents,data_type)
    contents is a string
    data-type is in ['hex','bin','b64',''] and describes format of string; 
    data-type of '' means bytes or utf-8 string
    """
    sizes = {'hex':4,'bin':1,'':8,'b64':6}
    self.length = sizes[data_type]*len(contents)
    if data_type == '':
      if type(contents) == str:
        self.bytes = bytes(contents,"UTF-8")
        # self.value = int.from_bytes(self.bytes,'big')
      elif type(contents) == bytes:
        # self.value = int.from_bytes(contents,'big')
        self.bytes = contents
      else: assert False, 'data_type of \'\' requires bytes or str as contents, not '+type(contents)
    else:
      if data_type == 'b64':
        if self.length <= 0: print(contents,'<- length error converting')
        self.bytes = self.b64_to_long(contents).to_bytes(ceil(self.length/8),'big')
        self.length -= contents.count('=')*8
        self.bytes = self.bytes[:ceil(self.length/8)]
        # self.bytes = base64.standard_b64decode(contents)
        # self.value = self.b64_to_long(contents)
        # self.value = int.from_bytes(self.bytes,'big')
      else:
        if len(contents)>2:
          if contents[0:2] in ['0x','0b']:
            contents = contents[2:]
            self.length -= 2
        if data_type == 'hex':
          # self.value = int(contents,16)
          self.bytes = bytes.fromhex(contents)
        elif data_type == 'bin':
          # self.value = int(contents,2)
          self.bytes = int(contents,2).to_bytes(ceil(self.length/8),'big')

  def b64_to_long(self,b64):
    key = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/'
    # a = [key.index(x) for x in b64]
    key = {item: i for i,item in enumerate(key)}
    key['=']=0
    a = [key[x] for x in b64]
    acc = 0
    for x in a:
      acc = acc << 6
      acc += x
    return acc

  def ascii_to_long(self,ascii):
    a = [ord(x) for x in ascii]
    acc = 0
    for x in a:
      acc = acc << 8
      acc += x
    return acc

  def hex(self):
    """returns value as hex string
    """
    # a = hex(self.value)[2:]
    # return '0'*(self.length//4-len(a)) + a
    return self.bytes.hex()

  def int(self):
    return int.from_bytes(self.bytes,'big')

  def bin(self):
    """returns value as binary
    """
    a = bin(int.from_bytes(self.bytes,'big'))[2:]
    return '0'*(self.length-len(a)) + a

  def ascii(self):
    """returns value as ascii
    # """
    a = self.bin()
    a = right_pad_chunk(a,8)
    return ''.join([chr(int(x,2)) for x in a])
    # return str(self.bytes,'utf-8') # this one doesn't work, oddly.

  def b64(self):
    """returns value as b64
    """
    return base64.standard_b64encode(self.bytes)

  def __xor__(self,value):
    ldiff = self.length - value.length
    v1 = int.from_bytes(self.bytes,'big')
    v2 = int.from_bytes(value.bytes,'big')
    bytelength = max(len(self.bytes),len(value.bytes))
    if ldiff > 0:
      d = data(int.to_bytes(v1 ^ (v2 << ldiff),bytelength,'big'))
    else:
      d = data(int.to_bytes((v1 << -ldiff) ^ v2,bytelength,'big'))
      # d = data(bin(,'bin')
    d.length = max(self.length,value.length)
    return(d)

  def xor_repeating(self,other):
    """usage: key.xor_repeating(text)
    ex: data('p5Cdk3?').xor_repeating('Some plaintext')
    returns a data object.
    """
    if self.length <= 0: print(self.hex())
    d = (self.bin()*(other.length//self.length +1))[:other.length]
    d = data(d,'bin')
    return d ^ other

  def __lshift__(self,left):
    return data(self.bin()+'0'*left,'bin')

  def __rshift__(self,right):
    return data(self.bin()[:-right],'bin')

def xor(a,b):
  return (data(a)^data(b)).bytes

def random_bytes(n=16):
  return int.to_bytes(random.getrandbits(n*8),n,'big')

def repeating_xor_crypt(text,key):
  key = data(key)
  # print(key.bin())
  text = data(text)
  # print(text.bin())
  return key.xor_repeating(text).hex()

# print(repeating_xor_crypt(text,'ICE'))
def test_b64():
  a = "TWFyeSBoYWQgYSBsaXR0bGUgbGFtYi4uLiBASktMTU5PUFpbXF1eX2BhamtsbW5ven1+"
  b = b"Mary had a little lamb... @JKLMNOPZ[\]^_`ajklmnoz}~"
  print(data(a,'b64').ascii())
  print(b)

def test_r_xor():
  text = "Burning 'em, if you ain't quick and nimble\nI go crazy when I hear a cymbal"
  key = "ICE"
  target = "0b3637272a2b2e63622c2e69692a23693a2a3c6324202d623d63343c2a2622632"+"4272765272a282b2f20430a652e2c652a31243"+"33a653e2b2027630c692b20283165286326302e27282f"
  print(data(key).xor_repeating(data(text)).hex() == target)

def test_ascii():
  a = "TWFyeSBoYWQgYSBsaXR0bGUgbGFtYi4uLiBASktMTU5PUFpbXF1eX2BhamtsbW5ven1+"
  b = "Mary had a little lamb... @JKLMNOPZ[\]^_`ajklmnoz}~"
  print(data(data(a,'b64').ascii()).b64())
  print(a)

def test_bin():
  for i in range(255):
    b = bin(i)
    print(data(b,'bin').bytes)

# test_b64()
# test_ascii()
# test_r_xor()
# test_bin()
