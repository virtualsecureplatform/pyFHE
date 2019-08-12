import numpy as np
from .utils import gaussian32
from .key import SecretKey

mu = 2**29

def bootsSymEncrypt(p,key):
    plaintextlength = len(p)
    a=np.zeros((plaintextlength, key.params.n), dtype = np.int32)
    b=np.zeros(plaintextlength, dtype = np.int32)
    for i in range(plaintextlength):
        if p[i] == 0:
            a[i],b[i] = lweSymEncrypt(-mu,key)
        else:
            a[i],b[i] = lweSymEncrypt(mu,key)
    return np.array([a,b])

def bootsSymDecrypt(c,sk):
    ciphertextlength = len(c[0])
    return np.array([lweSymDecrypt(c[0][i],c[1][i],sk.key) for i in range(ciphertextlength)])

def lweSymEncrypt(p,key:SecretKey):
    a = np.random.randint(-2**31,2**31 ,size = key.params.n, dtype = np.int32)
    b = gaussian32(p,key.params.alpha,1)[0] + np.dot(a,key.key.tlwe)
    return a,b

def lweSymDecrypt(ca,cb,key:SecretKey):
    return np.int32((1 + np.sign(cb - np.dot(ca,key.tlwe)))/2)