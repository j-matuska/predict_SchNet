#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 28 14:17:43 2025

@author: jamat
"""

import logging
import platform
import time
import os 
import pytorch_lightning


from kniznica.parser.predict import parse_cmd
from kniznica.data.converter import AtomsConverterModule, AtomsConverterModuleSerial
from kniznica.data.ASE import load_xyz



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
    
    stime = time.time()
    logging.info("Start time: {}".format(stime)) 
    atoms = load_xyz(xyz_name)
    etime = time.time()
    logging.info("End time: {}".format(etime)) 
    logging.info("Run time: {}".format(etime-stime))
    
    stime = time.time()
    logging.info("Start time: {}".format(stime)) 
    
    model = AtomsConverterModule(5.0, device)

    prediction = model(list(atoms))
    
    logging.info("End time: {}".format(etime)) 
    logging.info("Run time: {}".format(etime-stime))
    
    stime = time.time()
    logging.info("Start time: {}".format(stime)) 
    
    modelSerial = AtomsConverterModuleSerial(5.0, device)

    predictionSerial = modelSerial(list(atoms))
    
    logging.info("End time: {}".format(etime)) 
    logging.info("Run time: {}".format(etime-stime))
    for key in ["_idx_j", "_idx_i", "_idx", "_idx_m"]:
        print(key, predictionSerial[key].size(), prediction[key].size())
        print(predictionSerial[key])
        print(prediction[key])
        
    for key in prediction.keys():
        print(key, (prediction[key]==predictionSerial[key]).all())

if __name__ == '__main__':
    args = parse_cmd()
    main(args)