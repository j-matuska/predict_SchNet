# -*- coding: utf-8 -*-
"""
Script to predict DS using NN trained in SchNetPack 0.3

Additonal options are comming soon...

"""

import sys
import logging
import platform
import time
import os 

from data.SchNetPack03 import load_xyz
from model.SchNetPack03 import trained_NN
#from prediction.SchNetPack03 import predict
from output.SchNetPack03 import write_csv

def main():
    
    device = 'cpu' # to be mofified to be readed from input
    modelname = 'Schnet03_6_10Ang_train80' # to be modified to be readed from input, but it maybe necessary, because on qchcluster is only one viable model 
    splits = ["01", "02", "03", "04", "05"]

    
    xyz_name = sys.argv[1] # only thing readed from input, xyz file in extended xyz format containing structure of molecules

    logging.basicConfig(level = logging.INFO, filename='{}.log'.format(modelname), filemode='a')
    logging.info(' ============================================= \n' )

    cpu_model = platform.processor()
    logging.info('{} \n'.format(cpu_model))
    
    # load molecules
    atoms = load_xyz(xyz_name)

    num_mol=len(atoms)
    print(xyz_name, 'Number of molecules: ',num_mol)
    logging.info('{} - Number of molecules: {}'.format(xyz_name, num_mol))
        
    # load NN from config
    NNs = trained_NN(modelname, splits, device = device)
    
    start_time = time.time()
    logging.info("Start time: {}".format(start_time)) 
    
    # predict all
    predictions = NNs.predict(atoms)
    
    stop_time = time.time()
    logging.info("End time: {}".format(stop_time))
    
    logging.info("Run time: {}".format(stop_time-start_time)) 
    logging.info("Run time per molecule: {}".format((stop_time-start_time)/num_mol))
    
    name0=os.path.splitext(os.path.split(xyz_name)[-1])[-2]
    csv_name = '%s_%s.csv' % (name0, modelname)
    
    logging.info('Writing predictions to file {} ...'.format(csv_name))
    
    # export to csv
    write_csv(csv_name, predictions)
    
    logging.info('Predictions successfully stored in file {}'.format(csv_name))
    
    return 0


if __name__ == '__main__':
    main()