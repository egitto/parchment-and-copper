from bytestring_tools import *

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

def find_ecb_encrypted(data_array):
  return [text.hex() for text in texts if repetition_score(text.bytes,16)>0]

texts = open("cryptopals_8.txt").readlines()
texts = [data(x.strip(),'hex') for x in texts]
print(find_ecb_encrypted(texts))