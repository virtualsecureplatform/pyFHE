import numpy as np
cimport numpy as np
from .mulfft cimport TwistGen

cdef class lweParams:
    def __init__(self,n,alpha,N,l,Bgbit,bkalpha,t,basebit,ksalpha):
        self.n = n
        self.alpha = alpha
        self.N = N
        self.l = l
        self.Bg = 2 ** Bgbit
        self.Bgbit = Bgbit
        self.bkalpha = bkalpha
        self.h = np.array([self.Bg**(-(i+1)) for i in range(l)])
        self.offset = np.uint32(self.Bg/2 * np.sum(2**32 * np.asarray(self.h)))
        self.decb = np.array([2.0**(-32) * self.Bg**(i+1) for i in range(l)])
        self.twist = TwistGen(N)
        self.t = t
        self.basebit = basebit
        self.ksalpha = ksalpha