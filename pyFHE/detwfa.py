from .trgsw import trgswfftExternalProduct, trgswfftExternalProductlvl2
from .key import lweParams
from .mulfft import TwistFFT
import numpy as np


def CMUXFFT(CFFT, d1, d0, params: lweParams):
    return trgswfftExternalProduct(CFFT, d1 - d0, params) + d0

def CMUXFFTlvl2(CFFT, d1, d0, params: lweParams):
    return trgswfftExternalProductlvl2(CFFT, d1 - d0, params) + d0


# def CMUX(C, d1, d0, params: lweParams):
#     # return trgswExternalProdcut(C,d1-d0,params)+d0
#     return trgswfftExternalProduct(TwistFFT(C, params.twist), d1 - d0, params) + d0