from .utils import dtot32
import numpy as np

# Reference https://math.stackexchange.com/questions/1435448/negacyclic-fft-multiplication

def TwistGen(N):
    return np.array([np.exp(1j * k * np.pi / N) for k in range(N // 2)])

def TwistFFT(a, twist, dim=1):
    Ns2 = len(twist)
    b = np.double(a)
    # https://stackoverflow.com/questions/2598734/numpy-creating-a-complex-array-from-2-real-ones
    if dim == 1:
        t = np.empty(Ns2, dtype=np.complex128)
        t.real = b[:Ns2]
        t.imag = b[Ns2 : 2 * Ns2]
        t *= twist
        return np.fft.fft(t)
    elif dim == 2:
        t = np.empty((b.shape[0], Ns2), dtype=np.complex128)
        t.real = b[:, :Ns2]
        t.imag = b[:, Ns2 : 2 * Ns2]
        t *= twist
        return np.fft.fft(t,axis=1)

def TwistIFFT(a, twist, axis=None):
    b = np.multiply(np.fft.ifft(a, axis=(axis or -1)), np.conjugate(twist))
    return np.append(np.real(b), np.imag(b), axis=axis)

def PolyMul(a, b, twist):  # a or b in R and other in T
    return np.uint32(
        np.round(
            TwistIFFT(
                np.multiply(TwistFFT(np.int32(a), twist), TwistFFT(np.int32(b), twist)),
                twist,
            )
        )
        % 2 ** 32
    )
