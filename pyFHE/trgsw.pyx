import numpy as np
cimport numpy as np
from .trlwe import trlweSymEncrypt
from .mulfft import PolyMul,TwistFFT,TwistIFFT
from .utils import dtot32

#Gadget Decomposition.
cdef np.ndarray[np.uint32_t,ndim = 2] Decomposition(np.ndarray[np.uint32_t,ndim = 2] trlwe, params):
    cdef np.ndarray[np.uint32_t,ndim = 3] temp = np.uint32(np.floor(np.multiply.outer(params.decb,trlwe + params.offset)%params.Bg) - params.Bg/2) #DOING FLOOR IS IMPORTANT.
    return np.concatenate([temp[:,0],temp[:,1]])

cdef np.ndarray[np.complex128_t,ndim = 2] DecompositionFFT(np.ndarray[np.uint32_t,ndim = 2] trlwe,params):
    cdef np.ndarray[np.int32_t,ndim = 2] decvec = np.int32(Decomposition(trlwe,params))
    cdef int i
    return np.array([TwistFFT(decvec[i],params.twist) for i in range(2 * params.l)])

def trgswSymEncrypt(np.ndarray[np.uint32_t] p,float alpha,np.ndarray[np.float64_t] h,np.ndarray[np.uint32_t] key, np.ndarray[np.complex128_t] twist):
    cdef int l = len(h)
    cdef np.ndarray[np.uint32_t,ndim = 3] c = np.vstack([[trlweSymEncrypt(np.zeros(len(key)),alpha,key,twist)] for i in range(2*l)])
    cdef np.ndarray[np.uint32_t,ndim = 2] muh = dtot32(np.outer(h,p))
    c[:l,0] += muh
    c[l:,1] += muh
    return c

def trgswfftSymEncrypt(np.ndarray[np.uint32_t] p, float alpha,np.ndarray[np.float64_t]h,np.ndarray[np.uint32_t] key, np.ndarray[np.complex128_t] twist):
    cdef np.ndarray[np.int32_t, ndim = 3] trgsw = np.int32(trgswSymEncrypt(p, alpha, h, key, twist))
    cdef int i,j
    return np.array([np.array([TwistFFT(trgsw[i][j],twist) for j in range(2)]) for i in range(2 * len(h))])

def trgswfftExternalProduct(np.ndarray[np.complex128_t,ndim = 3] trgswfft,np.ndarray[np.uint32_t,ndim = 2] trlwe, params):
    cdef np.ndarray[np.complex128_t,ndim = 2] decvecfft = DecompositionFFT(trlwe,params)
    # if l is small enough, adding before IFFT doesn't make much noise and reduce number of IFFT which is a very heavy function.
    cdef int i
    return np.array([np.uint32(np.round(TwistIFFT(np.sum([np.multiply(decvecfft[i], trgswfft[i][0]) for i in range(2 * params.l)],axis = 0),params.twist))%2**32),np.uint32(np.round(TwistIFFT(np.sum([np.multiply(decvecfft[i], trgswfft[i][1]) for i in range(2 * params.l)], axis = 0),params.twist))%2**32)],dtype = np.uint32)

#These are not optimized functions. Just for making reader easier to understand the algorithm.
#def trgswExternalProduct(g,r,params):
#    cdef np.ndarray[np.uint32_t,ndim = 2] decvec = Decomposition(r,params)
#    return np.array([np.sum([PolyMul(decvec[i], g[i][0],params.twist) for i in range(2 * params.l)],axis = 0),np.sum([PolyMul(decvec[i], g[i][1],params.twist) for i in range(2 * params.l)], axis = 0)],dtype = np.uint32)