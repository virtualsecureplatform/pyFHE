import numpy as np

def dtot32(d:np.float):
    return np.int32((d%1)*(2**32))

def gaussian32(mu,alpha:float,size = 1):
    return dtot32(np.random.normal(mu,alpha,size))