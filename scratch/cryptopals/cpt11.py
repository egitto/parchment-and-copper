from cpt10 import *
import random

def random_key():
  return int.to_bytes(random.getrandbits(16*8),16,'big')

def pkcs7_pad(by,length):
  pad = length - len(by)
  pad = int.to_bytes(pad,1,'big')*pad
  return by + pad

def padtext(input_bytes):
  leftpad = random_key()[0:random.randint(6,11)]
  rightpad = random_key()[0:random.randint(6,11)]
  a = leftpad + input_bytes + rightpad
  return pkcs7_pad(a,16*(len(a)//16 + 1))

def blackbox(input_bytes):
  plaintext = padtext(input_bytes)
  if random.randint(0,1):
    return ECB_encrypt(plaintext,random_key())
  else:
    return CBC_encrypt(plaintext,random_key(),iv=random_key())

def encryption_oracle(blackbox):
  def chunk(a,chunksize):
    return [a[i*chunksize:(i+1)*chunksize] for i in range(0,ceil(len(a)/chunksize))]

  def group_repetitions(text,size):
    chunks = chunk(text,size)
    acc = {x:0 for x in chunks}
    for x in chunks: acc[x] += 1
    c = [(acc[x],x) for x in acc if acc[x] > 1]
    return sorted(c)[::-1]

  def repetition_score(string,size):
    return sum([val for val, text in group_repetitions(string,size)])

  query = b'\x00'*512
  score = repetition_score(blackbox(query),16) 
  print(score)
  if score > 5: return 'EBC'
  else: return 'CBC'

# for i in range(30): encryption_oracle(blackbox)