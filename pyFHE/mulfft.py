from .utils import dtot32
import numpy as np
import pyfftw

# Reference https://math.stackexchange.com/questions/1435448/negacyclic-fft-multiplication


def TwistGen(N):
    return np.array([np.exp(1j * k * np.pi / N) for k in range(N // 2)])

def TwistFFT(a, twist, fft, dim=1):
    Ns2 = len(twist)
    b = np.double(a)
    # https://stackoverflow.com/questions/2598734/numpy-creating-a-complex-array-from-2-real-ones
    if dim == 1:
        t = np.empty(Ns2, dtype=np.complex128)
        t.real = b[:Ns2]
        t.imag = b[Ns2 : 2 * Ns2]
        t *= twist
        return fft[dim-1](t)
    elif dim == 2:
        t = np.empty((b.shape[0], Ns2), dtype=np.complex128)
        t.real = b[:, :Ns2]
        t.imag = b[:, Ns2 : 2 * Ns2]
        t *= twist
        return fft[dim-1](t)

def TwistIFFT(a, twist, ifft, axis=None):
    if axis == 1:
        b = np.multiply(ifft[1](a), np.conjugate(twist))
    else:
        b = np.multiply(ifft[0](a), np.conjugate(twist))
    return np.append(np.real(b), np.imag(b), axis=axis)


def PolyMul(a, b, twist, fft, ifft):  # a or b in R and other in T
    return np.uint32(
        np.round(
            TwistIFFT(
                np.multiply(TwistFFT(np.int32(a), twist, fft), TwistFFT(np.int32(b), twist, fft)),
                twist,
                ifft
            )
        )
        % 2 ** 32
    )
