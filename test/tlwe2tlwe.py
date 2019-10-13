from pyFHE.tlwe import tlweSymEncrypt,tlweSymDecrypt
from pyFHE.key import SecretKey,CloudKey
from pyFHE.gatebootstrapping import GateBootstrappingTLWE2TLWE
import numpy as np

for i in range(100):
    sk = SecretKey(500,2.44e-5,1024,2,1024,3.73e-9,8,2,2.44e-5)
    #sk = SecretKey(10,2**(-31),128,2,1024,0,2,1,2**(-24))
    bk = CloudKey(sk).bk
    p = np.random.binomial(1,0.5) 
    x = tlweSymEncrypt((p * 2 + -1) * (2**-3),sk.params.alpha,sk.key.tlwe)
    y = GateBootstrappingTLWE2TLWE(x,bk,sk.params,sk.key.trlwe)
    np.set_printoptions(threshold=2000)
    if p != tlweSymDecrypt(y,sk.key.trlwe):
        print(p)
        print(tlweSymDecrypt(y,sk.key.trlwe))
        print("ERROR")
        print(i)
        break