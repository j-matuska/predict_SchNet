# -*- coding: utf-8 -*-

import torch
from schnetpack.interfaces import AtomsConverter
import schnetpack.transform


class extended_model:
    
    def __init__(self, split, model ):
        self.split = split
        self.model = model

class trained_NN:
    
    def __init__(self, modelname: str, splits: str, cutoff = 10.0, device = 'cpu'):
        self.modelname = modelname
        self.splits = splits
        self.cutoff = cutoff
        self.device = device
        self.converter = AtomsConverter(
            neighbor_list = schnetpack.transform.MatScipyNeighborList(cutoff = self.cutoff), # alternative: ASENeighborList(cutoff = cutoff), 
            transforms = [
                schnetpack.transform.SubtractCenterOfMass()
                ],
            device = self.device,
            dtype=torch.float32
            ) # converter to translate ASE atoms to Schnetpack input

    def predict(self, atoms):
        
        # this way is not quicker on CUDA. Verify for more molecules and empty graphic card
        
        # improvized solution, because only one NN model can be loaded at once; it cannot be quick
        n_mol = len(atoms)
        property_list = [{} for i in range(n_mol)]
                
        for split in self.splits:
            
            model = self.load_model(split)
            
            for i in range(n_mol):
            
                # suradnicove vstupy z xyz; konverzia na vstup pre NN
                inputs = self.converter(atoms[i])
                
                # add name to dictionary
                identifier = str(atoms[i].info['name'])
                property_list[i]["name"] = identifier
            
                # calculation of prediction
                pred = model(inputs)
                predicted_property = pred['DS'].detach().cpu().numpy()[0]
                # add prediction to dictionary
                property_list[i][split] = predicted_property
                    
        return property_list

    def load_model(self, s: str):
    
        if self.modelname == "Schnet20_6_10Ang_train80":
            modelpath = "/home/matuska/BACOVBEAT3_lowcharge/Schnet/6/80_{s}b".format(s = s) #format(modelname = self.modelname, s = s)
        
        return torch.load(modelpath+'/best_model', map_location = torch.device(self.device))
    
