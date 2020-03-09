
from pyFHE.tlwe import tlweSymEncrypt,tlweSymDecrypt
from pyFHE.key import SecretKey,CloudKey
from pyFHE.controller import GateBootstrapping

import numpy as np
import time


def test():
    sk = SecretKey(500,2.44e-5,1024,2,10,3.73e-9,8,2,2.44e-5)
    ck = CloudKey(sk)
    p = np.random.binomial(1,0.5)
    c = tlweSymEncrypt((p * 2 + -1) * (2**-3),sk.params.alpha,sk.key.tlwe)
    res = GateBootstrapping(c,ck)
    y = tlweSymDecrypt(res,sk.key.tlwe)
    np.set_printoptions(threshold=2000)
    if p != y:
        print("FAILED")
        print(tlweSymDecrypt(np.uint32(np.append(np.zeros(ck.params.n),2**29)) - ca - cb,sk.key.tlwe))
        print(y)
        exit()
test()
print('completed.')