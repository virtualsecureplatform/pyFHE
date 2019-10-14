from .key import CloudKey
from .key import lweParams
import numpy as np

def IdentityKeySwitch(tlwe,ksk,params:lweParams):
    aibar = np.uint32(np.round(tlwe[:-1] * 2**(params.basebit*params.t -32)))
    mask = 1<<params.basebit
    return np.zeros(params.n).append(tlwe[-1]) - np.sum([[ksk[i][j][aibar>>(32-(j+1)*params.Bgbit)&mask] for j in range(params.t)] for i in range(params.n)])

