from pyFHE.trlwe import trlweSymEncrypt, trlweSymDecrypt
from pyFHE.trgsw import trgswfftSymEncrypt, trgswfftExternalProduct
from pyFHE.key import SecretKey, FFTplans
from pyFHE.utils import dtot32
import numpy as np

np.set_printoptions(threshold=2000)
for i in range(100):
    sk = SecretKey(500, 2 ** (-7), 1024, 2, 10, 3.73e-9, 8, 2, 2.43e-5)
    plan = FFTplans(sk)
    x = trlweSymEncrypt(
        np.full(sk.params.N, 2 ** -3), sk.params.alpha, sk.key.trlwe, sk.params.twist, plan.fft,plan.ifft
    )
    A = trgswfftSymEncrypt(
        np.append([1], np.zeros(sk.params.N - 1)),
        sk.params.bkalpha,
        sk.params.h,
        sk.key.trlwe,
        sk.params.twist,
        plan.fft,
        plan.ifft
    )
    y = trgswfftExternalProduct(A, x, sk.params, plan.fft, plan.ifft)
    if np.sum(trlweSymDecrypt(y, sk.key.trlwe, sk.params.twist, plan.fft, plan.ifft)) != len(y[0]):
        print(trlweSymDecrypt(y, sk.key.trlwe, sk.params.twist,plan.fft,plan.ifft))
        print(np.uint32(y))
        print(i)
        break
