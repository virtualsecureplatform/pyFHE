import numpy as np
from .mulfft import TwistGen

class lweKey:
    def __init__(self,n:int,N:int):
        self.tlwe = np.random.randint(2,size = n,dtype = np.uint32)
        self.trlwe = np.random.randint(2,size = N, dtype = np.uint32)
        self.twist = TwistGen(N)

class lweParams:
    def __init__(self,n:int,alpha:float,N:int,l:int,Bg:int,bkalpha:float):
        self.n = n
        self.alpha = alpha
        self.N = N
        self.l = l
        self.Bg = Bg
        self.bkalpha = bkalpha

class SecretKey:
    def __init__(self,n:int,alpha:float,N:int,l:int,Bg:int,bkalpha:float): #Modify this to change parameter
        self.params = lweParams(n,alpha,N,l,Bg,bkalpha)
        self.key = lweKey(n,N)