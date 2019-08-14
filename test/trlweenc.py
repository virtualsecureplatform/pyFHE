from pyFHE import key,trlwe

sk = key.SecretKey(500,2**(-9),2,2,512,2**(-24))
c = trlwe.trlweSymEncrypt([-2**29,2**29],2**(-27),sk.key.trlwe,sk.key.twist)
print (trlwe.trlweSymDecrypt(c,sk.key.trlwe,sk.key.twist))