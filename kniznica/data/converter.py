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
    
class AtomsConverterDatamodule(torch.utils.data.DataLoader):
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
        super().__init__(
            inputs,
            batch_size = batch_size,
            num_workers = num_workers,
            shuffle = shuffle,
            pin_memory = pin_memory
            )


