from .utils import dtot32
import numpy as np
import sympy
import pyfftw

pyfftw.interfaces.cache.enable()

# Reference https://math.stackexchange.com/questions/1435448/negacyclic-fft-multiplication

def TwistGen(N):
    return np.array([np.exp(1j * k * np.pi / N) for k in range(N // 2)])

def TwistGenLong(N):
    return np.array([np.exp(1j * np.float128(k) * np.pi / N) for k in range(N // 2)])

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

#To compute 64bit Torus multiplication, long double is needed.
def TwistFFTlong(a, twist, dim =1):
    Ns2 = len(twist)
    b = np.float128(a)
    # https://stackoverflow.com/questions/2598734/numpy-creating-a-complex-array-from-2-real-ones
    if dim == 1:
        t = np.empty(Ns2, dtype=np.complex256)
        t.real = b[:Ns2]
        t.imag = b[Ns2 : 2 * Ns2]
        t *= twist
        return pyfftw.interfaces.numpy_fft.fft(t)
    elif dim == 2:
        t = np.empty((b.shape[0], Ns2), dtype=np.complex256)
        t.real = b[:, :Ns2]
        t.imag = b[:, Ns2 : 2 * Ns2]
        t *= twist
        return pyfftw.interfaces.numpy_fft.fft(t,axis=1)

def TwistIFFT(a, twist, axis=None):
    b = np.multiply(np.fft.ifft(a, axis=(axis or -1)), np.conjugate(twist))
    return np.append(np.real(b), np.imag(b), axis=axis)

def TwistIFFTlong(a, twist, axis=None):
    b = np.multiply(pyfftw.interfaces.numpy_fft.ifft(a, axis=(axis or -1)), np.conjugate(twist))
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

def PolyMullvl2Long(a,b,twist):
    return np.uint64(
        np.round(
            TwistIFFTlong(
                np.multiply(TwistFFTlong(np.int64(a), twist), TwistFFTlong(np.int64(b), twist)),
                twist,
            )
        )%np.float128(2)**64
    )


def PolyMullvl2(a, b, twist):  # a or b in R and other in T
    return np.uint64(
        np.round(
            TwistIFFT(
                np.multiply(TwistFFT(np.int64(a), twist), TwistFFT(np.int64(b), twist)),
                twist,
            )
        )
        % 2 ** 64
    )

# These are not optimized functions. Just for making reader easier to understand the algorithm.
# def PolyMullvl2Ideal(a,b):
#     x = sympy.symbols("x")
#     N = len(a)
#     ab = np.uint64(np.flip(np.array((sympy.Poly(np.flip(a),x) * sympy.Poly(np.flip(b),x)).all_coeffs())%2**64))
#     return ab[:N] - np.append(ab[N:], np.zeros(2 * N - len(ab),dtype=np.uint64))