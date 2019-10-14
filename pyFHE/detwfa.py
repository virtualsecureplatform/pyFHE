from .trgsw import trgswfftExternalProdcut
from .key import lweParams
from .mulfft import TwistFFT
import numpy as np

def CMUXFFT(CFFT,d1,d0,params:lweParams):
    return trgswfftExternalProdcut(CFFT,d1-d0,params)+d0

def CMUX(C,d1,d0,params:lweParams):
    #return trgswExternalProdcut(C,d1-d0,params)+d0
    return trgswfftExternalProdcut(TwistFFT(C,params.twist),d1-d0,params)+d0