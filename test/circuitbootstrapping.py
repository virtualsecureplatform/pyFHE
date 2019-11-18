from pyFHE.tlwe import tlweSymEncrypt, tlweSymDecrypt
from pyFHE.trlwe import trlweSymEncrypt,trlweSymDecrypt
from pyFHE.key import SecretKey, CloudKey
from pyFHE.gatebootstrapping import CircuitBootstrapping
from pyFHE.trgsw import trgswExternalProduct
from pyFHE.mulfft import PolyMul
import numpy as np

from concurrent import futures
from os import cpu_count


def test():
    sk = SecretKey(500,2.44e-5,1024,2,10,3.73e-9,8,2,2.44e-5,2048,4,9,2**-44,10,3,2**-31)
    ck = CloudKey(sk)
    p = np.random.binomial(1, 0.5)
    p = 1
    x = tlweSymEncrypt((p * 2 + -1) * (2 ** -3), sk.params.alpha, sk.key.tlwe)
    r = trlweSymEncrypt(np.full(sk.params.N,(p * 2 + -1) * (2 ** -3)), sk.params.alpha, sk.key.trlwe,sk.params.twist)
    y = CircuitBootstrapping(x,ck)
    print(y.shape)
    z = trgswExternalProduct(y,r,ck.params)
    np.set_printoptions(threshold=2000)
    za = trlweSymDecrypt(z,sk.key.trlwe,sk.params.twist)
    print(za)

future_list = []
test()
print("completed.")
