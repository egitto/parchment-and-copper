from bytestring_tools import data
p = int('ffffffffffffffffc90fdaa22168c234c4c6628b80dc1cd129024e088a67cc74020bbea63b139b22514a08798e3404ddef9519b3cd3a431b302b0a6df25f14374fe1356d6d51c245e485b576625e7ec6f44c42e9a637ed6b0bff5cb6f406b7edee386bfb5a899fa5ae9f24117c4b1fe649286651ece45b3dc2007cb8a163bf0598da48361c55d39a69163fa8fd24cf5f83655d23dca3ad961c62f356208552bb9ed529077096966d670c354e4abc9804f1746c08ca237327ffffffffffffffff',16)
g = 2
a = 83957930158391048329104375493285498324538914938249930158391048329104375493285498324538914938249243
b = 2479301583910483291043754932854983245389149382499301583910483291043754932854983245389149382493894

def mod_exp(base,exp,mod):
  memo = {}
  def mod_exp(base,exp,mod):
    if (base,exp,mod) in memo.keys():
      return memo[(base,exp,mod)]
    if exp < 2:
      v = (base**exp)%mod
      memo[(base,exp,mod)] = v
      return v
    v = (mod_exp(base,exp//2,mod)**2)%mod
    if exp%2 == 1:
      v = (v*base)%mod
    memo[(base,exp,mod)] = v
    return v
  v = mod_exp(base,exp,mod)
  return v

A = mod_exp(g,a,p)
B = mod_exp(g,b,p)
s = mod_exp(A,b,p)
sp = mod_exp(B,a,p)
print(s == sp)