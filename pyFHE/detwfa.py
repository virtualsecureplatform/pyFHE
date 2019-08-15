from .trgsw import trgswExternalProdcut

def CMUX(C,d0,d1,params):
    return trgswExternalProdcut(C,d1-d0,params)+d0