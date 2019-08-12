import numpy as np
from .key import SecretKey
from .mulfft import PolyMul

def trlweSymEncrypt(p,sk:SecretKey):
    a = np.random.randint(-2**31,2**31 ,size = (sk.params.k,sk.params.N), dtype = np.int32)
    b = np.array(p) + np.sum([PolyMul(a[i],sk.key.trlwe[i],sk.twist) for i in range(sk.params.k)],axis = 0)
    return np.append(a,b)