from pyFHE.trlwe import trlweSymEncrypt,trlweSymDecrypt,SampleExtractIndex
from pyFHE.tlwe import tlweSymDecrypt
from pyFHE.key import SecretKey
import numpy as np

sk = SecretKey(500,2**(-9),2,2,512,2**(-27))
c = trlweSymEncrypt(np.array([2**-3,-2**-3]),2**(-24),sk.key.trlwe,sk.params.twist)
print(tlweSymDecrypt(SampleExtractIndex(c,0),sk.key.trlwe))
print(tlweSymDecrypt(SampleExtractIndex(c,1),sk.key.trlwe))