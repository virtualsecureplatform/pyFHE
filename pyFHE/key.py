import numpy as np
import pyfftw
from secrets import randbits
from .mulfft import TwistGen,TwistGenLong
from .tlwe import tlweSymEncrypt
from .trlwe import trlweSymEncrypt, trlweSymEncryptlvl2
from .trgsw import trgswfftSymEncrypt, trgswfftSymEncryptlvl2


class lweKey:
    def __init__(self, n: int, N: int, nbar:int):
        self.tlwe = np.array([randbits(1) for i in range(n)], dtype=np.uint32)
        self.trlwe = np.array([randbits(1) for i in range(N)], dtype=np.uint32)
        self.lvl2 = np.array([randbits(1) for i in range(nbar)],dtype = np.uint64)

class lweParams:
    def __init__(
        self,
        n: int,
        alpha: float,
        N: int,
        l: int,
        Bgbit: int,
        bkalpha: float,
        t: int,
        basebit: int,
        ksalpha: float,
        nbar:int,lbar:int,Bgbitbar:int,bklvl02alpha:float, tbar:int, basebitlvl21:int, privkskalpha:float
    ):
        self.n = n
        self.alpha = alpha
        self.N = N
        self.l = l
        self.Bg = 1 << Bgbit
        self.Bgbit = Bgbit
        self.bkalpha = bkalpha
        self.h = np.array([self.Bg ** (-(i + 1)) for i in range(l)], dtype=np.double)
        self.offset = np.uint32(self.Bg / 2 * np.sum(2 ** 32 * self.h))
        self.decbit = [32 - (p + 1) * Bgbit for p in range(l)]
        self.twist = TwistGen(N)
        self.t = t
        self.basebit = basebit
        self.ksalpha = ksalpha

        self.nbar = nbar
        self.lbar = lbar
        self.Bgbar = 1 << Bgbitbar
        self.Bgbitbar = Bgbitbar
        self.bklvl02alpha = bklvl02alpha
        self.hbar = np.array([np.double(self.Bgbar)**(-(i+1)) for i in range(lbar)],dtype = np.double)
        self.offsetlvl2 = np.uint64(self.Bgbar/2 * np.sum(2**64 * self.hbar))
        self.decbitlvl2 = [64 - (p + 1) * Bgbitbar for p in range(lbar)]
        self.tbar = tbar
        self.twistlvl2 = TwistGen(nbar)
        self.twistlvl2long = TwistGenLong(nbar)
        self.basebitlvl21 = basebitlvl21
        self.privkskalpha = privkskalpha

class SecretKey:
    def __init__(
        self,
        n: int,
        alpha: float,
        N: int,
        l: int,
        Bgbit: int,
        bkalpha: float,
        t: int,
        basebit: int,
        ksalpha: float,
        nbar:int,lbar:int,Bgbitbar:int,bklvl02alpha:float, tbar:int, basebitlvl21:int, privkskalpha:float
    ):  # Modify this to change parameter
        self.params = lweParams(n, alpha, N, l, Bgbit, bkalpha, t, basebit, ksalpha,nbar,lbar,Bgbitbar,bklvl02alpha,tbar,basebitlvl21,privkskalpha)
        self.key = lweKey(n, N,nbar)

class CloudKey:
    def __init__(self, sk: SecretKey):
        # if k, the decomposed part of the target of keyswitch function, is 0, the value is trivial.
        self.ksk = np.uint32(
            np.array(
                [
                    [
                        np.concatenate(
                            [
                                [np.zeros(sk.params.n + 1)],
                                [
                                    tlweSymEncrypt(
                                        sk.key.trlwe[i]
                                        * k
                                        * 2.0 ** (-(j + 1) * sk.params.basebit),
                                        sk.params.ksalpha,
                                        sk.key.tlwe,
                                    )
                                    for k in range(1, 2 ** sk.params.basebit)
                                ],
                            ]
                        )
                        for j in range(sk.params.t)
                    ]
                    for i in range(sk.params.N)
                ]
            )
        )
        
        key = np.append(np.int32(sk.key.lvl2),np.int32(-1))

        self.privksk = np.uint32(
            np.array(
                [
                    np.array([
                        np.array([
                            np.concatenate(
                                [
                                    [np.zeros((2,sk.params.N),dtype=np.uint32)],
                                    [
                                        trlweSymEncrypt(
                                            np.zeros(sk.params.N),
                                            sk.params.privkskalpha,
                                            sk.key.trlwe,
                                            sk.params.twist
                                        )
                                        + np.uint32(np.roll(
                                            np.concatenate([[u*key[i] << (32-(j+1)*sk.params.basebitlvl21)],np.zeros(2*sk.params.N-1)]),
                                            z*sk.params.N
                                            ).reshape(2,sk.params.N))
                                        for u in range(1, 2**sk.params.basebitlvl21)
                                    ]
                                ]
                            )
                            for j in range(sk.params.tbar)
                        ])
                        for i in range(sk.params.nbar + 1)
                    ])
                    for z in range(2)
                ]
            )
        )

        self.bkfft = np.array(
            [
                trgswfftSymEncrypt(
                    np.uint32(
                        np.concatenate([[sk.key.tlwe[i]], np.zeros(sk.params.N - 1)])
                    ),
                    sk.params.bkalpha,
                    sk.params.h,
                    sk.key.trlwe,
                    sk.params.twist
                )
                for i in range(sk.params.n)
            ]
        )

        self.bklvl02fft = np.array(
            [
                trgswfftSymEncryptlvl2(
                    np.uint64(
                        np.concatenate([[sk.key.tlwe[i]], np.zeros(sk.params.nbar - 1)])
                    ),
                    sk.params.bklvl02alpha,
                    sk.params.hbar,
                    sk.key.lvl2,
                    sk.params.twistlvl2long
                )
                for i in range(sk.params.n)
            ]
        )

        self.params = sk.params