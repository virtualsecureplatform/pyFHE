from .trgsw import trgswExternalProdcut
from .key import lweParams
import numpy as np

def CMUX(C,d0,d1,params:lweParams):
    return trgswExternalProdcut(C,d1-d0,params)+d0