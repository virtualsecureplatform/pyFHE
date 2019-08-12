import numpy as np
from .mulfft import TwistGen

class lweKey:
    def __init__(self,n:int,N:int,k:int):
        self.tlwe = np.random.randint(2,size = n,dtype = np.int32)
        self.trlwe = np.array([np.random.randint(2,size = N, dtype = np.int32) for i in range(k)])
        self.twist = TwistGen(N)

class lweParams:
    def __init__(self,n:int,alpha:float,N:int,k:int,l:int,Bg:int,bkalpha:float):
        self.n = n
        self.alpha = alpha
        self.N = N
        self.k = k
        self.l = l
        self.Bg = Bg
        self.bkalpha = bkalpha

class SecretKey:
    def __init__(self,n:int,alpha:float,N:int,k:int,l:int,Bg:int,bkalpha:float): #Modify this to change parameter
        self.params = lweParams(n,alpha,N,k,l,Bg,bkalpha)
        self.key = lweKey(n,N,k)