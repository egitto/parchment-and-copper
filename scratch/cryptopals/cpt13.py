from ecb import *
from cbc import *
from cpt12 import *
from padPKCS7 import PaddingError, pad, unpad
from math import ceil
import random

def kv_parse(string):
  #parses a string of key-value pairs and returns a dict of them (with string keys and values)
  return {kvpair.split("=")[0]: kvpair.split("=")[1] for kvpair in string.split("&") if len(kvpair.split('='))==2}

def profile_for(string):
  data = {"email":"","uid": "10","role": "user"}
  data["email"] = string .replace('&','').replace('=','')
  return ''.join([key+'='+data[key]+'&' for key in data.keys()])[:-1]

def random_key():
  return int.to_bytes(random.getrandbits(16*8),16,'big')

key = random_key()

# making it consistent for easier debugging
def oracle(input_string):
  key = data("sdJH432480hnfidjao2hc",'b64').bytes
  return ECB_encrypt(pad(profile_for(input_string).encode(),16),key)

def parse_encrypted(cyphertext):
  key = data("sdJH432480hnfidjao2hc",'b64').bytes
  a = data(unpad(ECB_decrypt(cyphertext,key),16))
  print(a.ascii())
  return kv_parse(a.ascii())

def bytes_oracle(input_bytes):
  return oracle(data(input_bytes).ascii())

# print(oracle(profile_for("foobar@fsd.com")))
# print(profile_for("foobar@fsd.com").encode())
print(parse_encrypted(oracle("foobar@fsd.com")))
# find out what the code block containing just "com&uid=10&role=" looks like
# find out what the code block containing just "admin&uid=10&rol" looks like, maybe? hm.
# and then the block                           "email=justgarbag"
# then combine them to make "email=fobar@fsd."+"com&uid=10&role="+"admin&uid=10&rol"+"email=justgarbag"
# "email=fobar@fsd." = block 0 of oracle("fobar@fsd.com")
# "com&uid=10&role=" = block 1 of oracle("fobar@fsd.com")
# "admin&uid=10&rol" = block 1 of oracle("fobar@fsd.admin")
# "email=justgarbag" = block 0 of oracle("justgarbag")
# "\xF0"*16          = block 2 of oracle("ninechars")
# this isn't a neat solution; it'll look like {"email": "fobar@fsd.com", "uid": "10", "role": "admin", "rolemail": "justgarbag"}

acc = b''
acc += oracle("fobar@fsd.com"  )[(16*0):(16*1)]  # "email=fobar@fsd."  block 0
acc += oracle("fobar@fsd.com"  )[(16*1):(16*2)]  # "com&uid=10&role="  block 1
acc += oracle("fobar@fsd.admin")[(16*1):(16*2)]  # "admin&uid=10&rol"  block 1
acc += oracle("justgarbag"     )[(16*0):(16*1)]  # "email=justgarbag"  block 0
acc += oracle("ninechars"      )[(16*2):(16*3)]  # "\xF0"*16           block 2
print(parse_encrypted(acc))