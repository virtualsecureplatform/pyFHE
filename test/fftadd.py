from pyFHE.mulfft import TwistFFT, TwistIFFT, TwistGen
import numpy as np

a = [-1, 2 ** 31, 0, 1]
b = [2, 3, 1, 2]
twist = TwistGen(4)

print(TwistIFFT(np.sum([TwistFFT(a, twist), TwistFFT(b, twist)], axis=0), twist))
