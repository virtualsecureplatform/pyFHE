cimport numpy as np
from .lweparams cimport lweParams

cdef np.ndarray[np.uint32_t, ndim = 2] CMUXFFT(np.ndarray[np.complex128_t,ndim = 3],np.ndarray[np.uint32_t, ndim = 2],np.ndarray[np.uint32_t, ndim = 2],lweParams)