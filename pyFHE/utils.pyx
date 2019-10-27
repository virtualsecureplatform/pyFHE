import numpy as np
cimport numpy as np

cdef np.ndarray[np.uint32_t] dtot32array(np.ndarray[np.float64_t]d):
    return np.uint32(np.round((d%1)*(2**32)))

cdef np.uint32_t dtot32(np.float64_t d):
    return np.uint32(np.round((d%1)*(2**32)))

cdef np.ndarray[np.uint32_t] gaussian32(np.ndarray[np.uint32_t] mu,float alpha):
    return dtot32array(np.random.normal(0,alpha,len(mu))) + mu