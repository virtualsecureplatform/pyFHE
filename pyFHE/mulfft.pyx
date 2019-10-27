#from pyfftw import FFTW
import numpy as np
cimport numpy as np

#Reference https://math.stackexchange.com/questions/1435448/negacyclic-fft-multiplication

cdef np.ndarray[np.complex128_t] TwistGen(int N):
    return np.array([np.exp(1j*k*np.pi/N) for k in range(N//2)])

cdef np.ndarray[np.complex128_t] TwistFFT(np.ndarray[np.int32_t] a,np.complex128_t[:] twist):
    cdef int Ns2 = len(twist)
    cdef np.ndarray[np.double_t] b = np.double(a)
    return np.fft.fft(np.multiply((b[:Ns2]+1j*b[Ns2:2*Ns2]),np.array(twist)))

cdef np.ndarray[np.uint32_t] TwistIFFT(np.ndarray[np.complex128_t] a,np.complex128_t[:] twist):
    cdef np.ndarray[np.complex128_t] b = np.multiply(np.fft.ifft(a),np.conjugate(np.array(twist)))
    return np.append(np.real(b),np.imag(b))

cdef np.ndarray[np.uint32_t] PolyMul(np.ndarray[np.uint32_t,ndim=1] a,np.ndarray[np.uint32_t,ndim=1] b,np.complex128_t[:] twist): #a or b in R and other in T
    return np.uint32(np.round(TwistIFFT(np.multiply(TwistFFT(np.int32(a),twist),TwistFFT(np.int32(b),twist)),twist))%2**32)
