# -*- coding: utf-8 -*-

import torch
from schnetpack import AtomsConverter


class trained_NN:
    
    def __init__(self, modelname: str, splits: str, device = 'cpu'):
        self.modelname = modelname
        self.splits = splits
        self.models = self.load_models()
        self.converter = AtomsConverter(device=device) # converter to translate ASE atoms to Schnetpack input
        
    def predict(self, atoms):
        
        property_list = []
        
        for at in atoms:
        
            # suradnicove vstupy z xyz #
            inputs = self.converter(at)
            identifier = str(at.info['name'])
            
            # create dictionary with name and predictions
            line = {}
            
            # add name to dictionary
            line["name"] = identifier
            
            for split, model in self.models:
                
                # calculation of prediction
                pred = model(inputs)
                predicted_property = pred['DS'].detach().cpu().numpy()[0,0]
                # add prediction to dictionary
                line[split] = predicted_property
                
            property_list.append( 
                line 
                )
        
        return property_list

    def load_models(self):
        
        trained_models = []
        
        for s in self.splits:
            
            modelpath = "/ehome/PROGS/misc/schnetpack_models/kniznica/model/trained_models/{modelname}/{s}".format(modelname = self.modelname, s = s)
            trained_models.append(
                (
                    s,
                    torch.load(modelpath+'/best_model')
                    )
                )
            
        return trained_models
    
def load_model(modelname):
    
    """
    Testing function to load only first model from cross-validation.
    """
    
    splits = ["01"]
    
    modelpath = "trained_models/{modelname}/{s}".format(modelname = modelname, s = splits[0])
    model = torch.load(modelpath+'/best_model')

    return [trained_NN(model, splits)]

