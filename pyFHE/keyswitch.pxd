cimport numpy as np
from .key cimport CloudKey

cdef np.ndarray[np.uint32_t] IdentityKeySwitch(np.ndarray[np.uint32_t] tlwe,CloudKey ck)