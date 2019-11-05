cimport numpy as np

cpdef np.ndarray[np.complex128_t] TwistFFT(np.ndarray[np.int32_t], np.ndarray[np.complex128_t])
cpdef np.ndarray[np.uint32_t] TwistIFFT(np.ndarray[np.complex128_t], np.ndarray[np.complex128_t])
cpdef np.ndarray[np.uint32_t] PolyMul(np.ndarray[np.uint32_t],np.ndarray[np.uint32_t], np.ndarray[np.complex128_t])