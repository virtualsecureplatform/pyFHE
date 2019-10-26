from .detwfa import CMUXFFT
from .keyswitch import IdentityKeySwitch
from .trlwe import SampleExtractIndex,trlweSymEncrypt,trlweSymDecrypt
from .key import lweParams,CloudKey
from .utils import dtot32
import numpy as np
cimport numpy as np

cpdef PolynomialMulByXai(np.ndarray[np.uint32_t] poly,int a,int N):
    cdef int aa
    cdef int i
    if(a==0 or a == 2*N):
        return poly
    elif(a < N):
        return np.uint32(np.concatenate([[-poly[i - a + N] for i in range(a)],[poly[i - a] for i in range(a,N)]]))
    else :
        aa = a - N
        return np.uint32(np.concatenate([[poly[i - aa + N] for i in range(aa)],[-poly[i - aa] for i in range(aa,N)]]))

cpdef BlindRotateFFT(np.ndarray[np.complex128_t, ndim = 4] bkfft,np.ndarray[np.uint32_t] tlwe,np.ndarray[np.uint32_t,ndim = 2] trlwe,params:lweParams):#t is TLWE and r is TRLWE polynomial to rotate and t is TLWE
    cdef np.ndarray[np.uint32_t] bara = np.uint32(np.round(np.double(tlwe) * (np.double(2.0**-32) * np.double(2 * params.N))))
    cdef np.ndarray[np.uint32_t,ndim = 2] acc = np.array([PolynomialMulByXai(trlwe[0],2 * params.N - bara[-1],params.N),PolynomialMulByXai(trlwe[1],2 * params.N - bara[-1],params.N)])
    cdef int i
    for i in range(params.n):
        if bara[i] == 0:
            continue 
        acc = CMUXFFT(bkfft[i],np.array([PolynomialMulByXai(acc[0],bara[i],params.N),PolynomialMulByXai(acc[1],bara[i],params.N)]),acc,params)
    return acc

cpdef GateBootstrappingTLWE2TLWEFFT(np.ndarray[np.uint32_t] tlwe,ck:CloudKey):
    cdef np.ndarray[np.uint32_t,ndim = 2] testvec = np.uint32(np.array([np.zeros(ck.params.N),np.full(ck.params.N,dtot32(2.0**-3))])) #This is same as original implemetation of TFHE.
    return SampleExtractIndex(BlindRotateFFT(ck.bkfft,tlwe,testvec,ck.params),0)

cpdef GateBootstrappingFFT(np.ndarray[np.uint32_t] tlwe,ck):
    return IdentityKeySwitch(GateBootstrappingTLWE2TLWEFFT(tlwe,ck),ck)

#These are not optimized functions. Just for making reader easier to understand the algorithm.
# def BlindRotate(bk,t:np.ndarray, r:np.ndarray,params:lweParams):#t is TLWE and r is TRLWE polynomial to rotate and t is TLWE
#     bara = np.uint32(np.round(np.double(t) * (2**-32 * 2 * params.N)))
#     acc = np.array([PolynomialMulByXai(r[0],2 * params.N - bara[-1],params.N),PolynomialMulByXai(r[1],2 * params.N - bara[-1],params.N)])
#     for i in range(params.n):
#         if bara[i] == 0:
#             continue 
#         acc = CMUX(bk[i],np.array([PolynomialMulByXai(acc[0],bara[i],params.N),PolynomialMulByXai(acc[1],bara[i],params.N)]),acc,params)
#     return acc

# def GateBootstrappingTLWE2TLWE(t,bk,params,key):
#     testvec = np.array([np.zeros(params.N),np.full(params.N,dtot32(2**-3))]) #This is same as original implemetation of TFHE.
#     return SampleExtractIndex(BlindRotate(bk,t,testvec,params),0)