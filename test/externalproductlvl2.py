from pyFHE.trlwe import trlweSymEncryptlvl2, trlweSymDecryptlvl2
from pyFHE.trgsw import trgswfftSymEncryptlvl2, trgswfftExternalProductlvl2
from pyFHE.key import SecretKey
from pyFHE.mulfft import PolyMullvl2Long
import numpy as np

np.set_printoptions(threshold=5000)
for i in range(100):
    sk = SecretKey(500,2.44e-5,1024,2,10,3.73e-9,8,2,2.44e-5,2048,4,9,2**-44,10,3,2**-31)
    x = trlweSymEncryptlvl2(
        np.full(sk.params.nbar, 2 ** -3), sk.params.bklvl02alpha, sk.key.lvl2, sk.params.twistlvl2
    )
    A = trgswfftSymEncryptlvl2(
        np.append([1], np.zeros(sk.params.nbar - 1)),
        sk.params.bklvl02alpha,
        sk.params.hbar,
        sk.key.lvl2,
        sk.params.twistlvl2,
        sk.params.twistlvl2long
    )
    y = trgswfftExternalProductlvl2(A, x, sk.params)
    print(y)
    if np.sum(trlweSymDecryptlvl2(y, sk.key.lvl2, sk.params.twistlvl2long)) != len(y[0]):
        print(trlweSymDecryptlvl2(y, sk.key.lvl2, sk.params.twistlvl2long))
        print(np.int64(y))
        print(i)
        break