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

def oracle_wrapper_for_decrypt_all(input_bytes):
  return oracle(data(b'justgarbag'+input_bytes).ascii())[16:]

# this doesn't work; eating '=' and '&' breaks it
# print(decrypt_all(oracle_wrapper_for_decrypt_all))

# print(parse_encrypted(oracle("foobar@fsd.com")))
# blocks to use: "email=fobar@fsd." + "com&uid=10&role=" + ("admin"+padding)
# {"email": "fobar@fsd.com", "uid": "10", "role": "admin"}

# "Using only the user input to profile_for() (as an oracle to generate "valid" ciphertexts) and the ciphertexts themselves, make a role=admin profile. " maybe this is cheating?
# additional knowledge needed for this attack:
# 1) type of padding used
# 2) knowledge of the contents of the rest of the encrypted string
# but I don't see a way to do it without this info.

def get_admin_access():
  acc = b''
  acc += oracle("fobar@fsd.com"             )[(16*0):(16*1)]  # "email=fobar@fsd."  block 0
  acc += oracle("fobar@fsd.com"             )[(16*1):(16*2)]  # "com&uid=10&role="  block 1
  acc += oracle("fobar@fsd.admin"+chr(11)*11)[(16*1):(16*2)]  # "admin"+padding     block 1
  print(parse_encrypted(acc))
  return acc 

get_admin_access()