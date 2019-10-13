from .key import CloudKey
from .key import lweParams
import numpy as np

def IdentityKeySwitch(tlwe,ksk,params:lweParams):
    res = np.zeros(params.n).append(tlwe[-1])
    