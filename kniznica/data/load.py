#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import torch
from torch.utils.data import Dataset, Sampler
from torch.utils.data.dataloader import _collate_fn_t, T_co

from schnetpack.interfaces import AtomsConverter
from schnetpack.data import AtomsLoader, _atoms_collate_fn
import schnetpack.transform

from typing import Optional, Sequence

import pytorch_lightning

import logging

from ASE import load_xyz

class XYZAtomsDataLoader(AtomsLoader):
    """
    
    """
    def __init__(
        self, 
        xyz_name :str,
        batch_size: Optional[int] = 1,
        shuffle: bool = False,
        sampler: Optional[Sampler[int]] = None,
        batch_sampler: Optional[Sampler[Sequence[int]]] = None,
        num_workers: int = 0,
        collate_fn: _collate_fn_t = _atoms_collate_fn,
        pin_memory: bool = False,
        **kwargs,
        ):
        super(XYZAtomsDataLoader, self).__init__(
            dataset = load_xyz(xyz_name),
            batch_size = batch_size,
            shuffle = shuffle,
            sampler = sampler,
            batch_sampler = batch_sampler,
            num_workers = num_workers,
            collate_fn = collate_fn,
            pin_memory = pin_memory,
            **kwargs,
            )
        self.xyz_name = xyz_name
        # self.converter = AtomsConverter(
        #     neighbor_list = schnetpack.transform.MatScipyNeighborList(cutoff = self.cutoff), # alternative: ASENeighborList(cutoff = cutoff), 
        #     transforms = [
        #         schnetpack.transform.SubtractCenterOfMass()
        #         ],
        #     device = self.device,
        #     dtype=torch.float32
        #     ) # converter to translate ASE atoms to Schnetpack input
        # load molecules
        # self.molecules = 
        
    
    

class XYZDataModule(pytorch_lightning.LightningDataModule):
    """
    A general ``LightningDataModule`` for conversion of XYZ to SchNetPack dataset.

    """
    def __init__(
            self, 
            xyz_name : str,
            batch_size: Optional[int] = 1,
            shuffle: bool = False,
            sampler: Optional[Sampler[int]] = None,
            batch_sampler: Optional[Sampler[Sequence[int]]] = None,
            num_workers: int = 0,
            collate_fn: _collate_fn_t = _atoms_collate_fn,
            pin_memory: bool = False,
            **kwargs,
            ):
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
        self.batch_size = batch_size,
        self.shuffle = shuffle,
        self.sampler = sampler,
        self.batch_sampler = batch_sampler,
        self.num_workers = num_workers,
        self.collate_fn = collate_fn,
        self.pin_memory = pin_memory
    
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
 
        self.predict_data = self.converter(list(self.molecules))
    
    def predict_dataloader(self):
        dataloader = AtomsLoader(
                self.predict_data,
                batch_size = self.batch_size,
                num_workers = self.num_workers,
                shuffle = self.shuffle,
                # shuffle=True,
                pin_memory = self.pin_memory
            )
        return dataloader

