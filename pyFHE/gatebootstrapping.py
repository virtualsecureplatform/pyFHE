from .detwfa import CMUX
from .trlwe import SampleExtractIndex,trlweSymEncrypt,trlweSymDecrypt
from .key import lweParams
from .utils import dtot32
import numpy as np

def PolynomialMulByXai(poly,a,N):
    if(a==0):
        return poly
    elif(a < N):
        return np.uint32(np.concatenate([[-poly[i - a + N] for i in range(a)],[poly[i] for i in range(N - a)]]))
    else :
        aa = a-N
        return np.uint32(np.concatenate([[poly[i - aa + N] for i in range(aa)],[-poly[i] for i in range(N - aa)]]))

def BlindRotate(bk,t:np.ndarray, r:np.ndarray,params:lweParams):#t is TLWE and r is TRLWE polynomial to rotate and t is TLWE
    bara = np.uint32(np.round(np.double(t) * (2**-32 * 2 * params.N)))
    acc = np.array([PolynomialMulByXai(r[0],2 * params.N - bara[-1],params.N),PolynomialMulByXai(r[1],2 * params.N - bara[-1],params.N)])
    for i in range(params.n):
        if bara[i] == 0:
            continue 
        acc = CMUX(bk[i],np.array([PolynomialMulByXai(acc[0],bara[i],params.N),PolynomialMulByXai(acc[1],bara[i],params.N)]),acc,params)
    return acc

def GateBootstrappingTLWE2TLWE(t,bk,params,key):
    testvec = np.array([np.zeros(params.N),np.full(params.N,dtot32(2**-3))]) #This is same as original implemetation of TFHE.
    print(trlweSymDecrypt(BlindRotate(bk,t,testvec,params),key,params.twist))
    return SampleExtractIndex(BlindRotate(bk,t,testvec,params),0)