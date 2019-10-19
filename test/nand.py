from pyFHE.tlwe import tlweSymEncrypt,tlweSymDecrypt
from pyFHE.key import SecretKey,CloudKey
from pyFHE.gate import HomNAND
from time import time

import numpy as np
from concurrent import futures


def test():
    sk = SecretKey(500,2.44e-5,1024,2,10,3.73e-9,8,2,2.44e-5)
    ck = CloudKey(sk)
    pa = np.random.binomial(1,0.5)
    pb = np.random.binomial(1,0.5)
    ca = tlweSymEncrypt((pa * 2 + -1) * (2**-3),sk.params.alpha,sk.key.tlwe)
    cb = tlweSymEncrypt((pb * 2 + -1) * (2**-3),sk.params.alpha,sk.key.tlwe)
    start = time()
    res = HomNAND(ca,cb,ck)
    end = time()
    print(end - start)
    y = tlweSymDecrypt(res,sk.key.tlwe)
    np.set_printoptions(threshold=2000)
    if (pa&pb)^1 != y:
        exit()
future_list = []
test()
# with futures.ProcessPoolExecutor() as executor:
#     for i in range(10):
#         future = executor.submit(fn=test,index=i)
#         future_list.append(future)
#     _ = futures.as_completed(fs=future_list)
print('completed.')
