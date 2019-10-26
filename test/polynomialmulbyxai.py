from pyFHE.gatebootstrapping import PolynomialMulByXai
from pyFHE.key import SecretKey
from pyFHE.utils import dtot32
import numpy as np

N = 10
a = np.random.randint(2*N)
x = np.uint32(np.random.randint(0,2**10,N))
y = PolynomialMulByXai(x,a,N)
b = np.flip(np.array(((np.poly1d(np.flip(x))*np.poly1d(np.append(1,np.zeros(a))))/np.poly1d(np.concatenate([[1],np.zeros(N-1),[-1]])))[1]))
print(x)
print(a)
print(b)
print(y)