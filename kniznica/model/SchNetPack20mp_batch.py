# -*- coding: utf-8 -*-

import torch
from kniznica.data.converter import AtomsConverterModule
from schnetpack.data import AtomsLoader
import pytorch_lightning


class trained_NN:
    
    def __init__(self, model_dir: str, splits: str, cutoff: float, target: str, device = 'cpu'):
        self.model_dir = model_dir
        self.splits = splits
        self.cutoff = cutoff
        self.target = target
        self.device = device
        self.converter = AtomsConverterModule(
            cutoff = self.cutoff,
            device = self.device,
            #n_cpu = n_cpu
            n_cpu = torch.get_num_threads()-2
            ) # converter to translate ASE atoms to Schnetpack input

    def predict(self, atoms):
        
        n_mol = len(atoms)
        property_list = [{} for i in range(n_mol)]
        print(n_mol)
        
        print(torch.get_num_threads())
        print(torch.get_num_interop_threads())
        # suradnicove vstupy z xyz; konverzia na vstup pre NN
        print(type(atoms))
        #print(list(atoms))
        print(type(list(atoms)))
        print(len(list(atoms)))
        inputs = self.converter(list(atoms))
        
        print(len(inputs))
        print(inputs.keys())
        
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
                num_nodes=1,
                devices=1, # all devices; 'auto' = based on accerelator; [int,..] list of indicies of the devices
                logger=False,
                accelerator='auto',
                enable_progress_bar=False
            )
            
            predicted_property = trainer.predict(model, dataloaders=dataloader) # inputs tu urcite nie su dobre
                        
            pp = []
            for a in predicted_property:

                pp.extend(a[self.target].numpy().tolist())


            
            # add prediction to dictionary
            for i in range(n_mol):
                property_list[i]["name"] = str(atoms[i].info['name'])
                property_list[i][split] = pp[i]
                
        return property_list
    
    
class pytorch_lightning_model_wrapper(pytorch_lightning.LightningModule):
    
    def __init__(
            self,
            model_dir,
            s
            ):
        
        super().__init__()
                        
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
        # schnet_parameters = inspect.getfullargspec(schnetpack.representation.SchNet)[0]
        #print(schnet_parameters)
        # if 'electronic_embeddings' in schnet_parameters:
        #     self.model.get_submodule("representation").electronic_embeddings = []
        #     print("Variable 'electronic_embeddings' is defined and declared as list(). ")
        if not hasattr(self.model.representation, "electronic_embeddings"):
            self.model.representation.electronic_embeddings = []
        

    def forward(self, inputs):
        return self.model(inputs)
    

        
    