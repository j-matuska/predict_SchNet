#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import torch
from torch.utils.data import DataLoader

from schnetpack.interfaces import AtomsConverter
from schnetpack.data import AtomsLoader
import schnetpack.transform

import pytorch_lightning

import logging

from ASE import load_xyz

class XYZDataset(DataLoader):
    """
    
    """
    def __init__(self, xyz_name):
        super().__init__()
        self.xyz_name = xyz_name
        self.converter = AtomsConverter(
            neighbor_list = schnetpack.transform.MatScipyNeighborList(cutoff = self.cutoff), # alternative: ASENeighborList(cutoff = cutoff), 
            transforms = [
                schnetpack.transform.SubtractCenterOfMass()
                ],
            device = self.device,
            dtype=torch.float32
            ) # converter to translate ASE atoms to Schnetpack input
    
    

class XYZDataModule(pytorch_lightning.LightningDataModule):
    """
    A general ``LightningDataModule`` for conversion of XYZ to SchNetPack dataset.

    """
    def __init__(self, xyz_name):
        super().__init__()
        self.xyz_name = xyz_name
        self.converter = AtomsConverter(
            neighbor_list = schnetpack.transform.MatScipyNeighborList(cutoff = self.cutoff), # alternative: ASENeighborList(cutoff = cutoff), 
            transforms = [
                schnetpack.transform.SubtractCenterOfMass()
                ],
            device = self.device,
            dtype=torch.float32
            ) # converter to translate ASE atoms to Schnetpack input
    
    def prepare_data(self):
        # download, IO, etc. Useful with shared filesystems
        # only called on 1 GPU/TPU in distributed
        # load molecules
        self.molecules = load_xyz(self.xyz_name)

        num_mol=len(self.molecules)
        print(self.xyz_name, 'Number of molecules: ',num_mol)
        logging.info('{} - Number of molecules: {}'.format(self.xyz_name, num_mol))

    def setup(self, stage):
        # make assignments here (val/train/test split)
        # called on every process in DDP
        
        n_mol = len(self.molecules)
        #property_list = [{} for i in range(n_mol)]
        print(n_mol)
        
        print(torch.get_num_threads())
        print(torch.get_num_interop_threads())
        # suradnicove vstupy z xyz; konverzia na vstup pre NN
        #inputs = [self.converter(a) for a in self.molecules]
        # it is not working, somehow it is in conflict with torch
        # pool = torch.multiprocessing.Pool(4)#multiprocessing.cpu_count())
        # inputs = [pool.apply(self.converter, args=([a for a in atoms],))]
        # pool.close()
        inputs = self.converter(list(self.molecules))
        
        print(len(inputs))
        
        dataloader = AtomsLoader(
                inputs,
                batch_size=100,
                num_workers=4,
                shuffle=False,
                # shuffle=True,
                pin_memory=True
            )
        

    def train_dataloader(self):
        return [0]

    def val_dataloader(self):
        return [0]

    def test_dataloader(self):
        return [0]

    def on_exception(self, exception):
        # clean up state after the trainer faced an exception
        ...

    def teardown(self):
        # clean up state after the trainer stops, delete files...
        # called on every process in DDP
        ...
