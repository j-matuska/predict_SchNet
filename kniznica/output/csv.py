# -*- coding: utf-8 -*-

import csv

def write_csv(csvname: str, property_list: list):
    
    #name=os.path.splitext(os.path.split(name)[-1])[-2]
    
    with open(csvname, 'w') as csvsubor:
        
        fieldnames = property_list[0].keys()
        zapisovac = csv.DictWriter(csvsubor, fieldnames = fieldnames, delimiter=';')
        zapisovac.writeheader()
        
        for zaznam in property_list:
            #print(zaznam)
            zapisovac.writerow(zaznam)
            
    return 0