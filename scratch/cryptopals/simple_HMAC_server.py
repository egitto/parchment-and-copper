from bottle import route, run, template, HTTPResponse
from bytestring_tools import random_bytes, data
from sha1_from_external_source import sha1 as sha1

@route('/<request>')
def process_request(request):
    r = request[request.index('?')+1:]
    r = r.split('&').split('=')
    r = {r[i][0]: r[i][1] for i in range(len(r)) if len(r[i]) == 2}
    valid = insecure_compare(HMAC(key,r.get('file','')),r.get('signature',''))
    if valid: raise HTTPResponse(status=200)
    else: raise HTTPResponse(status=500)

def HMAC(K,m):
  Kp = K
  if len(K) < 64: Kp = data(b'\x00'*(64-len(K))+K)
  elif len(K) > 64: Kp = data(sha1(K),'hex')
  opad = data(b'\x5c'*64) ^ Kp
  ipad = data(b'\x36'*64) ^ Kp
  return sha1(opad.bytes+data(sha1(ipad.bytes+m)).bytes)

def insecure_compare(s1,s2):
  if len(s1) != len(s2): return False
  for i in range(len(s1)):
    if s1[i] != s2[i]: return False
    time.sleep(0.05)
  return True

key = random_bytes(64)
run(host='localhost', port=8080, debug=True)