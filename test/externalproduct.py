from pyFHE.trlwe import trlweSymEncrypt, trlweSymDecrypt
from pyFHE.trgsw import trgswfftSymEncrypt, trgswfftExternalProduct
from pyFHE.key import SecretKey
import numpy as np

np.set_printoptions(threshold=4000)
for i in range(100):
    sk = SecretKey(500,2.44e-5,1024,2,10,3.73e-9,8,2,2.44e-5,2048,4,9,2**-44,10,3,2**-31)
    x = trlweSymEncrypt(
        np.full(sk.params.N, 2 ** -3), sk.params.alpha, sk.key.trlwe, sk.params.twist
    )
    A = trgswfftSymEncrypt(
        np.append([1], np.zeros(sk.params.N - 1)),
        sk.params.bkalpha,
        sk.params.h,
        sk.key.trlwe,
        sk.params.twist,
    )
    y = trgswfftExternalProduct(A, x, sk.params)
    print(y)
    if np.sum(trlweSymDecrypt(y, sk.key.trlwe, sk.params.twist)) != len(y[0]):
        print(trlweSymDecrypt(y, sk.key.trlwe, sk.params.twist))
        print(np.uint32(y))
        print(i)
        break
