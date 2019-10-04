from pyFHE.trlwe import trlweSymEncrypt,trlweSymDecrypt
from pyFHE.tlwe import tlweSymEncrypt
from pyFHE.key import SecretKey, CloudKey
from pyFHE.gatebootstrapping import BlindRotate
import numpy as np

sk = SecretKey(10,2**(-31),128,2,1024,0)
ck = CloudKey(sk)
r = trlweSymEncrypt(np.concatenate([[2**-3],np.full(sk.params.N-1,-2**-3)]),0,sk.key.trlwe,sk.params.twist)
t =  tlweSymEncrypt(2**-3,sk.params.alpha,sk.key.tlwe)
bara = np.uint32(np.round(np.double(t) * (2**-32 * 2 * sk.params.N)))
index = (((np.dot(bara[:-1],sk.key.tlwe)-bara[-1])%(2*sk.params.N))+2*sk.params.N)%(sk.params.N)
print(index)
print(trlweSymDecrypt(BlindRotate(ck.bk,t,r,sk.params),sk.key.trlwe,sk.params.twist))