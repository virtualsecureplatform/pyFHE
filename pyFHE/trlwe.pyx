from .mulfft cimport PolyMul
from .utils cimport gaussian32,dtot32array
from secrets import randbits
import numpy as np
cimport numpy as np

def trlweSymEncrypt(np.ndarray[np.float64_t] p,double alpha,np.uint32_t[:] key,np.complex128_t[:] twist):
    a = np.array([randbits(32) for i in range(len(key))], dtype = np.uint32)
    b = gaussian32(dtot32array(p),alpha) 
    b += PolyMul(a,np.array(key),twist)
    return np.array([a,b])

def trlweSymDecrypt(c,np.uint32_t[:] key,twist):
    return (1 + np.sign(np.int32(c[1] - PolyMul(c[0],key,twist))))//2

cdef np.ndarray[np.uint32_t] SampleExtractIndex(np.ndarray[np.uint32_t, ndim = 2] trlwe,int index):
    cdef int i
    cdef int N = len(trlwe[0])
    return np.concatenate([[trlwe[0][index-i] for i in range(index+1)],[-trlwe[0][N-1-i] for i in range(N-index-1)],[trlwe[1][index]]])