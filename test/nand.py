
from pyFHE.tlwe import tlweSymEncrypt,tlweSymDecrypt
from pyFHE.key import SecretKey,CloudKey
from pyFHE.gate import HomNAND

import numpy as np
import time


def test():
    sk = SecretKey(500,2.44e-5,1024,2,10,3.73e-9,8,2,2.44e-5)
    ck = CloudKey(sk)
    pa = np.random.binomial(1,0.5)
    pb = np.random.binomial(1,0.5)
    ca = tlweSymEncrypt((pa * 2 + -1) * (2**-3),sk.params.alpha,sk.key.tlwe)
    cb = tlweSymEncrypt((pb * 2 + -1) * (2**-3),sk.params.alpha,sk.key.tlwe)
    res = HomNAND(ca,cb,ck)
    start = time.time()
    for i in range(10):
        res = HomNAND(ca,cb,ck)
    end = time.time()
    print((end-start)/10)
    y = tlweSymDecrypt(res,sk.key.tlwe)
    np.set_printoptions(threshold=2000)
    if (pa&pb)^1 != y:
        print("FAILED")
        print(tlweSymDecrypt(np.uint32(np.append(np.zeros(ck.params.n),2**29)) - ca - cb,sk.key.tlwe))
        print(y)
        exit()
future_list = []
test()
# with futures.ProcessPoolExecutor() as executor:
#     for i in range(10):
#         future = executor.submit(fn=test,index=i)
#         future_list.append(future)
#     _ = futures.as_completed(fs=future_list)
print('completed.')
