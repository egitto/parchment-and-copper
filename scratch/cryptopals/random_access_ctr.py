# Break "random access read/write" AES CTR

# Back to CTR. Encrypt the recovered plaintext from this file (the ECB exercise) under CTR with a random key (for this exercise the key should be unknown to you, but hold on to it).

# Now, write the code that allows you to "seek" into the ciphertext, decrypt, and re-encrypt with different plaintext. Expose this as a function, like, "edit(ciphertext, key, offset, newtext)".

# Imagine the "edit" function was exposed to attackers by means of an API call that didn't reveal the key or the original plaintext; the attacker has the ciphertext and controls the offset and "new text".

# Recover the original plaintext.
# Food for thought.

# A folkloric supposed benefit of CTR mode is the ability to easily "seek forward" into the ciphertext; to access byte N of the ciphertext, all you need to be able to do is generate byte N of the keystream. Imagine if you'd relied on that advice to, say, encrypt a disk.
from bytestring_tools import *
from ctr import *
from ecb import b64_file_to_bytes, ECB_decrypt

key = random_bytes(16)
cypher = CTR_cypher(key)
cyphertext = cypher.encrypt(ECB_decrypt(b64_file_to_bytes('cryptopals_25.txt'),b"YELLOW SUBMARINE"))

def edit(cyphertext, key, offset, newtext):
  l = len(newtext)
  cypher = CTR_cypher(key)
  cypher.set_offset(offset)
  a = cypher.encrypt(newtext)
  return cyphertext[:offset]+a+cyphertext[offset+l:]

def edit_api(cyphertext,offset,newtext):
  return edit(cyphertext,key,offset,newtext)

def recover_plaintext(cyphertext,edit_api):
  # leet hacker skillz
  return edit_api(cyphertext,0,cyphertext)

print(recover_plaintext(cyphertext,edit_api))