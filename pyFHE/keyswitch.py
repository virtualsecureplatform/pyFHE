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
    return t.sum(axis=1).sum(axis=0)


def IdentityKeySwitch(tlwe, ck: CloudKey):
    aibar = np.uint32(np.round(tlwe[:-1] * 2 ** (ck.params.basebit * ck.params.t - 32)))
    mask = (1 << ck.params.basebit) - 1

    lhs = np.uint32(np.append(np.zeros(ck.params.n), tlwe[-1]))
    rhs = calc_rhs(ck, aibar, mask)

    return lhs - rhs
