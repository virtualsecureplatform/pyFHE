from pyFHE.trgsw import Decomposition
from pyFHE.trlwe import trlweSymEncrypt, trlweSymDecrypt
from pyFHE.key import SecretKey, FFTplans
from pyFHE.utils import dtot32
import numpy as np

for i in range(1000):
    sk = SecretKey(500, 2 ** (-7), 1024, 2, 10, 3.73e-9, 8, 2, 2.43e-5)
    plan = FFTplans(sk)
    p = np.random.randint(0, 2, size=sk.params.N, dtype=np.uint32)
    c = trlweSymEncrypt(
        (2 * p - 1) * 2 ** -3, sk.params.alpha, sk.key.trlwe, sk.params.twist, plan.fft, plan.ifft
    )
    cdec = Decomposition(c, sk.params)
    h = dtot32(sk.params.h)
    rec = np.array([cdec[0] * h[0] + cdec[1] * h[1], cdec[2] * h[0] + cdec[3] * h[1]])
    if np.any(trlweSymDecrypt(rec, sk.key.trlwe, sk.params.twist, plan.fft, plan.ifft) != p):
        print(i)
        break
