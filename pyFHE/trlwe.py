import numpy as np
from .key import SecretKey
from .mulfft import PolyMul
from .utils import gaussian32

def trlweSymEncrypt(p,alpha,key,twist):
    a = np.random.randint(0,2**32 ,size = len(key), dtype = np.uint32)
    b = gaussian32(p,alpha,len(key)) 
    b += PolyMul(a,key,twist)
    return np.array([a,b])

def trlweSymDecrypt(c,key,twist):
    return (1 + np.sign(np.int32(c[1] - PolyMul(c[0],key,twist))))//2