import numpy as np
cimport numpy as np
from secrets import randbits
from .utils cimport gaussian32,dtot32

mu = 2**-3

def bootsSymEncrypt(p,sk):
    plaintextlength = len(p)
    c = np.empty((plaintextlength,sk.params.n+1),dtype = np.uint32)
    for i in range(plaintextlength):
        if p[i] == 0:
            c[i] = tlweSymEncrypt(-mu,sk.params.alpha,sk.key.tlwe)
        else:
            c[i] = tlweSymEncrypt(mu,sk.params.alpha,sk.key.tlwe)
    return c

def bootsSymDecrypt(c,sk):
    ciphertextlength = len(c)
    return np.array([tlweSymDecrypt(c[i],sk.key.tlwe) for i in range(ciphertextlength)])

def tlweSymEncrypt(float p,float alpha,np.uint32_t[:] key):
    cdef np.ndarray[np.uint32_t] a = np.array([randbits(32) for i in range(len(key))], dtype = np.uint32)
    cdef np.ndarray[np.uint32_t] b = gaussian32(np.array([dtot32(p)],dtype=np.uint32),alpha)
    return np.uint32(np.append(a,b[0]+ np.dot(a,np.array(key))))

def tlweSymDecrypt(c,key):
    return np.uint32((1 + np.sign(np.int32(c[len(key)] - np.dot(c[:len(key)],key))))/2)