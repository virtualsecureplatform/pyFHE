from pyFHE.mulfft import PolyMul,TwistGen
from pyFHE.utils import dtot32
import numpy as np

N = 1024
for i in range(1000):
    a = dtot32(np.random.random(N))*2**-32
    b = np.random.randint(0,2**10,N)# choose max = Bg
    ab = np.array(list(np.poly1d(a)*np.poly1d(b)))
    y=(ab[:N]-np.append(ab[N:],0))%1
    if np.any((np.abs(PolyMul(dtot32(a),b,TwistGen(N))*2**-32) - y) > 2**-31):
        print(i)
        print(y)
        print(PolyMul(dtot32(a),b,TwistGen(N))*2**-32)
        break