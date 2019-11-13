from pyFHE.trlwe import trlweSymEncrypt, trlweSymDecrypt
from pyFHE.key import SecretKey
import numpy as np

np.set_printoptions(threshold=2000)
for i in range(1000):
    sk = SecretKey(500,2.44e-5,1024,2,10,3.73e-9,8,2,2.44e-5,2048,4,9,2**-44,10,3)
    p = np.random.randint(0, 2, size=sk.params.N, dtype=np.uint32)
    c = trlweSymEncrypt(
        (2 * p - 1) * 2 ** -3, sk.params.alpha, sk.key.trlwe, sk.params.twist
    )
    y = trlweSymDecrypt(c, sk.key.trlwe, sk.params.twist)
    if np.any(p != y):
        print(i)
        print(trlweSymDecrypt(c, sk.key.trlwe, sk.params.twist))
        break
