from .key cimport CloudKey
from .lweparams cimport lweParams
import numpy as np
cimport numpy as np

cdef np.ndarray[np.uint32_t] IdentityKeySwitch(np.ndarray[np.uint32_t] tlwe,CloudKey ck):
    cdef np.ndarray[np.uint32_t] aibar = np.uint32(np.round(tlwe[:-1] * 2.0**(ck.params.basebit*ck.params.t -32)))
    cdef np.uint32_t mask = (1<<ck.params.basebit) - 1
    cdef int i,j
    return np.uint32(np.append(np.zeros(ck.params.n),tlwe[-1])) - np.sum([np.sum([ck.ksk[i][j][aibar[i]>>(ck.params.basebit*(ck.params.t-(j+1))) &mask] for j in range(ck.params.t)], axis = 0) for i in range(ck.params.N)],axis = 0)