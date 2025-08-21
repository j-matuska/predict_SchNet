# -*- coding: utf-8 -*-

import numpy

def write_npz(npzname: str, property_list: list):
    
    zaznam = {} 
    for k,v in property_list[0].items():
        zaznam[k] = [v]
    
    for p in property_list:
        for k,v in p.items():
            zaznam[k].append(v)
    
    numpy.save(npzname, **zaznam)
    
    return 0
