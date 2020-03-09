import numpy as np
from .key import lweParams,CloudKey

#paramsは定数
N = 1024

#Module
def dtot32(d:np.float):
    return np.uint32(np.round((d%1)*(2**32)))

#Module
#ただマスクして配線繋ぎ変えてほぼ符号反転して出力するだけ
def SampleExtractIndexZero(r):
    return np.concatenate([[r[0][0]],[-r[0][N-1-i] for i in range(N-1)],[r[1][0]]])

#Module
def PolyMulNaieve(a,b):
    rotreg = np.array(b,dtype=np.uint32)
    acc = np.zeros(len(a),dtype=np.uint32)
    for i in  range(len(a)):
        acc += a*rotreg
        rotreg = np.roll(rotreg,1)
        rotreg[0]*=-1
    return acc

#Module
def PolynomialMulByXai(poly,a):
    res = np.roll(poly,a)
    if(N<a):
        res[0:a]*=-1
    else:
        aa = a-N
        res[aa:-1]*=-1
    return res

#Module(たぶんこれスカラーずつやったほうが良い気がするけどここでは配列として表現。アドレス叩き込んだらこの配列と同じ結果が出ればいい)
def Decomposition(trlwe,params):
    temp = np.uint32(np.floor(np.multiply.outer(params.decb,trlwe + params.offset)%params.Bg) - params.Bg/2) #DOING FLOOR IS IMPORTANT.
    return np.concatenate([temp[:,0],temp[:,1]])

#Function
def trgswExternalProduct(g,r,params):
    decvec = Decomposition(r,params)
    #これたぶんひとつのモジュールでPolとSummationするやつで二回やるあれ。並列でも良い。CB考えるとそれもあり？
    return np.array([np.sum([PolyMulNaieve(decvec[i], g[i][0]) for i in range(2 * params.l)],axis = 0),np.sum([PolyMulNaieve(decvec[i], g[i][1]) for i in range(2 * params.l)], axis = 0)],dtype = np.uint32)

#Function
def CMUX(C,d1,d0,params:lweParams):
    return trgswExternalProdcut(C,d1-d0,params)+d0

#Function
def BlindRotate(bk,t:np.ndarray, r:np.ndarray,params:lweParams):#t is TLWE and r is TRLWE polynomial to rotate and t is TLWE
    bara = np.uint32(np.round(np.double(t) * (2**-32 * 2 * params.N)))
    bara[-1] = 2 * params.N - bara[-1]#こいつだけ特別
    #baraは多分スカラーとして１個ずつ生成するのが良い
    acc = np.array([PolynomialMulByXai(r[0],bara[-1],params.N),PolynomialMulByXai(r[1],bara[-1],params.N)])
    for i in range(params.n):
        if bara[i] == 0:
            continue 
        acc = CMUX(bk[i],np.array([PolynomialMulByXai(acc[0],bara[i],params.N),PolynomialMulByXai(acc[1],bara[i],params.N)]),acc,params)#ここうまいことやれば一時変数減らせる？
    return acc

#Function
def GateBootstrappingTLWE2TLWEFFT(t,ck:CloudKey):
    testvec = np.array([np.zeros(ck.params.N),np.full(ck.params.N,dtot32(2**-3))]) #This is same as original implemetation of TFHE.
    return SampleExtractIndexZero(BlindRotate(ck.bk,t,testvec,ck.params))