import numpy as np
from secrets import randbits
from .utils import gaussian32, gaussian64, dtot32, dtot64
import os

mu = 2 ** -3


def bootsSymEncrypt(p, sk):
    plaintextlength = len(p)
    c = np.empty((plaintextlength, sk.params.n + 1), dtype=np.uint32)
    for i in range(plaintextlength):
        if p[i] == 0:
            c[i] = tlweSymEncrypt(-mu, sk.params.alpha, sk.key.tlwe)
        else:
            c[i] = tlweSymEncrypt(mu, sk.params.alpha, sk.key.tlwe)
    return c


def bootsSymDecrypt(c, sk):
    ciphertextlength = len(c)
    return np.array(
        [tlweSymDecrypt(c[i], sk.key.tlwe) for i in range(ciphertextlength)]
    )


def tlweSymEncrypt(p, alpha, key):
    # a = np.array([randbits(32) for i in range(len(key))], dtype=np.uint32)
    a = np.frombuffer(os.urandom(len(key) * 4), dtype=np.uint32)
    b = gaussian32(dtot32(p), alpha, 1)[0] + np.dot(a, key)
    return np.append(a, b)

def tlweSymEncryptlvl2(p, alpha, key):
    a = np.array([randbits(64) for i in range(len(key))], dtype=np.uint64)
    b = gaussian64(dtot64(p), alpha, 1)[0] + np.dot(a, key)
    return np.append(a, b)

def tlweSymDecrypt(c, key):
    return np.uint32(
        (1 + np.sign(np.int32(c[len(key)] - np.dot(c[: len(key)], key)))) / 2
    )