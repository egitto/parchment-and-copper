from bottle import route, run, template, HTTPResponse, request
from bytestring_tools import random_bytes, data
from sha1_from_external_source import sha1 as sha1
import time

@route('/test')
def process_request():
  file = request.query.file
  signature = request.query.signature
  valid = insecure_compare(HMAC(key,file),signature)
  if valid: raise HTTPResponse(status=200)
  else: raise HTTPResponse(status=500)

def HMAC(K,m):
  Kp = data(K)  
  m = data(m).bytes
  if len(K) < 64: Kp = data(b'\x00'*(64-len(K))+K)
  elif len(K) > 64: Kp = data(sha1(K),'hex')
  opad = data(b'\x5c'*64) ^ Kp
  ipad = data(b'\x36'*64) ^ Kp
  return sha1(opad.bytes+data(sha1(ipad.bytes+m)).bytes)

def insecure_compare(s1,s2):
  if len(s1) != len(s2): return False
  for i in range(len(s1)):
    time.sleep(0.001)
    if s1[i] != s2[i]: return False
  return True

key = b"this is the test key"
print(HMAC(key,b'message'))
run(host='localhost', port=8080, debug=True)