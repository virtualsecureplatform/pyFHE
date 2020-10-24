import numpy as np

# Double to Torus32
def dtot32(d:np.float):
    return np.uint32(np.round((d%1)*(2**32)))

# Modular Gaussian distribution
def gaussian32(mu,alpha:float,size = 1):
    return dtot32(np.random.normal(0,alpha,size)) + np.uint32(mu)
