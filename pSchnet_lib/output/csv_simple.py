# -*- coding: utf-8 -*-

def writecsv(csvname: str, property_list: list):
    
    #name=os.path.splitext(os.path.split(name)[-1])[-2]
    
    with open(csvname, 'w') as csvsubor:
        
        fieldnames = property_list[0].keys()
        csvsubor.writelines((";".join( str(x) for x in fieldnames),"\n"))
        
        for zaznam in property_list:
            #print(zaznam)
            csvsubor.writelines((";".join(str(y) for y in zaznam.values()),"\n"))
            
    return 0