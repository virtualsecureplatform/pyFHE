from pyFHE import key,trlwe
import numpy as np

sk = key.SecretKey(500,2**(-9),2,2,512,2**(-24))
c = trlwe.trlweSymEncrypt(np.array([-2**(-3),2**(-3)]),2**(-27),sk.key.trlwe,sk.params.twist)
print (trlwe.trlweSymDecrypt(c,sk.key.trlwe,sk.params.twist))