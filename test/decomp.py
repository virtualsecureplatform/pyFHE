from pyFHE.trgsw import Decomposition
from pyFHE.trlwe import trlweSymEncrypt,trlweSymDecrypt
from pyFHE.key import SecretKey
from pyFHE.utils import dtot32
import numpy as np

sk = SecretKey(500,2**(-9),2,2,512,2**(-27))
c = trlweSymEncrypt(np.array([2**-3,-2**-3]),2**(-24),sk.key.trlwe,sk.params.twist)
cdec = Decomposition(c,sk.params)
rec = dtot32(np.array([cdec[0] * sk.params.h[0] + cdec[1] * sk.params.h[1],cdec[2] * sk.params.h[0] + cdec[3] * sk.params.h[1]]))
print(sk.params.h)
print(c)
print(cdec)
print(rec)
print(trlweSymDecrypt(rec,sk.key.trlwe,sk.params.twist))