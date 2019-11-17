from pyFHE.detwfa import CMUXFFT
from pyFHE.trgsw import trgswfftSymEncrypt
from pyFHE.trlwe import trlweSymEncrypt,trlweSymDecrypt
from pyFHE.key import SecretKey
import numpy as np

np.set_printoptions(threshold=2000)
for i in range(1000):
    sk = SecretKey(500,2.44e-5,1024,2,10,3.73e-9,8,8,2.44e-5)
    p0 = np.random.randint(0,2,size = sk.params.N,dtype=np.uint32)
    p1 = np.random.randint(0,2,size = sk.params.N,dtype=np.uint32)
    d0 = trlweSymEncrypt((2*p0 - 1)*2**-3,sk.params.alpha,sk.key.trlwe,sk.params.twist)
    d1 = trlweSymEncrypt((2*p1 - 1)*2**-3,sk.params.alpha,sk.key.trlwe,sk.params.twist)
    c = np.random.randint(0,2)
    CFFT = trgswfftSymEncrypt(np.append([c],np.zeros(sk.params.N - 1)),sk.params.bkalpha,sk.params.h,sk.key.trlwe,sk.params.twist)
    y = trlweSymDecrypt(CMUXFFT(CFFT,d1,d0,sk.params),sk.key.trlwe,sk.params.twist)
    if np.any(c*(p1-p0)+p0 != y):
        print(i)
        print(p0)
        print(p1)
        print(c)
        print(c*(p1-p0)+p0)
        print(y)
        break