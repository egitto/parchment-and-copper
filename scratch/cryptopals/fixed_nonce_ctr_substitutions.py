from ctr import CTR_encrypt #yes, not the cypher
from bytestring_utils import data, chunk



texts = open("cryptopals_19.txt").readlines()
texts = [data(x.strip(),'b64') for x in texts]
texts = [CTR_encrypt(x,b"Yellow submarine",)]