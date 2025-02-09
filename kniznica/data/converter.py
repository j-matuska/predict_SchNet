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

import multiprocessing

from typing import Optional, Sequence

class AtomsConverterModule:
    
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
        
    def __call__(self, inputs):
        pool = multiprocessing.Pool(processes=4)
        outputs = pool.map(self.converter, inputs)
        pool.close()
        pool.join()
        c_outputs = outputs[0]
        for i,stream in enumerate(outputs[1:]):
            for key in outputs[0].keys():
                if "_idx" == key:
                    c_outputs[key] = torch.cat(
                        (
                            c_outputs[key], 
                            stream[key].add(i*len(inputs)//4)
                            ),
                        dim = 0 
                        )
                elif "_idx_m" == key:
                    c_outputs[key] = torch.cat(
                        (
                            c_outputs[key], 
                            stream[key].add(i*len(input)//4)
                            ),
                         dim = 0 
                         )
                elif "_idx_i" == key:
                    c_outputs[key] = torch.cat(
                        (
                            c_outputs[key], 
                            stream[key].add(torch.sum(c_outputs["_n_atoms"][:-1]).item())
                            ), 
                        dim = 0
                        )
                elif "_idx_j" == key:
                    c_outputs[key] = torch.cat(
                        (
                            c_outputs[key], 
                            stream[key].add(torch.sum(c_outputs["_n_atoms"][:-1]).item())
                            ),
                        dim = 0
                        )
                else:
                    c_outputs[key] = torch.cat(
                        (
                            c_outputs[key],
                            stream[key]
                            ),
                        dim = 0 
                        )
            
        return c_outputs
    
class AtomsConverterModuleSerial:
    
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
        
    def __call__(self, inputs):
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


