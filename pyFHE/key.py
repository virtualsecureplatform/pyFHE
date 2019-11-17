import numpy as np
from secrets import randbits
from .mulfft import TwistGen
from .tlwe import tlweSymEncrypt
from .trgsw import trgswfftSymEncrypt

class lweKey:
    def __init__(self,n:int, N:int):
        self.tlwe = np.array([randbits(1) for i in range(n)],dtype = np.uint32)
        self.trlwe = np.array([randbits(1) for i in range(N)],dtype = np.uint32)

class lweParams:
    def __init__(self,n:int,alpha:float,N:int,l:int,Bgbit:int,bkalpha:float,t:int,basebit:int,ksalpha:float):
        self.n = n
        self.alpha = alpha
        self.N = N
        self.l = l
        self.Bg = 1 << Bgbit
        self.Bgbit = Bgbit
        self.bkalpha = bkalpha
        self.h = np.array([self.Bg**(-(i+1)) for i in range(l)],dtype = np.double)
        self.offset = np.uint32(self.Bg/2 * np.sum(2**32 * self.h))
        self.decb = np.array([(2**(-32)) * (self.Bg**(i+1)) for i in range(l)], dtype = np.double)
        self.twist = TwistGen(N)
        self.t = t
        self.basebit = basebit
        self.ksalpha = ksalpha

class SecretKey:
    def __init__(self,n:int,alpha:float,N:int,l:int,Bgbit:int,bkalpha:float,t:int,basebit:int,ksalpha:float): #Modify this to change parameter
        self.params = lweParams(n,alpha,N,l,Bgbit,bkalpha,t,basebit,ksalpha)
        self.key = lweKey(n,N)

class CloudKey:
    def __init__(self,sk:SecretKey):
        #if k, the decomposed part of the target of keyswitch function, is 0, the value is trivial.
        self.ksk = np.uint32(np.array([[np.concatenate([[np.zeros(sk.params.n +1)],[tlweSymEncrypt(sk.key.trlwe[i] * k * 2.0**(-(j+1)*sk.params.basebit),sk.params.ksalpha,sk.key.tlwe) for k in range(1,2**sk.params.basebit)]]) for j in range(sk.params.t)] for i in range(sk.params.N)]))
        self.bkfft = np.array([trgswfftSymEncrypt(np.uint32(np.concatenate([[sk.key.tlwe[i]],np.zeros(sk.params.N - 1)])),sk.params.bkalpha,sk.params.h,sk.key.trlwe,sk.params.twist) for i in range(sk.params.n)])
        self.params = sk.params