import numpy as np
from .mulfft import TwistGen

class lweKey:
    def __init__(self,n:int, N:int, l:int, Bg:int):
        self.tlwe = np.random.randint(2,size = n,dtype = np.uint32)
        self.trlwe = np.random.randint(2,size = N, dtype = np.uint32)

class CloudKey:
    def __init__(self):
        self.KS = None

class lweParams:
    def __init__(self,n:int,alpha:float,N:int,l:int,Bg:int,bkalpha:float):
        self.n = n
        self.alpha = alpha
        self.N = N
        self.l = l
        self.Bg = Bg
        self.bkalpha = bkalpha
        self.h = np.array([Bg**(-(i+1)) for i in range(l)],dtype = np.double)
        self.offset = np.uint32(Bg/2 * np.sum(2**32 * self.h))
        self.decb = np.array([2**(-32) * Bg**(i+1) for i in range(l)], dtype = np.double)
        self.twist = TwistGen(N)

class SecretKey:
    def __init__(self,n:int,alpha:float,N:int,l:int,Bg:int,bkalpha:float): #Modify this to change parameter
        self.params = lweParams(n,alpha,N,l,Bg,bkalpha)
        self.key = lweKey(n,N,l,Bg)