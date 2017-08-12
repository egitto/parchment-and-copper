from ctr import CTR_encrypt, counter_function
from bytestring_tools import data, chunk, xor

texts = open("cryptopals_19.txt").readlines()
texts = [data(x.strip(),'b64').bytes for x in texts]
for text in texts: print(text)
texts = [CTR_encrypt(x,b"Yellow submarine",counter_function,0) for x in texts]

abc = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ ,!."\''

def score_guess(guess,i,reference_i):
  guess = data(guess).bytes
  plain_chars = set([x for x in abc])
  compare_with = [x for x in texts if len(x)>i]
  reference = texts[reference_i]
  return sum([data(xor(xor(x[i:i+1],guess),reference[i:i+1])).ascii() in plain_chars for x in compare_with])/len(compare_with)
  # cyphertext ^ correct_guess ^ different_cyphertext = plaintext; this estimates plaintext (badly)

def best_guesses(i,reference_i):
  guesses = sorted([(score_guess(x,i,reference_i),x) for x in abc])[::-1][:10]
  return(''.join([y for x,y in guesses if x > 0.9]))

def table_of_guesses(reference_i,start=0):
  for i in range(start,len(texts[reference_i])):
    print(best_guesses(i,reference_i))

def key_if(guess,i,reference_i):
  return (data(guess) ^ data((texts[reference_i][i:]))).bytes[i:len(guess)+i]

def decode_with_keydict(keydict):
  key = b''
  for i in sorted(keydict.keys()):
    while len(key) < i:
      key += b'\x00'
    key += keydict[i]
  print(xor(key,data(texts[0]).bytes))

def decode_with_key(i,key):
  print(xor(key,data(texts[i]).bytes)[:len(texts[i])])

key = key_if(b'I have passed with a nod of the head',0,4)
for i in range(40):
  print(i)
  decode_with_key(i,key)
    
decode_with_key(2,key)
table_of_guesses(2,len(key))
print(key)