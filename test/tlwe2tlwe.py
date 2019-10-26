from pyFHE.tlwe import tlweSymEncrypt,tlweSymDecrypt
from pyFHE.key import SecretKey,CloudKey
from pyFHE.gatebootstrapping import GateBootstrappingTLWE2TLWEFFT
import numpy as np

from concurrent import futures
from os import cpu_count

def test():
    sk = SecretKey(500,2.44e-5,1024,2,10,3.73e-9,8,2,2.44e-5)
    ck = CloudKey(sk)
    p = np.random.binomial(1,0.5) 
    x = tlweSymEncrypt((p * 2 + -1) * (2**-3),sk.params.alpha,sk.key.tlwe)
    y = GateBootstrappingTLWE2TLWEFFT(x,ck)
    np.set_printoptions(threshold=2000)
    if p != tlweSymDecrypt(y,sk.key.trlwe):
        print(p)
        print(tlweSymDecrypt(y,sk.key.trlwe))
        print(i)
        exit()

future_list = []
for i in range(10):
    test()
print('completed.')