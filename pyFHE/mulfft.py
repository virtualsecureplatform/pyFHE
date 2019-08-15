import numpy as np
from .utils import dtot32

#Reference https://math.stackexchange.com/questions/1435448/negacyclic-fft-multiplication

def TwistGen(N):
    return np.array([np.exp(1j*k*np.pi/N) for k in range(N//2)])

def TwistFFT(a,twist):
    Ns2 = len(twist)
    b = np.array(a,dtype = np.double)
    return np.fft.fft(np.multiply((b[:Ns2]+1j*b[Ns2:2*Ns2]),twist))

def TwistIFFT(a,twist):
    b = np.multiply(np.fft.ifft(a),np.conjugate(twist))
    return np.append(np.real(b),np.imag(b))

def PolyMul(a,b,twist):
    return np.uint32(TwistIFFT(np.multiply(TwistFFT(a,twist),TwistFFT(b,twist)),twist) % (2**32))
