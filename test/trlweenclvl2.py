from pyFHE.trlwe import trlweSymEncryptlvl2, trlweSymDecryptlvl2
from pyFHE.key import SecretKey
import numpy as np

np.set_printoptions(threshold=2000)
for i in range(1000):
    sk = SecretKey(500,2.44e-5,1024,2,10,3.73e-9,8,2,2.44e-5,2048,4,9,2**-44,10,3)
    p = np.random.randint(0, 2, size=sk.params.nbar, dtype=np.int64)
    c = trlweSymEncryptlvl2(
        (2 * p - 1) * (2 ** -3), sk.params.bklvl02alpha, sk.key.lvl2, sk.params.twistlvl2long
    )
    y = trlweSymDecryptlvl2(c, sk.key.lvl2, sk.params.twistlvl2long)
    if np.any(p != y):
        print(i)
        print(p)
        print(y)
        break
