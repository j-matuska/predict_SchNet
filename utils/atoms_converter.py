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
from kniznica.data.converter import AtomsConverterModule, AtomsConverterDatamodule
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
    
    atoms = load_xyz(xyz_name)
    
    datamodule = AtomsConverterDatamodule(
        atoms,
        batch_size = 100,
        num_workers = 4,
        )
    
    model = AtomsConverterModule(5.0, device)
    
    trainer = pytorch_lightning.Trainer(
        num_nodes=1,
        devices=1, # all devices; 'auto' = based on accerelator; [int,..] list of indicies of the devices
        strategy="auto",
        logger=False,
        accelerator='auto',
        enable_progress_bar=False
    )
    
    prediction = trainer.predict(model, dataloaders=datamodule)
    
    print(prediction)

if __name__ == '__main__':
    args = parse_cmd()
    main(args)