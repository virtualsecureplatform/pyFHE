cimport numpy as np

cdef np.ndarray[np.uint32_t] dtot32array(np.ndarray[np.float64_t]d)
cdef np.uint32_t dtot32(np.float64_t d)
cdef np.ndarray[np.uint32_t] gaussian32(np.ndarray[np.uint32_t],float)