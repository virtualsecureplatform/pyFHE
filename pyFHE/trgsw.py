import numpy as np
from .trlwe import trlweSymEncrypt,trlweSymEncryptlvl2, trlweSymDecryptlvl2
from .mulfft import PolyMul, TwistFFT, TwistIFFT, TwistFFTlong, TwistIFFTlong, PolyMullvl2Long, PolyMullvl2
from .utils import dtot32,dtot64

# Gadget Decomposition.
def Decomposition(trlwe, params):
    t = trlwe + params.offset
    t = np.array([t >> i for i in params.decbit])
    t &= params.Bg - 1
    t -= params.Bg // 2
    return np.concatenate([t[:, 0], t[:, 1]])

def Decompositionlvl2(trlwe, params):
    t = trlwe + params.offsetlvl2
    t = np.array([t >> i for i in params.decbitlvl2])
    t &= params.Bgbar - 1
    t -= params.Bgbar // 2
    return np.concatenate([t[:, 0], t[:, 1]])

def DecompositionFFT(r, params):
    decvec = Decomposition(r, params)
    return TwistFFT(np.int32(decvec), params.twist, dim=2)

def DecompositionFFTlvl2(r, params):
    decvec = Decompositionlvl2(r, params)
    return TwistFFTlong(np.int64(decvec), params.twistlvl2long, dim=2)

def trgswSymEncrypt(p, alpha: float, h, key, twist):
    l = len(h)
    c = np.vstack(
        [[trlweSymEncrypt(np.zeros(len(key)), alpha, key, twist)] for i in range(2 * l)]
    )
    muh = dtot32(np.outer(h, p))
    c[:l, 0] += muh
    c[l:, 1] += muh
    return c

def trgswSymEncryptlvl2(p, alpha: float, h, key, twistlong):
    l = len(h)
    c = np.vstack(
        [[trlweSymEncryptlvl2(np.zeros(len(key)), alpha, key, twistlong)] for i in range(2 * l)]
    )
    muh = dtot64(np.outer(h, p))
    c[:l, 0] += muh
    c[l:, 1] += muh
    return c

def trgswfftSymEncrypt(p, alpha: float, h, key, twist):
    trgsw = np.int32(trgswSymEncrypt(p, alpha, h, key, twist))
    return np.array(
        [
            np.array([TwistFFT(trgsw[i][j], twist) for j in range(2)])
            for i in range(2 * len(h))
        ]
    )

def trgswfftSymEncryptlvl2(p, alpha: float, h, key, twistlong):
    trgsw = np.int64(trgswSymEncryptlvl2(p, alpha, h, key, twistlong))
    return np.array(
        [
            np.array([TwistFFTlong(trgsw[i][j], twistlong) for j in range(2)])
            for i in range(2 * len(h))
        ]
    )

def trgswfftExternalProduct(trgswfft, trlwe, params):
    decvecfft = DecompositionFFT(trlwe, params)
    # if l is small enough, adding before IFFT doesn't make much noise and reduce number of IFFT which is a very heavy function.
    t = decvecfft.reshape(2*params.l, 1, params.N//2) * trgswfft
    t = t.sum(axis=0)
    t = TwistIFFT(t, params.twist, axis=1)
    t = np.uint32(t)
    return t

def trgswfftExternalProductlvl2(trgswfft, trlwe, params):
    decvecfft = DecompositionFFTlvl2(trlwe, params)
    # if l is small enough, adding before IFFT doesn't make much noise and reduce number of IFFT which is a very heavy function.
    t = decvecfft.reshape(2*params.lbar, 1, params.nbar//2) * trgswfft
    t = t.sum(axis=0)
    t = TwistIFFTlong(t, params.twistlvl2long, axis=1)
    t = np.uint64(t%np.float128(2.0)**64)
    return t

def trgswExternalProductlvl2(trgsw, trlwe, params):
    decvec = Decompositionlvl2(trlwe, params)
    return np.array(
        [
            np.sum(
                [
                    PolyMullvl2Long(decvec[i], trgsw[i][0], params.twistlvl2long)
                    for i in range(2 * params.lbar)
                ],
                axis=0,
            ),
            np.sum(
                [
                    PolyMullvl2Long(decvec[i], trgsw[i][1], params.twistlvl2long)
                    for i in range(2 * params.lbar)
                ],
                axis=0,
            ),
        ],
        dtype=np.uint64,
    )

# These are not optimized functions. Just for making reader easier to understand the algorithm.
# def trgswExternalProduct(g, r, params):
#     decvec = Decomposition(r, params)
#     return np.array(
#         [
#             np.sum(
#                 [
#                     PolyMul(decvec[i], g[i][0], params.twist)
#                     for i in range(2 * params.l)
#                 ],
#                 axis=0,
#             ),
#             np.sum(
#                 [
#                     PolyMul(decvec[i], g[i][1], params.twist)
#                     for i in range(2 * params.l)
#                 ],
#                 axis=0,
#             ),
#         ],
#         dtype=np.uint32,
#     )