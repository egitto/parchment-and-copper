from math import ceil, floor

# def hex_to_bytes(a): 
#   acc = [int('0x'+a[i]+a[i+1],16) for i in range(0,len(a),2) if i+1 < len(a)]
#   if len(a)%2 == 1: acc += [int('0x'+a[-1]+'0',16)]
#   return acc

# def bytes_to_long(a):
#   acc = 0
#   for byte in a:
#     acc = acc << 8
#     acc |= byte
#   return acc

def chunk(a,chunksize):
  return [a[i*chunksize:(i+1)*chunksize] for i in range(0,ceil(len(a)/chunksize))]

def right_pad_chunk(a,chunksize):
  b = chunk(a,chunksize)
  b[-1] == b[-1]+'0'*(chunksize-len(b[-1]))
  return b

def hex_to_bin(a):
  if a == "": return ""
  pad_to = len(a)*4
  b = bin(int(a,16))[2:]
  return '0'*(pad_to-len(b))+b

def int_to_hex_with_size(size,a):
  h = hex(a)[2:]
  return '0'*(size-len(h))+h


def bin_to_b64(a):
  # print("bin:",a)
  key = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/'
  # a = '0'*(3-len(a)%3) + a
  # print(a)
  v = [int(x,2) for x in right_pad_chunk(a,6)]
  # v = [int(x,2)<<(6-len(x)) for x in chunk(a,6)]
  v = ''.join([key[x] for x in v])
  # print(v)
  return v

def pass_through_functions(functionlist, value):
  if len(functionlist) == 1:
    return functionlist[0](value)
  else:
    return pass_through_functions(functionlist[1:],functionlist[0](value))

def hex_to_b64(a):
  return pass_through_functions([hex_to_bin,bin_to_b64],a)

def b64_to_bin(a):
  if a == "": return ""
  key = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/'
  pad_to = len(a)*6
  b = [bin(key.index(val))[2:] for val in a]
  return ''.join(['0'*(6-len(x))+x for x in b])

def bin_to_hex(a):
  # print('initial value:',a)
  a = chunk(a,4)
  a[-1] += '0'*(4-len(a[-1]))
  h = ''.join([hex(int(x,2))[2:] for x in a])
  # h = hex(int(a,2))[2:]
  # print('value as bin:',''.join(a))
  # print('value as hex:',h)
  return h

def b64_to_hex(a):
  return pass_through_functions([b64_to_bin,bin_to_hex],a)

def hex_to_ascii(a):
  b = right_pad_chunk(a,2)
  return ''.join([chr(int(c,16)) for c in b])

# print(hex_to_b64(b64_to_hex("AafdsfnsdnB")))
print(b64_to_hex(hex_to_b64("49276d2")))

# print(hex_to_b64('49276d206b696c6c696e6720796f757220627261696e206c696b65206120706f69736f6e6f7573206d757368726f6f6d'))

def hex_to_long(a):
  return int(a,16)

def hexor(a,b):
  pad_to = len(a)
  c = hex_to_long(a) ^ hex_to_long(b)
  c = hex(c)[2:]
  c = '0'*(pad_to-len(c))+c
  return c

a = "1c0111001f010100061a024b53535009181" 
b = "686974207468652062756c6c27732065796" 
c = "746865206b696420646f6e277420706c617"

# print(hexor(a,b))
# print(c)

def plaintext_similarity_chi_sq(text):
  # frequencies from http://www.data-compression.com/english.html, truncated
  text = text.lower()
  plain_freq = {'a': 0.0651, 'b': 0.0124, 'c': 0.0217, 'd': 0.0349, 'e': 0.1041, 'f': 0.0197, 'g': 0.0158, 'h': 0.0492, 'i': 0.0558, 'j': 0.0009, 'k': 0.005, 'l': 0.0331, 'm': 0.0202, 'n': 0.0564, 'o': 0.0596, 'p': 0.0137, 'q': 0.0008, 'r': 0.0497, 's': 0.0515, 't': 0.0729, 'u': 0.0225, 'v': 0.0082, 'w': 0.0171, 'x': 0.0013, 'y': 0.0145, 'z': 0.0007, ' ': 0.1918, 'ascii': 0.0001}
  abc = set(plain_freq.keys())
  actual = {x: 0 for x in abc}
  score = 0
  for char in text: 
    if char in abc: 
      actual[char] += 1
    # this is a dumb hack
    else: actual['ascii'] += 1 
  sum = len(text)
  expected = {char: plain_freq[char]*sum for char in abc}
  for x in actual.keys():
    score += ((expected[x]-actual[x])**2)/expected[x]
  # print(int(score),text)
  return score

def plaintext_similarity_count_ascii(text):
  text = text.lower()
  score = len(text)+5
  non_ascii = set(list("\"abcdefghijklmnopqrstuvwxyz01234567890' "))
  score += sum([-1 for i in text if i in non_ascii])
  return score

def index_of_best_text(texts,plaintext_rating_function):
  # plaintext_similarity is function accepting text and minimized when text is plaintext.
  best_i = 0
  best_rating = 2**32
  for i in range(len(texts)):
    r = plaintext_rating_function(texts[i])
    if r < best_rating: best_i, best_rating = i, r
  return best_i

def single_char_xor(char,text):
  crypt_text = char*(len(text)//2)
  # return hex_to_b64(hexor(text,crypt_text))
  return hexor(text,crypt_text)

def decrypt_single_char_xor(text,test):
  chars = [int_to_hex_with_size(2,i) for i in range(0xFF)]
  texts = [hex_to_ascii(single_char_xor(char,text)) for char in chars]
  i = index_of_best_text(texts,test)
  return texts[i]

def test_single_char_xor(s): 
  for k in [int_to_hex_with_size(2,i) for i in range(0xFF)]:
    assert (s == single_char_xor(k,single_char_xor(k,s)))

def find_encrypted_line(texts):
  def decrypt(texts, method):
    x = [decrypt_single_char_xor(text, method) for text in texts]
    return sorted(list(zip([method(text) for text in x], x)))[0]
  print(decrypt(texts,plaintext_similarity_count_ascii))
  print(decrypt(texts,plaintext_similarity_chi_sq))
  # return([decrypt(texts,method) for method in [plaintext_similarity_count_ascii,plaintext_similarity_chi_sq]])


# print(decrypt_single_char_xor('1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736',plaintext_similarity_count_ascii))

# texts = open('cryptopals_4.txt').readlines()
# texts = [x.strip() for x in texts]
# print(find_encrypted_line(texts)) 
# you may also want to remove whitespace characters like `\n` at the end of each line

