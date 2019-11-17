from .mulfft import PolyMul,PolyMullvl2Long
from .utils import gaussian32, dtot32, gaussian64, dtot64
from secrets import randbits
import os
import numpy as np


def trlweSymEncrypt(p, alpha, key, twist):
    # a = np.array([randbits(32) for i in range(len(key))], dtype=np.uint32)
    a = np.frombuffer(os.urandom(len(key) * 4), dtype=np.uint32)
    b = gaussian32(dtot32(p), alpha, len(key))
    b += PolyMul(a, key, twist)
    return np.array([a, b])

def trlweSymEncryptlvl2(p,alpha,key, twistlong):
    # a = np.array([randbits(64) for i in range(len(key))], dtype = np.uint64)
    a = np.frombuffer(os.urandom(len(key) * 8), dtype=np.uint64)
    b = gaussian64(dtot64(p),alpha,len(key))
    b += PolyMullvl2Long(a,key,twistlong)
    return np.array([a,b])

def trlweSymDecrypt(c, key, twist):
    return (1 + np.sign(np.int32(c[1] - PolyMul(c[0], key, twist)))) // 2

def trlweSymDecryptlvl2(c, key, twistlong):
    return (1 + np.sign(np.int64(c[1] - PolyMullvl2Long(c[0], key, twistlong)))) // 2

def SampleExtractIndex(r, index):
    N = len(r[0])
    return np.concatenate(
        [
            [r[0][index - i] for i in range(index + 1)],
            [-r[0][N - 1 - i] for i in range(N - index - 1)],
            [r[1][index]],
        ]
    )
