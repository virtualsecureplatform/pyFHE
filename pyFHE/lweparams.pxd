cimport numpy as np

cdef class lweParams:
    cdef public int n,N,l,Bg,Bgbit,t,basebit
    cdef public double alpha,bkalpha,ksalpha
    cdef public np.uint32_t offset
    cdef public np.float64_t[:] h,decb
    cdef public np.complex128_t[:] twist