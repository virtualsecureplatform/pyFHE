from .trgsw import trgswfftExternalProduct
from .mulfft import TwistFFT
import numpy as np

def CMUXFFT(CFFT, d1, d0,params):
    return trgswfftExternalProduct(CFFT,d1-d0,params)+d0

def CMUX(C,d1,d0,params):
    #return trgswExternalProdcut(C,d1-d0,params)+d0
    return trgswfftExternalProduct(TwistFFT(C,params.twist),d1-d0,params)+d0