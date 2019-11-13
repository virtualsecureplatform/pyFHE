from pyFHE.trgsw import Decompositionlvl2
from pyFHE.trlwe import trlweSymEncryptlvl2, trlweSymDecryptlvl2
from pyFHE.key import SecretKey
from pyFHE.utils import dtot64
import numpy as np

for i in range(1000):
    sk = SecretKey(500,2.44e-5,1024,2,10,3.73e-9,8,2,2.44e-5,2048,4,9,2**-44,10,3)
    p = np.random.randint(0, 2, size=sk.params.nbar, dtype=np.int64)
    c = trlweSymEncryptlvl2(
        (2 * p - 1) * 2 ** -3, sk.params.bklvl02alpha, sk.key.lvl2, sk.params.twistlvl2long
    )
    cdec = Decompositionlvl2(c, sk.params)
    h = dtot64(sk.params.hbar)
    rec = np.sum([[cdec[i] * h[i], cdec[sk.params.lbar + i] * h[i]] for i in range(sk.params.lbar)],axis=0)
    if np.any(trlweSymDecryptlvl2(rec, sk.key.lvl2, sk.params.twistlvl2long) != p):
        print(i)
        break