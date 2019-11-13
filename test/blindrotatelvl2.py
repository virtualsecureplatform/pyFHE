from pyFHE.trlwe import trlweSymEncryptlvl2, trlweSymDecryptlvl2, SampleExtractIndex
from pyFHE.tlwe import tlweSymEncrypt, tlweSymDecrypt
from pyFHE.key import SecretKey, CloudKey
from pyFHE.gatebootstrapping import BlindRotateFFTlvl2
import numpy as np

sk = SecretKey(500,2.44e-5,1024,2,10,3.73e-9,8,2,2.44e-5,2048,4,9,2**-44,10,3)
ck = CloudKey(sk)
r = trlweSymEncryptlvl2(np.full(sk.params.nbar, 2 ** -3), 0, sk.key.lvl2, sk.params.twistlvl2long)
t = tlweSymEncrypt(-(2 ** -3), sk.params.alpha, sk.key.tlwe)
bara = np.uint32(np.round(np.double(t) * (2 ** -32 * 2 * sk.params.nbar)))
index = (
    ((np.dot(bara[:-1], sk.key.tlwe) - bara[-1]) % (2 * sk.params.nbar)) + 2 * sk.params.nbar
) % (sk.params.nbar)
np.set_printoptions(threshold=4000)
Y = BlindRotateFFTlvl2(ck.bklvl2fft, t, r, sk.params)
print(index)
print(trlweSymDecryptlvl2(Y, sk.key.lvl2, sk.params.twistlvl2long))
print(tlweSymDecrypt(SampleExtractIndex(Y, 0), sk.key.trlwe))
