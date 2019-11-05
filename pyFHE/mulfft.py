#from pyfftw import FFTW
import numpy as np

#Reference https://math.stackexchange.com/questions/1435448/negacyclic-fft-multiplication

def TwistGen(N):
    return np.array([np.exp(1j*k*np.pi/N) for k in range(N//2)])

def TwistFFT(a, twist, fft):
    Ns2 = len(twist)
    b = np.double(a)
    return fft(np.multiply((b[:Ns2]+1j*b[Ns2:2*Ns2]),twist))

def TwistIFFT(a, twist, ifft):
    b = np.multiply(ifft(a),np.conjugate(twist))
    return np.append(np.real(b),np.imag(b))

def PolyMul(a, b, twist, fft, ifft): #a or b in R and other in T
    return np.uint32(np.round(TwistIFFT(np.multiply(TwistFFT(np.int32(a),twist,fft),TwistFFT(np.int32(b),twist,fft)),twist, ifft))%2**32)
