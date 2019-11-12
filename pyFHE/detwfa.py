from .trgsw import trgswfftExternalProduct, trgswfftExternalProductlvl2
from .mulfft import TwistFFT
import numpy as np

def CMUXFFT(CFFT, d1, d0,params,fft,ifft):
    return trgswfftExternalProduct(CFFT,d1-d0,params,fft,ifft)+d0

def CMUXFFTlvl2(CFFT, d1, d0,params,fft,ifft):
    return trgswfftExternalProductlvl2(CFFT,d1-d0,params,fft,ifft)+d0

#These are not optimized functions. Just for making reader easier to understand the algorithm.
# def CMUX(C,d1,d0,params,fft,ifft):
#     #return trgswExternalProdcut(C,d1-d0,params)+d0
#     return trgswfftExternalProduct(TwistFFT(C,params.twist,fft),d1-d0,params,fft,ifft)+d0