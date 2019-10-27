cimport numpy as np

cdef np.ndarray[np.complex128_t] TwistGen(int)
cdef np.ndarray[np.complex128_t] TwistFFT(np.ndarray[np.int32_t], np.complex128_t[:])
cdef np.ndarray[np.uint32_t] TwistIFFT(np.ndarray[np.complex128_t], np.complex128_t[:])
cdef np.ndarray[np.uint32_t] PolyMul(np.ndarray[np.uint32_t],np.ndarray[np.uint32_t], np.complex128_t[:])