# -*- coding: utf-8 -*-

# not fully working

import pickle

def write_pickle(picklename: str, property_list: list):
    
    zaznam = {} 
    for k,v in property_list[0].items():
        zaznam[k] = [v.tolist()]
    
    for p in property_list[1:]:
        for k,v in p.items():
            zaznam[k].append(v.tolist())
    
    with open(picklename, 'wb') as file:
        pickle.dump(zaznam, file)
    
    return 0

def read_pickle(picklename: str):
    
    with open(picklename, 'rb') as file:
        data = pickle.load(file)
    
    return data["name"],data["01"]