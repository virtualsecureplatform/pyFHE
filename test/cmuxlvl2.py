from pyFHE.detwfa import CMUXFFTlvl2
from pyFHE.trgsw import trgswfftSymEncryptlvl2
from pyFHE.trlwe import trlweSymEncryptlvl2, trlweSymDecryptlvl2
from pyFHE.key import SecretKey
import numpy as np

np.set_printoptions(threshold=5000)
for i in range(1000):
    sk = SecretKey(500,2.44e-5,1024,2,10,3.73e-9,8,2,2.44e-5,2048,4,9,2**-44,10,3,2**-31)
    p0 = np.random.randint(0, 2, size=sk.params.nbar, dtype=np.int64)
    p1 = np.random.randint(0, 2, size=sk.params.nbar, dtype=np.int64)
    d0 = trlweSymEncryptlvl2(
        (2 * p0 - 1) * 2 ** -3, sk.params.bklvl02alpha, sk.key.lvl2, sk.params.twistlvl2long
    )
    d1 = trlweSymEncryptlvl2(
        (2 * p1 - 1) * 2 ** -3, sk.params.bklvl02alpha, sk.key.lvl2, sk.params.twistlvl2long
    )
    c = np.random.randint(0, 2)
    CFFT = trgswfftSymEncryptlvl2(
        np.append([c], np.zeros(sk.params.nbar - 1)),
        sk.params.bklvl02alpha,
        sk.params.hbar,
        sk.key.lvl2,
        sk.params.twistlvl2long,
    )
    y =CMUXFFTlvl2(CFFT, d1, d0, sk.params)
    print(y)
    z = trlweSymDecryptlvl2(y, sk.key.lvl2, sk.params.twistlvl2long)
    if np.any(c * (p1 - p0) + p0 != z):
        print(i)
        print(p0)
        print(p1)
        print(c)
        print(c * (p1 - p0) + p0)
        print(z)
        break