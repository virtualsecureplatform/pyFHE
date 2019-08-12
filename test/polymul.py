from pyFHE.mulfft import PolyMul,TwistGen

a = [2,0,0,1]
b = [2,3,1,2]

print(PolyMul(a,b,TwistGen(4)))