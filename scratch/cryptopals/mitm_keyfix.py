# Implement a MITM key-fixing attack on Diffie-Hellman with parameter injection

# Use the code you just worked out to build a protocol and an "echo" bot. You don't actually have to do the network part of this if you don't want; just simulate that. The protocol is:

# A->B
#     Send "p", "g", "A"
# B->A
#     Send "B"
# A->B
#     Send AES-CBC(SHA1(s)[0:16], iv=random(16), msg) + iv
# B->A
#     Send AES-CBC(SHA1(s)[0:16], iv=random(16), A's msg) + iv 
from bytestring_tools import random_bytes, data
class Alice():
  def __init__(self,private_hex):
    self.a = int.from_bytes(random_bytes(16),'big')
    self.p = int.from_bytes(random_bytes(16),'big')
    self.g = 2
    