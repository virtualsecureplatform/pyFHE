from pyFHE.mulfft import PolyMul, TwistGen
from pyFHE.utils import dtot32
from pyFHE.key import FFTplans,SecretKey
import numpy as np

N = 1024
Bg = 1024
twist = TwistGen(N)
sk = SecretKey(500, 2 ** (-7), 1024, 2, 10, 3.73e-9, 8, 2, 2.43e-5)
plan = FFTplans(sk)
for i in range(10000):
    a = dtot32(np.random.random(N)) * 2 ** -32
    b = np.int32(np.random.randint(-Bg / 2, Bg / 2, N))  # choose max = Bg
    ab = np.flip(np.array(np.poly1d(np.flip(a)) * np.poly1d(np.flip(b))))
    y = (ab[:N] - np.append(ab[N:], np.zeros(2 * N - len(ab)))) % 1
    # y = np.flip(np.array((ab/np.poly1d(np.append(1,np.append(np.zeros(N-1),-1))))[0])%1)
    a = np.uint32(dtot32(a))
    c = PolyMul(a, np.uint32(b), twist, plan.fft,plan.ifft)
    if np.any((np.abs(c * 2 ** -32) - y) > 2 ** -60):
        print(i)
        print(y)
        print(c * 2 ** -32)
        break
