from .gatebootstrapping cimport GateBootstrappingFFT, GateBootstrappingTLWE2TLWEFFT
from .keyswitch cimport IdentityKeySwitch
from .key cimport CloudKey
import numpy as np
cimport numpy as np

cpdef HomNAND(np.ndarray[np.uint32_t] ca,np.ndarray[np.uint32_t] cb,CloudKey ck):
    return GateBootstrappingFFT(np.uint32(np.append(np.zeros(ck.params.n),2**29)) - ca - cb,ck)

def HomOR(np.ndarray[np.uint32_t] ca,np.ndarray[np.uint32_t] cb,CloudKey ck):
    return GateBootstrappingFFT(np.uint32(np.append(np.zeros(ck.params.n),2**29)) + ca + cb,ck)

def HomAND(np.ndarray[np.uint32_t] ca,np.ndarray[np.uint32_t] cb,CloudKey ck):
    return GateBootstrappingFFT(np.uint32(np.append(np.zeros(ck.params.n),-2**29)) + ca + cb,ck)

def HomXOR(np.ndarray[np.uint32_t] ca,np.ndarray[np.uint32_t] cb,CloudKey ck):
    return GateBootstrappingFFT(np.uint32(np.append(np.zeros(ck.params.n),2**30)) + 2*(ca + cb),ck)

def HomXNOR(np.ndarray[np.uint32_t] ca,np.ndarray[np.uint32_t] cb,CloudKey ck):
    return GateBootstrappingFFT(np.uint32(np.append(np.zeros(ck.params.n),-2**30)) - 2*(ca + cb),ck)

def HomNOT(np.ndarray[np.uint32_t] ca):
    return -ca

def HomNOR(np.ndarray[np.uint32_t] ca,np.ndarray[np.uint32_t] cb,CloudKey ck):
    return GateBootstrappingFFT(np.uint32(np.append(np.zeros(ck.params.n),-2**29)) - ca - cb,ck)

def HomANDNY(np.ndarray[np.uint32_t] ca,np.ndarray[np.uint32_t] cb,CloudKey ck):
    return GateBootstrappingFFT(np.append(np.zeros(ck.params.n),np.uint32(-2**29)) - ca + cb,ck)

def HomANDYN(np.ndarray[np.uint32_t] ca,np.ndarray[np.uint32_t] cb,CloudKey ck):
    return GateBootstrappingFFT(np.append(np.zeros(ck.params.n),np.uint32(-2**29)) + ca - cb,ck)

def HomORNY(np.ndarray[np.uint32_t] ca,np.ndarray[np.uint32_t] cb,CloudKey ck):
    return GateBootstrappingFFT(np.append(np.zeros(ck.params.n),2**29) - ca + cb,ck)

def HomORYN(np.ndarray[np.uint32_t] ca,np.ndarray[np.uint32_t] cb,CloudKey ck):
    return GateBootstrappingFFT(np.append(np.zeros(ck.params.n),2**29) + ca - cb,ck)

def HomMUX(np.ndarray[np.uint32_t] ca,np.ndarray[np.uint32_t] cb,cc,ck):
    return IdentityKeySwitch(np.append(np.zeros(ck.params.n),2**29) + GateBootstrappingTLWE2TLWEFFT(np.append(np.zeros(ck.params.n),np.uint32(-2**29)) + ca + cb,ck) + GateBootstrappingTLWE2TLWEFFT(np.append(np.zeros(ck.params.n),np.uint32(-2**29)) - ca + cc,ck),ck)