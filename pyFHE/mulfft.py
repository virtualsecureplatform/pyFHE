from .utils import dtot32
import numpy as np
from numba import jit

#Reference https://math.stackexchange.com/questions/1435448/negacyclic-fft-multiplication

def TwistGen(N):
    return np.array([np.exp(1j*k*np.pi/N) for k in range(N//2)])

def TwistFFT(a,twist):
    Ns2 = len(twist)
    b = np.double(a)
    return np.fft.fft(np.multiply((b[:Ns2]+1j*b[Ns2:2*Ns2]),twist))

def TwistIFFT(a,twist):
    b = np.multiply(np.fft.ifft(a),np.conjugate(twist))
    return np.append(np.real(b),np.imag(b))

def PolyMul(a, b, twist): #a or b in R and other in T
    return np.uint32(np.round(TwistIFFT(np.multiply(TwistFFT(np.int32(a),twist),TwistFFT(np.int32(b),twist)),twist))%2**32)
