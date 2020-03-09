from .rotator import GateBootstrappingTLWE2TLWEFFT
from .switcher import IdentityKeySwitch

#ckは定数なので初期化のときに書き込まれてそのまま
def GateBootstrapping(tlwe,ck):
    reg = GateBootstrappingTLWE2TLWEFFT(tlwe,ck)
    return IdentityKeySwitch(reg,ck)