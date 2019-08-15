from .detwfa import CMUX
from .trlwe import SampleExtractIndex,trlweSymEncrypt
from .key import lweParams
import numpy as np

mu = 2**-3

def PolynomialMulByXai(poly,a,N):
    if(a==0):
        return poly
    elif(a < N):
        return np.concatenate([[-poly[i - a + N] for i in range(a)],[poly[i] for i in range(N - a)]])
    else :
        aa = a-N
        return np.concatenate([[poly[i - aa + N] for i in range(aa)],[-poly[i] for i in range(N - aa)]])

def BlindRotate(bk,t, r:np.ndarray,params:lweParams):#t is TLWE and r is TRLWE polynomial to rotate and t is TLWE
    bara = np.uint32(np.round(t * (2**-32 * 2 * params.N)))
    acc = PolynomialMulByXai(r,2 * params.N - bara[-1],params.N)
    for i in range(params.n):
        acc += CMUX(bk[i],np.array([PolynomialMulByXai(acc[0],bara[i],params.N),PolynomialMulByXai(acc[1],bara[i],params.N)]),acc,params)
    return acc

def GateBootstrappingTLWE2TLWE(bk,t,params):
    testvec = np.full(params.N,mu)
    return SampleExtractIndex(BlindRotate(bk,t,np.concatenate([[np.zeros(params.N)],[testvec]]),params),0)