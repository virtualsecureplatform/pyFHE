from .trgsw import trgswfftExternalProduct
from .key import lweParams
from .mulfft import TwistFFT
import numpy as np
cimport numpy as np

cpdef CMUXFFT(np.ndarray[np.complex128_t,ndim = 3] CFFT,np.ndarray[np.uint32_t, ndim = 2] d1,np.ndarray[np.uint32_t, ndim = 2] d0,params):
    return trgswfftExternalProduct(CFFT,d1-d0,params)+d0

cpdef CMUX(C,d1,d0,params:lweParams):
    #return trgswExternalProdcut(C,d1-d0,params)+d0
    return trgswfftExternalProduct(TwistFFT(C,params.twist),d1-d0,params)+d0