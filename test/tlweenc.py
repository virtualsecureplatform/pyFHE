from pyFHE import tlwe

sk = tlwe.SecretKey(500,2**(-9))
cb,ca = tlwe.bootsSymEncrypt([0,1],sk)
print (tlwe.bootsSymDecrypt(cb,ca,sk))