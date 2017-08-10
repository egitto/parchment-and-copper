from math import ceil

class PaddingError(Exception):
  pass

def pad(text,blocksize):
  length = ceil((len(text)+1)/blocksize)*blocksize
  pad = length - len(text)
  pad = int.to_bytes(pad,1,'big')*pad
  return text + pad

def unpad(text,blocksize):
  pad = text[-1]
  # print(int.to_bytes(text[-1],1,'big')*pad,text[-pad:])
  if int.to_bytes(text[-1],1,'big')*pad == text[-pad:]:
    return text[:-pad]
  else:
    raise PaddingError

# print(unpad(pad(b'',4),4))
# print(unpad(pad(b'a',4),4))
# print(unpad(pad(b'as',4),4))
# print(unpad(pad(b'asd',4),4))
# print(unpad(pad(b'asdf',4),4))