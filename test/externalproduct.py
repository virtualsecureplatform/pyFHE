from pyFHE.trgsw import trgswSymEncrypt,trgswExternalProdcut
from pyFHE.trlwe import trlweSymEncrypt,trlweSymDecrypt
from pyFHE.key import SecretKey
from pyFHE.mulfft import PolyMul
import numpy as np

np.set_printoptions(threshold=2000)
sk = SecretKey(500,2**(-9),8,2,1024,2**-24,8,2,2.44e-5)
sk = SecretKey(500,2**(-7),1024,2,1024,3.73e-9,8,2,2.43e-5)
x = trlweSymEncrypt(np.full(sk.params.N,2**-3),sk.params.alpha,sk.key.trlwe,sk.params.twist)
A = trgswSymEncrypt(np.append([-1],np.zeros(sk.params.N - 1)),sk.params.bkalpha,sk.params.h,sk.key.trlwe,sk.params.twist)
y = trgswExternalProdcut(A,x,sk.params)
print(np.int32(A[0][1] - PolyMul(A[0][0],sk.key.trlwe,sk.params.twist)))
print(trlweSymDecrypt(y,sk.key.trlwe,sk.params.twist))