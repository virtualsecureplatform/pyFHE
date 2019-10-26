import numpy as np
cimport numpy as np
from .trlwe import trlweSymEncrypt
from .mulfft import PolyMul,TwistFFT,TwistIFFT
from .utils import dtot32

#Gadget Decomposition.
cpdef Decomposition(np.ndarray[np.uint32_t,ndim = 2] trlwe,params):
    cdef np.ndarray[np.uint32_t,ndim = 3] temp = np.uint32(np.floor(np.multiply.outer(params.decb,trlwe + params.offset)%params.Bg) - params.Bg/2) #DOING FLOOR IS IMPORTANT.
    return np.concatenate([temp[:,0],temp[:,1]])

cdef DecompositionFFT(np.ndarray[np.uint32_t,ndim = 2] trlwe,params):
    cdef np.ndarray[np.int32_t,ndim = 2] decvec = np.int32(Decomposition(trlwe,params))
    cdef int i
    return np.array([TwistFFT(decvec[i],params.twist) for i in range(2 * params.l)])

cdef trgswSymEncrypt(p,float alpha, h, key, twist):
    l = len(h)
    c = np.vstack([[trlweSymEncrypt(np.zeros(len(key)),alpha,key,twist)] for i in range(2*l)])
    muh = dtot32(np.outer(h,p))
    c[:l,0] += muh
    c[l:,1] += muh
    return c

cpdef trgswfftSymEncrypt(p, alpha:float, h, key, twist):
    trgsw = np.int32(trgswSymEncrypt(p, alpha, h, key, twist))
    return np.array([np.array([TwistFFT(trgsw[i][j],twist) for j in range(2)]) for i in range(2 * len(h))])

cpdef trgswfftExternalProduct(np.ndarray[np.complex128_t,ndim = 3] trgswfft,np.ndarray[np.uint32_t,ndim = 2] trlwe,params):
    cdef np.ndarray[np.complex128_t,ndim = 2] decvecfft = DecompositionFFT(trlwe,params)
    # if l is small enough, adding before IFFT doesn't make much noise and reduce number of IFFT which is a very heavy function.
    return np.array([np.uint32(np.round(TwistIFFT(np.sum([np.multiply(decvecfft[i], trgswfft[i][0]) for i in range(2 * params.l)],axis = 0),params.twist))%2**32),np.uint32(np.round(TwistIFFT(np.sum([np.multiply(decvecfft[i], trgswfft[i][1]) for i in range(2 * params.l)], axis = 0),params.twist))%2**32)],dtype = np.uint32)

#These are not optimized functions. Just for making reader easier to understand the algorithm.
#def trgswExternalProduct(g,r,params):
#    cdef np.ndarray[np.uint32_t,ndim = 2] decvec = Decomposition(r,params)
#    return np.array([np.sum([PolyMul(decvec[i], g[i][0],params.twist) for i in range(2 * params.l)],axis = 0),np.sum([PolyMul(decvec[i], g[i][1],params.twist) for i in range(2 * params.l)], axis = 0)],dtype = np.uint32)