#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 28 12:05:34 2025

@author: jamat
"""

import torch
from torch.utils.data import Dataset, Sampler

import schnetpack.transform
from schnetpack.interfaces import AtomsConverter

import pytorch_lightning

from typing import Optional, Sequence

class AtomsConverterModule(pytorch_lightning.LightningModule):
    
    def __init__(self, cutoff, device):
        super().__init__()
        self.converter = AtomsConverter(
            neighbor_list = schnetpack.transform.MatScipyNeighborList(cutoff = cutoff), # alternative: ASENeighborList(cutoff = cutoff), 
            transforms = [
                schnetpack.transform.SubtractCenterOfMass()
                ],
            device = device,
            dtype=torch.float32
            ) # converter to translate ASE atoms to Schnetpack input
        
    def forward(self, inputs):
        return self.converter(inputs)
    
    def predict_step(self, inputs):
        return self.converter(inputs)
    
class AtomsConverterDatamodule(pytorch_lightning.LightningDataModule):
    def __init__(
            self,
            inputs,
            batch_size: Optional[int] = 1,
            shuffle: bool = False,
            sampler: Optional[Sampler[int]] = None,
            batch_sampler: Optional[Sampler[Sequence[int]]] = None,
            num_workers: int = 0,
            pin_memory: bool = False
            ):
        super().__init__()
        self.inputs = inputs
        self.batch_size = batch_size
        self.shuffle = shuffle
        self.sampler = sampler
        self.batch_sampler = batch_sampler
        self.num_workers = num_workers
        self.pin_memory = pin_memory

    def train_dataloader(self):
        return torch.utils.data.DataLoader([])

    def val_dataloader(self):
        return torch.utils.data.DataLoader([])

    def test_dataloader(self):
        return torch.utils.data.DataLoader([])
    
    def predict_dataloader(self):
        dataset = torch.utils.data.DataLoader(
            self.inputs,
            batch_size = self.batch_size,
            num_workers = self.num_workers,
            shuffle = self.shuffle,
            pin_memory = self.pin_memory
            )
        return dataset
