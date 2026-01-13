#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script to predict DS using NN trained in SchNetPack 2.0

"""

import logging
import platform
import time
import os 

from pSchnet_lib.parser.merge import parse_cmd
from pSchnet_lib.data.ASE import load_xyz, get_expected
from pSchnet_lib.data.CSV import load_csvs, collate_csvs, fill_empty_predictions
from pSchnet_lib.output.conversions import collate_expected_predicted_all
from pSchnet_lib.output.csv import write_csv


def main(args):
    
    device = 'cpu'
    csv_name = args.csvfile
    mode = args.mode
    splits = args.splits
    xyz_name = args.xyz_file.name
    output_format = args.output
    target = args.target
    
    logging.basicConfig(level = logging.INFO, filename='{}.log'.format("merge"), filemode='a', force=True)
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
    
    # get expected values
    expected_list = get_expected(atoms, target)
    
    start_time = time.time()
    logging.info("Start time: {}".format(start_time)) 
    
    # load csv files
    predictions_tmp = load_csvs(csv_name, splits)
    
    # reformat to output structure
    predictions0 = collate_csvs(expected_list, predictions_tmp)
    predictions = fill_empty_predictions(predictions0, splits)
    
    stop_time = time.time()
    logging.info("End time: {}".format(stop_time))
    
    logging.info("Run time: {}".format(stop_time-start_time)) 
    logging.info("Run time per molecule: {}".format((stop_time-start_time)/(num_mol*len(splits))))
    
    # export to csv
    if output_format == "predicted":
        
        name0=os.path.splitext(os.path.split(xyz_name)[-1])[-2]
        csv_name = '{}_{}.csv'.format(name0, "merge")
        
        logging.info('Writing predictions to file {} ...'.format(csv_name))
        write_csv(csv_name, predictions)
        
        logging.info('Predictions successfully stored in file {}'.format(csv_name))

    elif output_format == "expected_predicted":
            
        ep = collate_expected_predicted_all(expected_list, predictions, target)
            
        name0=os.path.splitext(os.path.split(xyz_name)[-1])[-2]
        csv_name = '{}_{}.csv'.format(name0, "merge")
            
        logging.info('Writing predictions to file {} ...'.format(csv_name))
        write_csv(csv_name, ep)
            
        logging.info('Predictions successfully stored in file {}'.format(csv_name))
    
    else:
        
        print("Incorrect output format detected. No output file provided.")
    
    return 0


if __name__ == '__main__':
    args = parse_cmd()
    main(args)
