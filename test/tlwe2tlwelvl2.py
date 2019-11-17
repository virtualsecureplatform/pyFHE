from pyFHE.tlwe import tlweSymEncrypt, tlweSymDecrypt
from pyFHE.key import SecretKey, CloudKey
from pyFHE.gatebootstrapping import GateBootstrappingTLWE2TLWElvl2FFT
import numpy as np

from concurrent import futures
from os import cpu_count


def test():
    sk = SecretKey(500,2.44e-5,1024,2,10,3.73e-9,8,2,2.44e-5,2048,4,9,2**-44,10,3,2**-31)
    ck = CloudKey(sk)
    p = np.random.binomial(1, 0.5)
    x = tlweSymEncrypt((p * 2 + -1) * (2 ** -3), sk.params.alpha, sk.key.tlwe)
    mu = 1/sk.params.Bgbar
    y = GateBootstrappingTLWE2TLWElvl2FFT(x, ck, mu)
    print(y)
    z = np.int64(y[-1] - np.dot(y[:-1], sk.key.lvl2))
    np.set_printoptions(threshold=2000)
    print(i)
    print(p*mu)
    if abs(p*mu - z*2**-64)>mu/2:
        print(p*mu)
        print(z)
        exit()


future_list = []
for i in range(10):
    test()
print("completed.")
