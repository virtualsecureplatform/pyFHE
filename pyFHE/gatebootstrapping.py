from .detwfa import CMUXFFT
from .keyswitch import IdentityKeySwitch
from .trlwe import SampleExtractIndex, trlweSymEncrypt, trlweSymDecrypt
from .key import lweParams, CloudKey
from .utils import dtot32
import numpy as np


def PolynomialMulByXai(poly, a, N):
    a = a.item()
    if a == 0:
        return poly
    elif a < N:
        l0 = -poly[N - a : N]
        l1 = poly[0 : N - a]
        t = np.concatenate([l0, l1])
        return np.uint32(t)
    else:
        aa = a - N
        l0 = poly[N - aa : N]
        l1 = -poly[0 : N - aa]
        t = np.concatenate([l0, l1])
        return np.uint32(t)

def PolynomialMulByXailvl2(poly,a,N):
    a = a.item()
    if a == 0:
        return poly
    elif a < N:
        l0 = -poly[N - a : N]
        l1 = poly[0 : N - a]
        t = np.concatenate([l0, l1])
        return np.uint64(t)
    else:
        aa = a - N
        l0 = poly[N - aa : N]
        l1 = -poly[0 : N - aa]
        t = np.concatenate([l0, l1])
        return np.uint64(t)

def BlindRotateFFT(
    bkfft, t: np.ndarray, r: np.ndarray, params: lweParams
):  # t is TLWE and r is TRLWE polynomial to rotate and t is TLWE
    bara = np.uint32(np.round(np.double(t) * (2 ** -32 * 2 * params.N)))
    acc = np.array(
        [
            PolynomialMulByXai(r[0], 2 * params.N - bara[-1], params.N),
            PolynomialMulByXai(r[1], 2 * params.N - bara[-1], params.N),
        ]
    )
    for i in range(params.n):
        if bara[i] == 0:
            continue
        acc = CMUXFFT(
            bkfft[i],
            np.array(
                [
                    PolynomialMulByXai(acc[0], bara[i], params.N),
                    PolynomialMulByXai(acc[1], bara[i], params.N),
                ]
            ),
            acc,
            params,
        )
    return acc

def BlindRotateFFTlvl2(
    bkfft, tlwe: np.ndarray, trlwe: np.ndarray, params: lweParams
):
    bara = np.uint32(np.round(np.double(t) * (2 ** -32 * 2 * params.N)))
    acc = np.array(
        [
            PolynomialMulByXailvl2(trlwe[0], 2 * params.nbar - bara[-1], params.N),
            PolynomialMulByXailvl2(trlwe[1], 2 * params.nbar - bara[-1], params.N),
        ]
    )
    for i in range(params.n):
        if bara[i] == 0:
            continue
        acc = CMUXFFT(
            bkfft[i],
            np.array(
                [
                    PolynomialMulByXailvl2(acc[0], bara[i], params.N),
                    PolynomialMulByXailvl2(acc[1], bara[i], params.N),
                ]
            ),
            acc,
            params,
        )
    return acc

def GateBootstrappingTLWE2TLWEFFT(t, ck: CloudKey):
    testvec = np.array(
        [np.zeros(ck.params.N), np.full(ck.params.N, dtot32(2 ** -3))]
    )  # This is same as original implemetation of TFHE.
    return SampleExtractIndex(BlindRotateFFT(ck.bkfft, t, testvec, ck.params), 0)


def GateBootstrappingFFT(tlwe, ck:CloudKey):
    return IdentityKeySwitch(GateBootstrappingTLWE2TLWEFFT(tlwe, ck), ck)


# These are not optimized functions. Just for making reader easier to understand the algorithm.
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
