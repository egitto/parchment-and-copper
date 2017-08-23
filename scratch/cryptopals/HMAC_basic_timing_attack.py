import time
import requests
import scipy.stats as ss
import random

def timer(f):
  def wrapper(*args, **kwargs):
    a = time.time()
    f(*args, **kwargs)
    return time.time()-a
  return wrapper

def get(url):
  return requests.get(url)

def t_test(a, b):
  return ss.ttest_ind(a, b)[1]

def sample(prefix, candidates, suffix, scores):
  for x in candidates:
    scores[x] += [timer(get)(prefix+x+suffix)]

def scores_to_lists(scores):
  biggest = biggest_key(scores)
  a = []
  for l in [scores[x] for x in scores.keys() if x != biggest]: a += l
  b = scores[biggest]
  return (a,b)

def biggest_key(d):
  return sorted([(sum(d[x]),x) for x in d.keys()])[-1][1]

# duration to break = n * 40 * 20 * 16 * delay. 
# n*delay*12800. delay = 5/1000. time = 5 minutes = 600s 
# 600 s / (5/1000) / 12800 = 9.375. so, 10. okay....

# test procedure: head + test + tail. start: head = '', test = [hex(x)[-1] for x in range(16)], tail = '0*63'. run avg(timer(get), n)(url) for each value. add value with largest average time to head, shorten tail by one, repeat.

def get_HMAC(file):
  candidates = [hex(x)[-1] for x in range(16)]
  head = ''
  prefix = 'http://localhost:8080/test?file='+file+'&signature='
  while len(head) < 40:
    tail = '0'*(39-len(head))
    s = {x: [] for x in candidates}
    sample(prefix+head, candidates, tail, s)
    for x in range(1,300):
      candidates = random.sample(candidates,16) # shuffle them, just in case. 
      sample(prefix+head, candidates, tail, s)
      p = t_test(*scores_to_lists(s))
      print(x, p)
      if p < 0.0001 and x > 30:
        head += biggest_key(s)*2
        break
    head = head[:-1] # backtrack; in case we went astray somewhere
    print(head)
  return head

print(get_HMAC('message'))