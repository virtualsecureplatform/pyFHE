import numpy as np
from .trlwe import trlweSymEncrypt
from .mulfft import PolyMul,TwistFFT,TwistIFFT
from .utils import dtot32

#Gadget Decomposition.
def Decomposition(trlwe,params):
    temp = np.uint32(np.floor(np.multiply.outer(params.decb,trlwe + params.offset)%params.Bg) - params.Bg/2) #DOING FLOOR IS IMPORTANT.
    return np.concatenate([temp[:,0],temp[:,1]])

def Decompositionlvl2(trlwe,params):
    temp = np.uint64(np.floor(np.multiply.outer(params.decblvl2,trlwe + params.offsetlvl2)%params.Bgbar) - params.Bgbar/2) #DOING FLOOR IS IMPORTANT.
    return np.concatenate([temp[:,0],temp[:,1]])

def DecompositionFFT(r,params,fft):
    decvec = Decomposition(r,params)
    return np.array([TwistFFT(np.int32(decvec[i]),params.twist,fft) for i in range(2 * params.l)])

def DecompositionFFTlvl2(r,params,fft):
    decvec = Decompositionlvl2(r,params)
    return np.array([TwistFFT(np.int64(decvec[i]),params.twist,fft) for i in range(2 * params.lbar)])

def trgswSymEncrypt(p, alpha:float, h, key, twist, fft, ifft):
    l = len(h)
    c = np.vstack([[trlweSymEncrypt(np.zeros(len(key)),alpha,key,twist, fft ,ifft)] for i in range(2*l)])
    muh = dtot32(np.outer(h,p))
    c[:l,0] += muh
    c[l:,1] += muh
    return c

def trgswfftSymEncrypt(p, alpha:float, h, key, twist, fft, ifft):
    trgsw = np.int32(trgswSymEncrypt(p, alpha, h, key, twist,fft,ifft))
    return np.array([np.array([TwistFFT(trgsw[i][j],twist,fft) for j in range(2)]) for i in range(2 * len(h))])

def trgswfftExternalProduct(trgswfft,trlwe,params,fft,ifft):
    decvecfft = DecompositionFFT(trlwe,params,fft)
    # if l is small enough, adding before IFFT doesn't make much noise and reduce number of IFFT which is a very heavy function.
    return np.array([np.uint32(np.round(TwistIFFT(np.sum([np.multiply(decvecfft[i], trgswfft[i][0]) for i in range(2 * params.l)],axis = 0),params.twist, ifft))%2**32),np.uint32(np.round(TwistIFFT(np.sum([np.multiply(decvecfft[i], trgswfft[i][1]) for i in range(2 * params.l)], axis = 0),params.twist, ifft))%2**32)],dtype = np.uint32)

def trgswfftExternalProductlvl2(trgswfft,trlwe,params,fft,ifft):
    decvecfft = DecompositionFFT(trlwe,params,fft)
    # if l is small enough, adding before IFFT doesn't make much noise and reduce number of IFFT which is a very heavy function.
    return np.array([np.uint64(np.round(TwistIFFT(np.sum([np.multiply(decvecfft[i], trgswfft[i][0]) for i in range(2 * params.lbar)],axis = 0),params.twistlvl2, ifft))%2**64),np.uint64(np.round(TwistIFFT(np.sum([np.multiply(decvecfft[i], trgswfft[i][1]) for i in range(2 * params.lbar)], axis = 0),params.twistlvl2, ifft))%2**64)],dtype = np.uint64)

#These are not optimized functions. Just for making reader easier to understand the algorithm.
# def trgswExternalProduct(g,r,params):
#     decvec = Decomposition(r,params)
#     return np.array([np.sum([PolyMul(decvec[i], g[i][0],params.twist) for i in range(2 * params.l)],axis = 0),np.sum([PolyMul(decvec[i], g[i][1],params.twist) for i in range(2 * params.l)], axis = 0)],dtype = np.uint32)