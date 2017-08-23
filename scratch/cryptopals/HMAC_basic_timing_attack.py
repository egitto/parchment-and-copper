import time
import requests
import numpy

def timer(f):
  def wrapper(*args, **kwargs):
    a = time.time()
    f(*args, **kwargs)
    return time.time() - a
  return wrapper

def avg(f,n):
  def wrapper(*args, **kwargs): return sum([f(*args, **kwargs) for _ in range(n)])/n
  return wrapper

def get(url):
  return requests.get(url)

time_get = avg(timer(get),1)

# test procedure: head + test + tail. start: head = '', test = [hex(x)[-1] for x in range(16)], tail = '0*63'. run avg(timer(get),n)(url) for each value. add value with largest average time to head, shorten tail by one, repeat.

def get_HMAC(file):
  candidates = [hex(x)[-1] for x in range(16)]
  head = ''
  tail = '0'*39
  prefix = 'http://localhost:8080/test?file='
  try:
    while len(head) < 40:
      s = sorted([(time_get(prefix+file+'&signature='+head+x+tail),x) for x in candidates])
      print(s)
      head += s[-1][1]
      tail = tail[1:]
  except(HMAC_found): return head
  return False

print(get_HMAC('message'))