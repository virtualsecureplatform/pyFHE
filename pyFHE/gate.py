from .gatebootstrapping import GateBootstrappingFFT, GateBootstrappingTLWE2TLWEFFT
from .keyswitch import IdentityKeySwitch
from .key import CloudKey
import numpy as np

def HomNAND(ca, cb, ck: CloudKey):
    return GateBootstrappingFFT(
        np.uint32(np.append(np.zeros(ck.params.n), 2 ** 29)) - ca - cb, ck
    )


def HomOR(ca, cb, ck: CloudKey):
    return GateBootstrappingFFT(
        np.uint32(np.append(np.zeros(ck.params.n), 2 ** 29)) + ca + cb, ck
    )


def HomAND(ca, cb, ck: CloudKey):
    return GateBootstrappingFFT(
        np.uint32(np.append(np.zeros(ck.params.n), -(2 ** 29))) + ca + cb, ck
    )


def HomXOR(ca, cb, ck: CloudKey):
    return GateBootstrappingFFT(
        np.uint32(np.append(np.zeros(ck.params.n), 2 ** 30)) + 2 * (ca + cb), ck
    )


def HomXNOR(ca, cb, ck: CloudKey):
    return GateBootstrappingFFT(
        np.uint32(np.append(np.zeros(ck.params.n), -(2 ** 30))) - 2 * (ca + cb), ck
    )


def HomNOT(ca):
    return -ca


def HomNOR(ca, cb, ck: CloudKey):
    return GateBootstrappingFFT(
        np.uint32(np.append(np.zeros(ck.params.n), -(2 ** 29))) - ca - cb, ck
    )


def HomANDNY(ca, cb, ck: CloudKey):
    return GateBootstrappingFFT(
        np.append(np.zeros(ck.params.n), np.uint32(-(2 ** 29))) - ca + cb, ck
    )


def HomANDYN(ca, cb, ck: CloudKey):
    return GateBootstrappingFFT(
        np.append(np.zeros(ck.params.n), np.uint32(-(2 ** 29))) + ca - cb, ck
    )


def HomORNY(ca, cb, ck: CloudKey):
    return GateBootstrappingFFT(np.append(np.zeros(ck.params.n), 2 ** 29) - ca + cb, ck)


def HomORYN(ca, cb, ck: CloudKey):
    return GateBootstrappingFFT(np.append(np.zeros(ck.params.n), 2 ** 29) + ca - cb, ck)


def HomMUX(a, b, c, ck):
    return IdentityKeySwitch(
        np.append(np.zeros(ck.params.n), 2 ** 29)
        + GateBootstrappingTLWE2TLWEFFT(
            np.append(np.zeros(ck.params.n), np.uint32(-(2 ** 29))) + a + b, ck
        )
        + GateBootstrappingTLWE2TLWEFFT(
            np.append(np.zeros(ck.params.n), np.uint32(-(2 ** 29))) - a + c, ck
        ),
        ck,
    )
