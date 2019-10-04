import numpy as np
from .trlwe import trlweSymEncrypt
from .mulfft import PolyMul
from .utils import dtot32

#Gadget Decomposition.
def Decomposition(r,params):
    temp = np.int32(np.round(np.multiply.outer(params.decb,r + params.offset)%params.Bg - params.Bg//2))
    return np.concatenate([temp[:,0],temp[:,1]])

def trgswSymEncrypt(p, alpha, h, key, twist):
    l = len(h)
    c = np.vstack([[trlweSymEncrypt(np.zeros(len(key)),alpha,key,twist)] for i in range(2*l)])
    muh = dtot32(np.outer(h,p))
    c[:l,0] += muh
    c[l:,1] += muh
    return c

def trgswExternalProdcut(g,r,params):
    decvec = Decomposition(r,params)
    return np.array([np.sum([PolyMul(decvec[i], g[i][0],params.twist) for i in range(2 * params.l)],axis = 0),np.sum([PolyMul(decvec[i], g[i][1],params.twist) for i in range(2 * params.l)], axis = 0)],dtype = np.uint32)