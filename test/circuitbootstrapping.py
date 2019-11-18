from pyFHE.tlwe import tlweSymEncrypt, tlweSymDecrypt
from pyFHE.trlwe import trlweSymEncrypt,trlweSymDecrypt
from pyFHE.key import SecretKey, CloudKey
from pyFHE.gatebootstrapping import CircuitBootstrappingFFT
from pyFHE.detwfa import CMUXFFT
from pyFHE.mulfft import PolyMul
import numpy as np

from concurrent import futures
from os import cpu_count


def test():
    sk = SecretKey(500,2.44e-5,1024,2,10,3.73e-9,8,2,2.44e-5,2048,4,9,2**-44,10,3,2**-31)
    ck = CloudKey(sk)
    p = np.random.binomial(1, 0.5)
    p = 0
    x = tlweSymEncrypt((p * 2 + -1) * (2 ** -3), sk.params.alpha, sk.key.tlwe)
    d0 = trlweSymEncrypt(np.full(sk.params.N,(0 * 2 + -1) * (2 ** -3)), sk.params.alpha, sk.key.trlwe,sk.params.twist)
    d1 = trlweSymEncrypt(np.full(sk.params.N,(1 * 2 + -1) * (2 ** -3)), sk.params.alpha, sk.key.trlwe,sk.params.twist)
    y = CircuitBootstrappingFFT(x,ck)
    print(y.shape)
    z = CMUXFFT(y,d1,d0,ck.params)
    np.set_printoptions(threshold=2000)
    za = trlweSymDecrypt(z,sk.key.trlwe,sk.params.twist)
    print(za)

future_list = []
test()
print("completed.")
