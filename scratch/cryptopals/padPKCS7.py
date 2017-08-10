from math import ceil

class PaddingError(Exception):
  pass

def pad(text,blocksize):
  length = ceil((len(text)+1)/blocksize)*blocksize
  pad = length - len(text)
  pad = int.to_bytes(pad,1,'big')*pad
  return text + pad

def unpad(text,blocksize):
  pad = int.from_bytes(text[-1],'big')
  if text[-1]*pad == text[-pad:]:
    return text[:pad]
  else:
    raise PaddingError