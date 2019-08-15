from pyFHE.detwfa import CMUX
from pyFHE.trgsw import trgswSymEncrypt
from pyFHE.trlwe import trlweSymEncrypt,trlweSymDecrypt
from pyFHE.key import SecretKey
import numpy as np

sk = SecretKey(500,2**(-9),8,2,512,2**-27)
d0 = trlweSymEncrypt(np.array([2**-3,0,0,0,0,0,0,0]),2**-27,sk.key.trlwe,sk.params.twist)
d1 = trlweSymEncrypt(np.array([-2**-3,0,0,0,0,0,0,0]),2**-27,sk.key.trlwe,sk.params.twist)
C = trgswSymEncrypt(np.array([0,0,0,0,0,0,0,0]),sk.params.bkalpha,sk.params.h,sk.key.trlwe,sk.params.twist)
print(trlweSymDecrypt(CMUX(C,d0,d1,sk.params),sk.key.trlwe,sk.params.twist)[0])