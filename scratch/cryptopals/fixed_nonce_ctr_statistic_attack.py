from ctr import CTR_encrypt, counter_function
from bytestring_tools import data, chunk, xor
from vigenere_xor import transpose_bytes, possible_bytes
from h2b import plaintext_similarity_chi_sq as Xsq


texts = open("cryptopals_20.txt").readlines()
texts = [data(x.strip(),'b64').bytes for x in texts]
cyphertexts = [CTR_encrypt(x,b"Yellow submarine",counter_function,0) for x in texts]

def break_ragged_xor(cyphertexts):
  b = transpose_bytes(sorted(cyphertexts,key=len)[::-1])
  key = [b'\x00']*len(b)
  for i in range(len(key)):
    def score(test_key):
      return (Xsq(xor(b[i],test_key*len(b[i]))),test_key)
    key[i] = sorted(possible_bytes(),key=score)[0]
    print(i,xor(b[i],key[i]*len(b[i])))
  return b''.join(key)

key = break_ragged_xor(cyphertexts)
for x in cyphertexts:
  print(xor(x,key[:len(x)]))

# print(break_vigenere(cyphertext))