import random

class xory(str):
  def __lshift__(self, shift):
    s = self.split(' ')[shift:]+['0']*shift
    return xory(' '.join(s))
  def __xor__(self,val):
    s1 = xory.to_array_xory(self)
    s2 = xory.to_array_xory(val)
    return self.simplify_xor(' '.join(['^'.join(x+y) for x,y in zip(s1,s2)]))
  def to_array_xory(self):
    return [x.split('^') for x in self.split(' ') if x!=' ']

  def simplify_xor(self,string):
    s1 = xory.to_array_xory(string)
    s1 = [[x for x in items if items.count(x)%2==1 and not (len(items)==1 or x=='0' or x =='')] for items in s1]
    return xory(' '.join(['^'.join(x) for x in s1]))

  def __and__(self,integer):
    s = self.split(' ')
    b = '0'*(len(s)-len(bin(integer))+2)+bin(integer)[2:]
    return xory(' '.join([(x if y == '1' else '0') for x,y in zip(s,b)]))

def pp(x,s=''):
  x = bin(x)[2:]
  print(' '.join([y for y in '0'*(32-len(x))+x]),s)

def undo_xor_lshift_mask(val,shift,mask):
  x = val
  print('starting undo')
  i = 1
  while mask != 0:
    print(x,'   val')
    pp(mask, 'mask')
    print((x<<(shift*i))&mask,'   val&mask')
    x = x^((x<<(shift*i))&mask)
    mask = (mask<<shift)&mask
    i *= 2
  return x

b = int(random.random()*2**32)
shift = 7
y = xory('a b c d e f g h i j k l m n o p q r s t u v w x y z 1 2 3 4 5 6')
print(type(y<<shift))
print(type(((y<<shift)&b)))
print(y)
y = (y^((y<<shift)&b))
print(y)
y = undo_xor_lshift_mask(y,shift,b)
print(y,'           after first decode')
print(xory('a b c d e') << 2)

# print(string_xor(,'b c d e f g h i j k l m n o p q r s t u v w x y z 1 2 3 4 5 6 7'))