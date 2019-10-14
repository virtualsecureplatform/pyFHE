from pyFHE.tlwe import tlweSymEncrypt,tlweSymDecrypt
from pyFHE.key import SecretKey,CloudKey
from pyFHE.gatebootstrapping import GateBootstrappingTLWE2TLWEFFT
import numpy as np

for i in range(100):
    sk = SecretKey(500,2.44e-5,1024,2,10,3.73e-9,8,2,2.44e-5)
    bkfft = CloudKey(sk).bkfft
    p = np.random.binomial(1,0.5) 
    x = tlweSymEncrypt((p * 2 + -1) * (2**-3),sk.params.alpha,sk.key.tlwe)
    y = GateBootstrappingTLWE2TLWEFFT(x,bkfft,sk.params,sk.key.trlwe)
    np.set_printoptions(threshold=2000)
    if p != tlweSymDecrypt(y,sk.key.trlwe):
        print(p)
        print(tlweSymDecrypt(y,sk.key.trlwe))
        print("ERROR")
        print(i)
        break