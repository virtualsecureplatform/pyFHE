from .gatebootstrapping import GateBootstrappingFFT, GateBootstrappingTLWE2TLWEFFT
from .keyswitch import IdentityKeySwitch
from .key import CloudKey
import numpy as np
cimport numpy as np

cpdef HomNAND(np.ndarray[np.uint32_t] ca,np.ndarray[np.uint32_t] cb,ck:CloudKey):
    return GateBootstrappingFFT(np.uint32(np.append(np.zeros(ck.params.n),2**29)) - ca - cb,ck)

cpdef HomOR(np.ndarray[np.uint32_t] ca,np.ndarray[np.uint32_t] cb,ck:CloudKey):
    return GateBootstrappingFFT(np.uint32(np.append(np.zeros(ck.params.n),2**29)) + ca + cb,ck)

cpdef HomAND(np.ndarray[np.uint32_t] ca,np.ndarray[np.uint32_t] cb,ck:CloudKey):
    return GateBootstrappingFFT(np.uint32(np.append(np.zeros(ck.params.n),-2**29)) + ca + cb,ck)

cpdef HomXOR(np.ndarray[np.uint32_t] ca,np.ndarray[np.uint32_t] cb,ck:CloudKey):
    return GateBootstrappingFFT(np.uint32(np.append(np.zeros(ck.params.n),2**30)) + 2*(ca + cb),ck)

cpdef HomXNOR(np.ndarray[np.uint32_t] ca,np.ndarray[np.uint32_t] cb,ck:CloudKey):
    return GateBootstrappingFFT(np.uint32(np.append(np.zeros(ck.params.n),-2**30)) - 2*(ca + cb),ck)

cpdef HomNOT(np.ndarray[np.uint32_t] ca):
    return -ca

cpdef HomNOR(np.ndarray[np.uint32_t] ca,np.ndarray[np.uint32_t] cb,ck:CloudKey):
    return GateBootstrappingFFT(np.uint32(np.append(np.zeros(ck.params.n),-2**29)) - ca - cb,ck)

cpdef HomANDNY(np.ndarray[np.uint32_t] ca,np.ndarray[np.uint32_t] cb,ck:CloudKey):
    return GateBootstrappingFFT(np.append(np.zeros(ck.params.n),np.uint32(-2**29)) - ca + cb,ck)

cpdef HomANDYN(np.ndarray[np.uint32_t] ca,np.ndarray[np.uint32_t] cb,ck:CloudKey):
    return GateBootstrappingFFT(np.append(np.zeros(ck.params.n),np.uint32(-2**29)) + ca - cb,ck)

cpdef HomORNY(np.ndarray[np.uint32_t] ca,np.ndarray[np.uint32_t] cb,ck:CloudKey):
    return GateBootstrappingFFT(np.append(np.zeros(ck.params.n),2**29) - ca + cb,ck)

cpdef HomORYN(np.ndarray[np.uint32_t] ca,np.ndarray[np.uint32_t] cb,ck:CloudKey):
    return GateBootstrappingFFT(np.append(np.zeros(ck.params.n),2**29) + ca - cb,ck)

cpdef HomMUX(np.ndarray[np.uint32_t] ca,np.ndarray[np.uint32_t] cb,cc,ck):
    return IdentityKeySwitch(np.append(np.zeros(ck.params.n),2**29) + GateBootstrappingTLWE2TLWEFFT(np.append(np.zeros(ck.params.n),np.uint32(-2**29)) + ca + cb,ck) + GateBootstrappingTLWE2TLWEFFT(np.append(np.zeros(ck.params.n),np.uint32(-2**29)) - ca + cc,ck),ck)