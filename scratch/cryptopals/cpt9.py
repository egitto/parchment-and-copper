def pkcs7_pad(by,length):
  pad = length - len(by)
  pad = int.to_bytes(pad,1,'big')*pad
  return by + pad