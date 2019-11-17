from pyFHE.trgsw import Decomposition
from pyFHE.trlwe import trlweSymEncrypt,trlweSymDecrypt
from pyFHE.key import SecretKey
from pyFHE.utils import dtot32
import numpy as np

for i in range(1000):
    sk = SecretKey(500,2**(-7),1024,2,1024,3.73e-9,8,2,2.43e-5)
    p = np.random.randint(0,2,size = sk.params.N,dtype = np.uint32)
    c = trlweSymEncrypt((2*p-1)*2**-3,sk.params.alpha,sk.key.trlwe,sk.params.twist)
    cdec = Decomposition(c,sk.params)
    print(np.int32(cdec))
    h = dtot32(sk.params.h)
    rec = np.array([cdec[0] * h[0] + cdec[1] * h[1],cdec[2] * h[0] + cdec[3] * h[1]])
    if np.any(trlweSymDecrypt(rec,sk.key.trlwe,sk.params.twist) != p): 
        print(i)
        break