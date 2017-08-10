from cpt7 import *
from cpt10 import *
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
  a = data(ECB_decrypt(cyphertext,key)).ascii()
  print(a)
  return kv_parse(a)

def bytes_oracle(input_bytes):
  return oracle(data(input_bytes).ascii())

print(oracle(profile_for("foobar@fsd.com")))
print(profile_for("foobar@fsd.com").encode())
print(parse_encrypted(oracle("foobar@fsd.com")))
# find out what the code block containing just "com&uid=10&role=" looks like
# find out what the code block containing just "admin&uid=10&rol" looks like, maybe? hm.
# email=foobar@fsd.com&uid=10&role=user