from pyFHE.trgsw import trgswSymEncrypt,trgswExternalProdcut
from pyFHE.trlwe import trlweSymEncrypt,trlweSymDecrypt
from pyFHE.key import SecretKey
import numpy as np

sk = SecretKey(500,2**(-9),8,2,1024,0)
x = trlweSymEncrypt(np.array([-2**-3,0,0,0,0,0,0,0]),0,sk.key.trlwe,sk.params.twist)
A = trgswSymEncrypt(np.array([1,0,0,0,0,0,0,0]),sk.params.bkalpha,sk.params.h,sk.key.trlwe,sk.params.twist)
y = trgswExternalProdcut(A,x,sk.params)
print(trlweSymDecrypt(y,sk.key.trlwe,sk.params.twist))