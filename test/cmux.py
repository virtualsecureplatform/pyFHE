from pyFHE.detwfa import CMUX
from pyFHE.trgsw import trgswSymEncrypt
from pyFHE.trlwe import trlweSymEncrypt,trlweSymDecrypt
from pyFHE.key import SecretKey
import numpy as np

np.set_printoptions(threshold=2000)
for i in range(100):
    sk = SecretKey(500,2**(-9),8,2,512,2**-27,8,2,2.44e-5)
    sk = SecretKey(500,2.44e-5,1024,2,1024,3.73e-9,8,2,2.44e-5)
    d0 = trlweSymEncrypt(np.full(sk.params.N,-2**-3),sk.params.alpha,sk.key.trlwe,sk.params.twist)
    d1 = trlweSymEncrypt(np.full(sk.params.N,-2**-3),sk.params.alpha,sk.key.trlwe,sk.params.twist)
    C = trgswSymEncrypt(np.append([0],np.zeros(sk.params.N - 1)),sk.params.bkalpha,sk.params.h,sk.key.trlwe,sk.params.twist)
    y = trlweSymDecrypt(CMUX(C,d0,d1,sk.params),sk.key.trlwe,sk.params.twist)
    if np.sum(y) != 0:
        print(i)
        print(y)
        break