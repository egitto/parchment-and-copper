import sha1_from_external_source as sha1
import struct
from bytestring_tools import chunk, data, random_bytes

def produce_MAC(message,key=b'keep me hidden'):
  return sha1.sha1(key+message)

def verify_message(message,hash_cert,key=b'keep me hidden'):
  return hash_cert == sha1.sha1(key+message)

def test_MAC_system():
  message = b'look, up in the sky, a flying goat, with trousers of titanium and abs of teak!'
  MAC = produce_MAC(message)
  print(verify_message(message,MAC),'test_MAC_system()')                            
  print(not verify_message(message+b' haha disregard that',MAC),'test_MAC_system()')


def sha1_padding(message):
  # this is just taken out of sha1_from_external_source, slightly modified
  # provides ONLY the padding, not the entire last block
  message_byte_length = len(message)
  tail = b''
  # print(tail)
  tail += b'\x80'
  tail += b'\x00' * ((56 - (message_byte_length + 1) % 64) % 64)
  message_bit_length = message_byte_length * 8
  tail += struct.pack(b'>Q', message_bit_length)
  return tail

def resume_sha1(more_data,current_sha1,l_orig):
  l_adj = l_orig + len(sha1_padding(b'a'*l_orig))
  magic = [int(x,16) for x in chunk(str(current_sha1),8)]
  return sha1.sha1(more_data,magic_override=magic,fake_bytes=l_adj)

def test_resume_sha1():
  a = sha1.sha1(b'a')
  b = sha1.sha1(b'a'+sha1_padding(b'a')+b'a')
  c = resume_sha1(b'a',a,1)
  print(b==c,'test_resume_sha1()')

def forcibly_append_admin(original_message,MAC):
  prefix_lengths = [x for x in range(0,512)]
  x = b';role=admin;'
  for l in prefix_lengths:
    pad = sha1_padding(b'a'*l+original_message)
    test_MAC = resume_sha1(x,MAC,l+len(original_message))
    if verify_message(original_message+pad+x,test_MAC): return True
  return False

def test_break():
  message = b'look, up in the sky, a flying goat, with trousers of titanium and abs of teak!'
  MAC = produce_MAC(message)
  print(forcibly_append_admin(message,MAC),'test_break()')

def test():
  print('Testing sha1...')
  test_MAC_system()
  test_resume_sha1()
  test_break()
