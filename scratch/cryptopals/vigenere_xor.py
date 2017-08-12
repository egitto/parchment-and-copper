from bytestring_tools import *
from math import ceil
from h2b import plaintext_similarity_chi_sq as Xsq
from h2b import plaintext_similarity_count_ascii as Xascii


text = open('cryptopals_6.txt').readlines()
text = ''.join([x.strip() for x in text])
cyphertext = data(text,'b64')
# print(cyphertext.bytes[0:1],'first character in bytes')
# print(cyphertext.bin()[0:8],'first character in bin')
# print(cyphertext.ascii()[0],'first character in ascii')
# print(cyphertext.hex()[0:2],'first character in hex')

def transpose(array):
  """has to work on partially ragged "array" (list of strings)
  transpose(['This',' is ','just',' fin','e.']) -> ['T j e','hiuf.','issi','s tn']
  """
  a = ['']*len(array[0])
  for x in range(len(a)): #current character index, to be chunk
    for y in range(len(array)): # chunk indexes, to be character
      if len(array[y]) > x:
        a[x] += array[y][x]
  return a

def transpose_bytes(array):
  """has to work on partially ragged "array" (list of strings)
  transpose(['This',' is ','just',' fin','e.']) -> ['T j e','hiuf.','issi','s tn']
  """
  a = [b'']*len(array[0])
  for x in range(len(a)): #current character index, to be chunk
    for y in range(len(array)): # chunk indexes, to be character
      if len(array[y]) > x:
        a[x] += bytes([array[y][x]])
  return a

# transpose(['This',' is ','just',' fin','e.'])

def hamming_distance(a,b):
  a = data(a)
  b = data(b)
  return (a ^ b).bin().count('1')

# print(hamming_distance("this is a test","wokka wokka!!!"))

def find_keysize(text,sample_num,max_keysize):
  keysizes = list(range(2,max_keysize))
  distances = [0]*len(keysizes)
  b = text.bytes
  for i in range(len(keysizes)):
    keysize = keysizes[i]
    chunked = chunk(b,keysize)
    for j in range(sample_num):
      try: distances[i] += hamming_distance(chunked[j],chunked[j+1])
      except(IndexError): assert False, "sample number too high"
    distances[i] /= keysize
    distances[i] /= sample_num
    distances[i] = round(distances[i],3)
  d = sorted(list(zip(distances,keysizes)))  
  return d

def possible_bytes():
  return [bytes([x]) for x in range(256)]

# find_keysize(cyphertext)

keysizes = list(range(2,40))

def X(text):
  return Xascii(text) * Xsq(text)

def break_vigenere_given_keysize(cyphertext,keysize):
  key = [b'\x00']*keysize
  b = transpose_bytes(chunk(cyphertext.bytes,keysize))
  for i in range(len(key)):
    best_score = 2**32
    scores = [(Xsq(xor(b[i],test_key*len(b[i]))),test_key) for test_key in possible_bytes()]
    key[i] = sorted(scores)[0][1]
  return data(b''.join(key))

# key = data("9z8s")
# stuff = data('This is a test, it will be encrypted and it should look good')
# encrypted_stuff = key.xor_repeating(stuff)
# print(break_vigenere_given_keysize(encrypted_stuff,4))

def break_vigenere(cyphertext,keysize=0):
  if not keysize:
    keysizes = find_keysize(cyphertext,40,60)[:1]
    keysizes = [size for score, size in keysizes]
  else:
    keysizes = [keysize]
  print("checking keys with lengths: ",keysizes)
  keys = [break_vigenere_given_keysize(cyphertext,keysize) for keysize in keysizes]
  best_text = ''
  best_key = ''
  best_score = 2**320
  for key in keys:
    text = key.xor_repeating(cyphertext).bytes
    if X(text) < best_score:
      best_score = X(text)
      best_text = text
      best_key = key.bytes
  print(best_text)
  print('key:',best_key)
  return [best_key,best_text]

# for size in range(1,90):
#   print(find_keysize(cyphertext,size)[:5])
# # print(cyphertext.b64())


# decrypted = break_vigenere(cyphertext)
# print(decrypted)



# print(data(decrypted[0]).xor_repeating(cyphertext).bin()[:16],'decrypted')
# print(data(decrypted[0]).bin()[:16],'key')
# print(cyphertext.bin()[:16],'cyphertext')
# print(cyphertext.hex()[:4])
# print(cyphertext.b64()[:3])

# a = cyphertext
# print(bytes(cyphertext.ascii()[0],'ascii'),'first character of cyphertext, to ascii, then to bytes')
# print(a.hex()[:4],'cyphertext first 3 hex')

# a = '///='
# b = data(a,'b64')
# c = 'a'
# d = data(c)
# print(b.bin())
# print(b.hex())
# e = d.xor_repeating(b)
# print(e.bin(),'after xor')
# print(d.bin(),'key')
# print(b.bin(),'text')