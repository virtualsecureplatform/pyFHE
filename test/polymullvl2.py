from pyFHE.mulfft import PolyMullvl2, TwistGen,TwistFFT,TwistIFFT
from pyFHE.utils import dtot64
from pyFHE.key import SecretKey
import numpy as np

N = 2048
Bg = 2**9
twist = TwistGen(N)
for i in range(10000):
    a = dtot64(np.random.random(N)) * 2 ** -64
    b = np.int64(np.random.randint(-Bg // 2, Bg // 2, N))  # choose max = Bg
    ab = np.flip(np.array(np.poly1d(np.flip(a)) * np.poly1d(np.flip(b))))
    y = (ab[:N] - np.append(ab[N:], np.zeros(2 * N - len(ab)))) % 1
    # y = np.flip(np.array((ab/np.poly1d(np.append(1,np.append(np.zeros(N-1),-1))))[0])%1)
    a = np.uint64(dtot64(a))
    c = PolyMullvl2(a, np.uint64(b), twist)
    if np.any((np.abs(c * 2 ** -64) - y) > 2 ** -35):
        print(i)
        print(y)
        print(np.abs(c * 2 ** -64) - y)
        print(c * 2 ** -64)
        break
