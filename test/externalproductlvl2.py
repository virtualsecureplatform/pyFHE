from pyFHE.trlwe import trlweSymEncryptlvl2,trlweSymDecrypt
from pyFHE.trgsw import trgswfftSymEncryptlvl2,trgswfftExternalProductlvl2
from pyFHE.key import SecretKey,CloudKey
from pyFHE.utils import dtot32
import numpy as np

np.set_printoptions(threshold=2000)
for i in range(100):
    sk = SecretKey(500,2.44e-5,1024,2,10,3.73e-9,8,2,2.44e-5,2048,4,9,2**-44,10,3)
    ck = CloudKey(sk)
    x = trlweSymEncryptlvl2(np.full(sk.params.N,2**-3),sk.params.alpha,sk.key.lvl2,sk.params.twistlvl2,ck.fftlvl2,ck.ifftlvl2)
    A = trgswfftSymEncryptlvl2(np.append([1],np.zeros(sk.params.nbar - 1)),sk.params.bklvl02alpha,sk.params.hbar,sk.key.lvl2,sk.params.twistlvl2,ck.fftlvl2,ck.ifftlvl2)
    y = trgswfftExternalProductlvl2(A,x,sk.params,ck.fftlvl2,ck.ifftlvl2)
    if np.sum(trlweSymDecrypt(y,sk.key.trlwe,sk.params.twistlvl2,ck.fftlvl2,ck.ifftlvl2)) != len(y[0]):
        print(sk.params.decb)
        print(trlweSymDecrypt(y,sk.key.trlwe,sk.params.twistlvl2,ck.fftlvl2,ck.ifftlvl2))
        print(np.uint32(y))
        print(i)
        break