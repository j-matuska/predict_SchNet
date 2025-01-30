#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script to predict DS using NN trained in SchNetPack 2.0

"""

import logging
import platform
import time
import os 

from kniznica.parser.predict import parse_cmd
from kniznica.data.ASE import load_xyz, get_expected
from kniznica.model.SchNetPack20_batch import trained_NN
#from kniznica.model.SchNetPack21_batch import trained_NN
from kniznica.output.conversions import collate_expected_predicted_all
from kniznica.output.csv import write_csv
from kniznica.model.configuration import get_model_properties


def main(args):
    
    device = 'cpu'
    mode = args.mode
    modelname = args.model
    splits = args.splits
    xyz_name = args.xyz_file.name
    output_format = args.output
    
    logging.basicConfig(level = logging.INFO, filename='{}.log'.format(modelname), filemode='a', force=True)
    logging.info(' \n' )
    logging.info(' ============================================= \n' )
    logging.info(args)

    cpu_model = platform.processor()
    logging.info('{} \n'.format(cpu_model))
    
    # load molecules
    atoms = load_xyz(xyz_name)

    num_mol=len(atoms)
    print(xyz_name, 'Number of molecules: ',num_mol)
    logging.info('{} - Number of molecules: {}'.format(xyz_name, num_mol))
    
    # define properties of model
    model_dir, cutoff, target = get_model_properties(modelname, args)
    
    # load NN from config
    NNs = trained_NN(model_dir, splits, cutoff, target, device = device)
    
    start_time = time.time()
    logging.info("Start time: {}".format(start_time)) 
    
    # predict all
    predictions = NNs.predict(atoms)
    
    stop_time = time.time()
    logging.info("End time: {}".format(stop_time))
    
    logging.info("Run time: {}".format(stop_time-start_time)) 
    logging.info("Run time per molecule: {}".format((stop_time-start_time)/(num_mol*len(splits))))
    
    # export to csv
    if output_format == "predicted":
        
        name0=os.path.splitext(os.path.split(xyz_name)[-1])[-2]
        csv_name = '{}_{}.csv'.format(name0, modelname)
        
        logging.info('Writing predictions to file {} ...'.format(csv_name))
        write_csv(csv_name, predictions)
        
        logging.info('Predictions successfully stored in file {}'.format(csv_name))

    elif output_format == "expected_predicted":
        
        expected_list = get_expected(atoms, target)
            
        ep = collate_expected_predicted_all(expected_list, predictions, target)
            
        name0=os.path.splitext(os.path.split(xyz_name)[-1])[-2]
        csv_name = '{}_{}.csv'.format(name0, modelname)
            
        logging.info('Writing predictions to file {} ...'.format(csv_name))
        write_csv(csv_name, ep)
            
        logging.info('Predictions successfully stored in file {}'.format(csv_name))
    
    else:
        
        print("Incorrect output format detected. No output file provided.")
    
    return 0


if __name__ == '__main__':
    args = parse_cmd()
    main(args)
