from pyFHE.mulfft import PolyMul,TwistGen
from pyFHE.utils import dtot32
import numpy as np

N = 1024
twist = TwistGen(N)
for i in range(10000):
    a = dtot32(np.random.random(N))*2**-32
    b = np.uint32(np.random.randint(0,2**10,N))# choose max = Bg
    ab = np.flip(np.array(np.poly1d(np.flip(a))*np.poly1d(np.flip(b))))
    y=(ab[:N]-np.append(ab[N:],np.zeros(2*N-len(ab))))%1
    #y = np.flip(np.array((ab/np.poly1d(np.append(1,np.append(np.zeros(N-1),-1))))[0])%1)
    a =np.uint32(dtot32(a))
    c = PolyMul(a,b,twist)
    if np.any((np.abs(c*2**-32) - y) > 2**-31):
        print(i)
        print(y)
        print(c*2**-32)
        break
