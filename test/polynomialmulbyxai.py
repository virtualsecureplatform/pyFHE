from pyFHE.gatebootstrapping import PolynomialMulByXai
from pyFHE.key import SecretKey
from pyFHE.utils import dtot32
import numpy as np

sk = SecretKey(500,2**(-9),8,2,1024,2**-24,8,2,2.44e-5)
x = dtot32(np.array([-2**-3,2**-3,-2**-3,2**-3,-2**-3,2**-3,-2**-3,-2**-3]))
y = PolynomialMulByXai(x,10,8)
print(np.sign(np.int32(y)))