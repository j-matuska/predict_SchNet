# -*- coding: utf-8 -*-

# important: there is problem with memory. This takes too much memory. 
# 1825 molecules takes all the RAM. probably pl and torch is way to go.

import torch
from schnetpack.interfaces import AtomsConverter
from schnetpack.data import AtomsLoader
import schnetpack.transform
import pytorch_lightning
import inspect


class extended_model:
    
    def __init__(self, split, model ):
        self.split = split
        self.model = model

class trained_NN:
    
    def __init__(self, model_dir: str, splits: str, cutoff: float, device = 'cpu'):
        self.model_dir = model_dir
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
        
        n_mol = len(atoms)
        property_list = [{} for i in range(n_mol)]
        print(n_mol)
        
        print(torch.get_num_threads())
        print(torch.get_num_interop_threads())
        # suradnicove vstupy z xyz; konverzia na vstup pre NN
        inputs = [self.converter(a) for a in atoms]
        
        print(len(inputs))
        
        dataloader = AtomsLoader(
                inputs,
                batch_size=100,
                num_workers=4,
                shuffle=False,
                # shuffle=True,
                # pin_memory=self._pin_memory,
            )
        
        print(len(dataloader))
                
        for split in self.splits:
            
            model = pytorch_lightning_model_wrapper(self.model_dir, split)
            
            # calculation of prediction
                        
            trainer = pytorch_lightning.Trainer(
                num_nodes=4,
                devices=-1, # all devices; 'auto' = based on accerelator; [int,..] list of indicies of the devices
                logger=False,
                accelerator='auto',
                enable_progress_bar=False
            )
            
            predicted_property = trainer.predict(model, dataloaders=dataloader) # inputs tu urcite nie su dobre
            
            # print(type(predicted_property), predicted_property)
            
            pp = []
            for a in predicted_property:
                # print(a)
                # print(type(a))
                pp.extend(a["DS"].numpy().tolist())

            #pp = torch.cat([ a["DS"] for a in predicted_property])

            #predicted_property = model.results['DS'].detach().cpu().numpy()
                
            # add name to dictionary
            #identifier = str(atoms[i].info['name'])
            #property_list[i]["name"] = identifier
            
            # add prediction to dictionary
            for i in range(n_mol):
                property_list[i]["name"] = str(atoms[i].info['name'])
                property_list[i][split] = pp[i]
                
        return property_list

    # def load_model(self, s: str):
    
    #     if self.modelname == "Schnet20_6_10Ang_train80":
    #         modelpath = "/home/matuska/BACOVBEAT3_lowcharge/Schnet/6/80_{s}b".format(s = s) #format(modelname = self.modelname, s = s)
        
    #     return torch.load(modelpath+'/best_model', map_location = torch.device(self.device))
    
class pytorch_lightning_model_wrapper(pytorch_lightning.LightningModule):
    
    def __init__(
            self,
            model_dir,
            s
            ):
        
        super().__init__()
                
        # if self.modelname == "Schnet20_6_10Ang_train80":
        #     modelpath = "kniznica/model/trained_models/Schnet20_6_10Ang_train80/{s}".format(s = model_dir) #format(modelname = self.modelname, s = s)
        
        self.model_dir = "{model_dir}/{s}".format(model_dir = model_dir, s = s)
        
        # Load model at the end
        self.model = None
        self.load_model()
        
        self.results = []
    

    def load_model(self):
    
        self.model = torch.load(
            self.model_dir+'/best_model'
            )
        
        # modification to fit model of older SchNetPack 2.0.1 to newer SchNetPack 2.1.1
        schnet_parameters = inspect.getfullargspec(schnetpack.representation.SchNet)[0]
        #print(schnet_parameters)
        if 'electronic_embeddings' in schnet_parameters:
            self.model.get_submodule("representation").electronic_embeddings = []
            print("Variable 'electronic_embeddings' is defined and declared as list(). ")
        
    # def predict_step(self, batch):
    #     inputs, target = batch
    #     return self.model(inputs, target)
    
    def forward(self, inputs):
        return self.model(inputs)
    
    # def predict_step(self, batch, batch_idx, dataloader_idx=0):
        
    #     p = self(batch)
    #     self.results.append(p)
        
    #     return p
    
    # def on_predict_epoch_end(self):
        
    #     pp = torch.cat(self.results)

    #     # Now gather everything
    #     pp = self.all_gather(pp)

    #     # Reshape to remove the num_processes dimension.
    #     # NOTE: order is likely not going to match dataloader order
    #     self.results["DS"] = torch.flatten(pp, 0, -1).detach().cpu().numpy()
        
    