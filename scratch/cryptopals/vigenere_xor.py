from bytestring_tools import *
from math import ceil
from h2b import plaintext_similarity_chi_sq as Xsq
from h2b import plaintext_similarity_count_ascii as Xascii


text = open('cryptopals_6.txt').readlines()
text = ''.join([x.strip() for x in text])
cyphertext = data(text,'b64')
print(cyphertext.ascii()[0:2],'first character')

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

# transpose(['This',' is ','just',' fin','e.'])

def hamming_distance(a,b):
  a = data(a)
  b = data(b)
  return (a ^ b).bin().count('1')

# print(hamming_distance("this is a test","wokka wokka!!!"))

def find_keysize(text,sample_num):
  keysizes = list(range(2,41))
  distances = [0]*len(keysizes)
  b = text.ascii()
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
  return [data(chr(x)) for x in range(256)]

# find_keysize(cyphertext)

keysizes = list(range(2,40))

def X(text):
  return Xascii(text) * Xsq(text)

def break_vigenere_given_keysize(cyphertext,keysize):
  key = [0]*keysize
  b = transpose(chunk(cyphertext.ascii(),keysize))
  # print(b)
  for i in range(len(key)):
    best_score = 2**32
    best_line = ''
    for test_key in possible_bytes():
      current_line = test_key.xor_repeating(data(b[i])).ascii()
      current_score = Xsq(current_line)
      # print(current_line)
      if current_score < best_score:
        best_line = current_line
        key[i] = test_key.hex()
        best_score = current_score
    # print(bestdf_line)
  # print(key)
  key = data(''.join(key),'hex')
  # print(key.xor_repeating(cyphertext).ascii())
  return key

# key = data("9z8s")
# stuff = data('This is a test, it will be encrypted and it should look good')
# encrypted_stuff = key.xor_repeating(stuff)
# print(break_vigenere_given_keysize(encrypted_stuff,4))

def break_vigenere(cyphertext):
  keysizes = find_keysize(cyphertext,40)[:1]
  # keysizes = [[0,29]]
  keysizes = [size for score, size in keysizes]
  print("cheching keys with lengths: ",keysizes)
  keys = [break_vigenere_given_keysize(cyphertext,keysize) for keysize in keysizes]
  best_text = ''
  best_key = ''
  best_score = 2**32
  for key in keys:
    text = key.xor_repeating(cyphertext).ascii()
    if X(text) < best_score:
      best_score = X(text)
      best_text = text
      best_key = key.ascii()
  print(best_text)
  print('key:',best_key)
  return [best_key,best_text]

# for size in range(1,90):
#   print(find_keysize(cyphertext,size)[:5])
# # print(cyphertext.b64())
decrypted = break_vigenere(cyphertext)
print(decrypted)
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