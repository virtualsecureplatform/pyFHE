cimport numpy as np
from .lweparams cimport lweParams

cdef class CloudKey:
    cdef np.uint32_t[:,:,:,:] ksk
    cdef np.complex128_t[:,:,:,:] bkfft
    cdef lweParams params