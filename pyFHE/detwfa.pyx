from .trgsw cimport trgswfftExternalProduct
from .lweparams cimport lweParams
from .mulfft cimport TwistFFT
import numpy as np
cimport numpy as np

cdef np.ndarray[np.uint32_t, ndim = 2] CMUXFFT(np.ndarray[np.complex128_t,ndim = 3] CFFT,np.ndarray[np.uint32_t, ndim = 2] d1,np.ndarray[np.uint32_t, ndim = 2] d0,lweParams params):
    return trgswfftExternalProduct(CFFT,d1-d0,params)+d0

cdef CMUX(C,d1,d0,lweParams params):
    #return trgswExternalProdcut(C,d1-d0,params)+d0
    return trgswfftExternalProduct(TwistFFT(C,params.twist),d1-d0,params)+d0