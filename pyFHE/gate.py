from .gatebootstrapping import GateBootstrappingFFT, GateBootstrappingTLWE2TLWEFFT
from .keyswitch import IdentityKeySwitch
from .key import CloudKey, FFTplans
import numpy as np

def HomNAND(ca, cb, ck: CloudKey, plan: FFTplans):
    return GateBootstrappingFFT(
        np.uint32(np.append(np.zeros(ck.params.n), 2 ** 29)) - ca - cb, ck, plan
    )


def HomOR(ca, cb, ck: CloudKey, plan: FFTplans):
    return GateBootstrappingFFT(
        np.uint32(np.append(np.zeros(ck.params.n), 2 ** 29)) + ca + cb, ck, plan
    )


def HomAND(ca, cb, ck: CloudKey, plan: FFTplans):
    return GateBootstrappingFFT(
        np.uint32(np.append(np.zeros(ck.params.n), -(2 ** 29))) + ca + cb, ck, plan
    )


def HomXOR(ca, cb, ck: CloudKey, plan: FFTplans):
    return GateBootstrappingFFT(
        np.uint32(np.append(np.zeros(ck.params.n), 2 ** 30)) + 2 * (ca + cb), ck, plan
    )


def HomXNOR(ca, cb, ck: CloudKey, plan: FFTplans):
    return GateBootstrappingFFT(
        np.uint32(np.append(np.zeros(ck.params.n), -(2 ** 30))) - 2 * (ca + cb), ck, plan
    )


def HomNOT(ca):
    return -ca


def HomNOR(ca, cb, ck: CloudKey, plan: FFTplans):
    return GateBootstrappingFFT(
        np.uint32(np.append(np.zeros(ck.params.n), -(2 ** 29))) - ca - cb, ck, plan
    )


def HomANDNY(ca, cb, ck: CloudKey, plan: FFTplans):
    return GateBootstrappingFFT(
        np.append(np.zeros(ck.params.n), np.uint32(-(2 ** 29))) - ca + cb, ck, plan
    )


def HomANDYN(ca, cb, ck: CloudKey, plan: FFTplans):
    return GateBootstrappingFFT(
        np.append(np.zeros(ck.params.n), np.uint32(-(2 ** 29))) + ca - cb, ck, plan
    )


def HomORNY(ca, cb, ck: CloudKey, plan: FFTplans):
    return GateBootstrappingFFT(np.append(np.zeros(ck.params.n), 2 ** 29) - ca + cb, ck, plan)


def HomORYN(ca, cb, ck: CloudKey, plan: FFTplans):
    return GateBootstrappingFFT(np.append(np.zeros(ck.params.n), 2 ** 29) + ca - cb, ck, plan)


def HomMUX(a, b, c, ck:CloudKey, plan: FFTplans):
    return IdentityKeySwitch(
        np.append(np.zeros(ck.params.n), 2 ** 29)
        + GateBootstrappingTLWE2TLWEFFT(
            np.append(np.zeros(ck.params.n), np.uint32(-(2 ** 29))) + a + b, ck, plan
        )
        + GateBootstrappingTLWE2TLWEFFT(
            np.append(np.zeros(ck.params.n), np.uint32(-(2 ** 29))) - a + c, ck, plan
        ),
        ck,
    )