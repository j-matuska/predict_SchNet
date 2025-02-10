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
    
    def __init__(self, cutoff, device, n_cpu = 4):
        super().__init__()
        self.n_cpu = n_cpu
        self.converter = AtomsConverter(
            neighbor_list = schnetpack.transform.MatScipyNeighborList(cutoff = cutoff), # alternative: ASENeighborList(cutoff = cutoff), 
            transforms = [
                schnetpack.transform.SubtractCenterOfMass()
                ],
            device = device,
            dtype=torch.float32
            ) # converter to translate ASE atoms to Schnetpack input
        
    def converter2(self, i, inputs, outputs):
        #print(inputs)
        outputs[i] = self.converter(inputs)
        #print(outputs)
        
    def __call__(self, inputs):
        batch_size = len(inputs)//self.n_cpu
        # pool = multiprocessing.Pool(processes=self.n_cpu)
        # print(inputs)
        # print(type(inputs))
        # outputs = pool.map(self.converter, inputs, chunksize=batch_size)
        # pool.close()
        # pool.join()
        processes = []
        outputs = multiprocessing.Manager().dict()
        for i in range(self.n_cpu):
            p = multiprocessing.Process(target=self.converter2, args=(i,inputs[i*batch_size:(i+1)*batch_size],outputs))
            processes.append(p)
            p.start()
        for p in processes:
            p.join()
        #print(outputs)
        c_outputs = outputs[0]
        for i in range(1,self.n_cpu):
            for key in outputs[0].keys():
                if "_idx" == key:
                    c_outputs[key] = torch.cat(
                        (
                            c_outputs[key], 
                            outputs[i][key].add(i*batch_size)
                            ),
                        dim = 0 
                        )
                elif "_idx_m" == key:
                    c_outputs[key] = torch.cat(
                        (
                            c_outputs[key], 
                            outputs[i][key].add(i*batch_size)
                            ),
                        dim = 0 
                        )
                elif "_idx_i" == key:
                    c_outputs[key] = torch.cat(
                        (
                            c_outputs[key], 
                            outputs[i][key].add(torch.sum(c_outputs["_n_atoms"][:i*batch_size]).item())
                            ), 
                        dim = 0
                        )
                elif "_idx_j" == key:
                    c_outputs[key] = torch.cat(
                        (
                            c_outputs[key], 
                            outputs[i][key].add(torch.sum(c_outputs["_n_atoms"][:i*batch_size]).item())
                            ),
                        dim = 0
                        )
                else:
                    c_outputs[key] = torch.cat(
                        (
                            c_outputs[key],
                            outputs[i][key]
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


