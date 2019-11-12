from .mulfft import PolyMul,PolyMullvl2
from .utils import gaussian32,dtot32,gaussian64,dtot64
from secrets import randbits
import numpy as np

def trlweSymEncrypt(p,alpha,key,twist,fft,ifft):
    a = np.array([randbits(32) for i in range(len(key))], dtype = np.uint32)
    b = gaussian32(dtot32(p),alpha,len(key)) 
    b += PolyMul(a,key,twist,fft,ifft)
    return np.array([a,b])

def trlweSymEncryptlvl2(p,alpha,key,twist,fft,ifft):
    a = np.array([randbits(64) for i in range(len(key))], dtype = np.uint64)
    b = gaussian64(dtot64(p),alpha,len(key))
    b += PolyMullvl2(a,key,twist,fft,ifft)
    return np.array([a,b])

def trlweSymDecrypt(c,key,twist,fft,ifft):
    return (1 + np.sign(np.int32(c[1] - PolyMul(c[0],key,twist,fft,ifft))))//2

def SampleExtractIndex(r,index):
    N = len(r[0])
    return np.concatenate([[r[0][index-i] for i in range(index+1)],[-r[0][N-1-i] for i in range(N-index-1)],[r[1][index]]])