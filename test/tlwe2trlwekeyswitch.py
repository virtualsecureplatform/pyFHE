from pyFHE.tlwe import tlweSymEncrypt, tlweSymDecrypt
from pyFHE.key import SecretKey, CloudKey
from pyFHE.gatebootstrapping import GateBootstrappingTLWE2TLWElvl2FFT
from pyFHE.keyswitch import TLWE2TRLWEprivateKeySwitch
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
    mu = 1/sk.params.Bg
    y = GateBootstrappingTLWE2TLWElvl2FFT(x, ck, mu)
    z = TLWE2TRLWEprivateKeySwitch(y,ck,1)
    za = np.int32(z[1] - PolyMul(z[0], sk.key.trlwe, sk.params.twist))[0]*2**-32
    np.set_printoptions(threshold=2000)
    print(p*mu)
    print(za)

future_list = []
test()
print("completed.")
