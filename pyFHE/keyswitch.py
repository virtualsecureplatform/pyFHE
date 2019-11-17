from .key import CloudKey
from .key import lweParams
import numpy as np

def IdentityKeySwitch(tlwe,ck:CloudKey):
    aibar = np.uint32(np.round(tlwe[:-1] * 2**(ck.params.basebit*ck.params.t -32)))
    mask = (1<<ck.params.basebit) - 1
    return np.uint32(np.append(np.zeros(ck.params.n),tlwe[-1])) - np.sum([np.sum([ck.ksk[i][j][aibar[i]>>(ck.params.basebit*(ck.params.t-(j+1))) &mask] for j in range(ck.params.t)], axis = 0) for i in range(ck.params.N)],axis = 0)