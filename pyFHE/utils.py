import numpy as np

def dtot32(d: np.float):
    return np.uint32(np.round((d % 1) * (2 ** 32)))

def dtot64(d):
    return np.uint64(np.round((d%1)*(2.0**64)))

def gaussian32(mu, alpha: float, size=1):
    return dtot32(np.random.normal(0, alpha, size)) + np.uint32(mu)

def gaussian64(mu,alpha:float,size = 1):
    return dtot64(np.random.normal(0,alpha,size)) + np.uint64(mu)