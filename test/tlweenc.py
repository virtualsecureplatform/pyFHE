from pyFHE import key,tlwe

sk = key.SecretKey(500,2**(-9),1024,2,512,2**(-24))
c = tlwe.bootsSymEncrypt([0,1],sk)
print (tlwe.bootsSymDecrypt(c,sk))