from pyFHE.trlwe import trlweSymEncrypt,trlweSymDecrypt,SampleExtractIndex
from pyFHE.tlwe import tlweSymEncrypt,tlweSymDecrypt
from pyFHE.key import SecretKey, CloudKey
from pyFHE.gatebootstrapping import BlindRotateFFT
from pyFHE.utils import dtot32
import numpy as np

sk = SecretKey(500,2.44e-5,1024,2,10,3.73e-9,8,2,2.44e-5)
ck = CloudKey(sk)
r = trlweSymEncrypt(np.full(sk.params.N,2**-3),0,sk.key.trlwe,sk.params.twist)
t =  tlweSymEncrypt(-2**-3,sk.params.alpha,sk.key.tlwe)
bara = np.uint32(np.round(np.double(t) * (2**-32 * 2 * sk.params.N)))
index = (((np.dot(bara[:-1],sk.key.tlwe)-bara[-1])%(2*sk.params.N))+2*sk.params.N)%(sk.params.N)
np.set_printoptions(threshold=2000)
print(index)
print(trlweSymDecrypt(BlindRotateFFT(ck.bkfft,t,r,sk.params),sk.key.trlwe,sk.params.twist))
print(tlweSymDecrypt(SampleExtractIndex(BlindRotateFFT(ck.bkfft,t,r,sk.params),0),sk.key.trlwe))
