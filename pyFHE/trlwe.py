from .mulfft import PolyMul
from .utils import gaussian32,dtot32
import numpy as np

def trlweSymEncrypt(p,alpha,key,twist):
    a = np.random.randint(0,2**32 ,size = len(key), dtype = np.uint32)
    b = gaussian32(dtot32(p),alpha,len(key)) 
    b += PolyMul(a,key,twist)
    return np.array([a,b])

def trlweSymDecrypt(c,key,twist):
    return (1 + np.sign(np.int32(c[1] - PolyMul(c[0],key,twist))))//2

def SampleExtractIndex(r,index):
    N = len(r[0])
    return np.concatenate([[r[0][index-i] for i in range(index+1)],[-r[0][N-1-i] for i in range(N-index-1)],[r[1][index]]])