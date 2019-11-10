cimport numpy as np

cpdef np.ndarray[np.uint32_t] IdentityKeySwitch(np.ndarray[np.uint32_t] tlwe,np.ndarray[np.uint32_t,ndim=4] ksk, ck)