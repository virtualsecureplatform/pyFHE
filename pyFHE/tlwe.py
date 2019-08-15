import numpy as np
from .utils import gaussian32,dtot32
from .key import SecretKey

mu = 2**-3

def bootsSymEncrypt(p,sk:SecretKey):
    plaintextlength = len(p)
    c = np.empty((plaintextlength,sk.params.n+1),dtype = np.uint32)
    for i in range(plaintextlength):
        if p[i] == 0:
            c[i] = lweSymEncrypt(-mu,sk.params.alpha,sk.key.tlwe)
        else:
            c[i] = lweSymEncrypt(mu,sk.params.alpha,sk.key.tlwe)
    return c

def bootsSymDecrypt(c,sk):
    ciphertextlength = len(c)
    return np.array([lweSymDecrypt(c[i],sk.key.tlwe) for i in range(ciphertextlength)])

def lweSymEncrypt(p,alpha,key):
    a = np.random.randint(0,2**32 ,size = len(key), dtype = np.uint32)
    b = gaussian32(dtot32(p),alpha,1)[0] + np.dot(a,key)
    return np.append(a,b)

def lweSymDecrypt(c,key):
    return np.uint32((1 + np.sign(np.int32(c[len(key)] - np.dot(c[:len(key)],key))))/2)