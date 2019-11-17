from .key import CloudKey
from .key import lweParams
import numpy as np

def calc_rhs(ck, aibar, mask):
    indices_rhs = ck.params.basebit * np.arange(ck.params.t)[::-1]
    indices_lhs = np.tile(aibar, (ck.params.t, 1)).T
    indices = indices_lhs >> indices_rhs & mask

    first = np.repeat(np.arange(ck.params.N), ck.params.t)
    second = np.tile(np.arange(ck.params.t), ck.params.N)

    t = ck.ksk[first, second, indices.ravel()]
    t = t.reshape((ck.params.N, ck.params.t, -1))
    return t.sum(axis=(0, 1))

def IdentityKeySwitch(tlwe, ck: CloudKey):
    aibar = np.uint32(np.round(tlwe[:-1] * 2 ** (ck.params.basebit * ck.params.t - 32)))
    mask = (1 << ck.params.basebit) - 1

    lhs = np.uint32(np.append(np.zeros(ck.params.n), tlwe[-1]))
    rhs = calc_rhs(ck, aibar, mask)

    return lhs - rhs

def TLWE2TRLWEprivateKeySwitch(tlwe,ck:CloudKey,u):
    aibar = np.uint32(np.round(tlwe * 2 ** (ck.params.basebitlvl21 * ck.params.tbar - 64)))
    mask = (1 << ck.params.basebitlvl21) - 1

    indices_rhs = ck.params.basebitlvl21 * np.arange(ck.params.tbar)[::-1]
    indices_lhs = np.tile(aibar, (ck.params.tbar, 1)).T
    indices = indices_lhs >> indices_rhs & mask

    second = np.repeat(np.arange(ck.params.nbar+1), ck.params.tbar)
    third = np.tile(np.arange(ck.params.tbar), ck.params.nbar+1)

    t = ck.privksk[u, second, third, indices.ravel()]
    # t = t.reshape((ck.params.nbar, ck.params.tbar, -1))
    return -t.sum(axis=0)

# indices = np.arange(ck.params.nbar+1)

#     return np.sum([ck.privksk[u,indices,j,aibar>>(ck.params.basebit*(ck.params.t-(j+1))) &mask].sum(axis = 0) for j in range(ck.params.tbar)],axis=0)