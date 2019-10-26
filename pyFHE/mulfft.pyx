from .utils import dtot32

from pyfftw import FFTW
import numpy as np
cimport numpy as np

#Reference https://math.stackexchange.com/questions/1435448/negacyclic-fft-multiplication

def TwistGen(int N):
    return np.array([np.exp(1j*k*np.pi/N) for k in range(N//2)])

cpdef TwistFFT(np.ndarray[np.int32_t] a,np.ndarray[np.complex128_t] twist):
    cdef int Ns2 = len(twist)
    cdef np.ndarray[np.double_t] b = np.double(a)
    return np.fft.fft(np.multiply((b[:Ns2]+1j*b[Ns2:2*Ns2]),twist))

cpdef TwistIFFT(np.ndarray[np.complex128_t] a,np.ndarray[np.complex128_t] twist):
    cdef np.ndarray[np.complex128_t] b = np.multiply(np.fft.ifft(a),np.conjugate(twist))
    return np.append(np.real(b),np.imag(b))

cpdef PolyMul(np.ndarray[np.uint32_t,ndim=1] a,np.ndarray[np.uint32_t,ndim=1] b,np.ndarray[np.complex128_t,ndim=1] twist): #a or b in R and other in T
    return np.uint32(np.round(TwistIFFT(np.multiply(TwistFFT(np.int32(a),twist),TwistFFT(np.int32(b),twist)),twist))%2**32)
