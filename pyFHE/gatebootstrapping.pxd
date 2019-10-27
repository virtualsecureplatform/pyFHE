from .key cimport CloudKey
cimport numpy as np

cdef np.ndarray[np.uint32_t] GateBootstrappingTLWE2TLWEFFT(np.ndarray[np.uint32_t],CloudKey)
cdef np.ndarray[np.uint32_t] GateBootstrappingFFT(np.ndarray[np.uint32_t],CloudKey)