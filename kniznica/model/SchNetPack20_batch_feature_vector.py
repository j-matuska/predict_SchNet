# -*- coding: utf-8 -*-

# important: there is problem with memory. This takes too much memory. 
# 1825 molecules takes all the RAM. probably pl and torch is way to go.

import torch
from schnetpack.interfaces import AtomsConverter
from schnetpack.data import AtomsLoader
import schnetpack.transform
import pytorch_lightning
import inspect
from typing import Sequence, Union, Callable, Dict, Optional


class extended_model:
    
    def __init__(self, split, model ):
        self.split = split
        self.model = model

class FV(torch.nn.Module):
    """
    Copy embedings from representation.
    Modified clas Atomwise() from schnetpack
    """

    def __init__(
        self,
        n_in: int,
        output_key: str = "y",
        per_atom_output_key: Optional[str] = None,
    ):
        """
        Args:
            n_in: input dimension of representation
            output_key: the key under which the result will be stored
            per_atom_output_key: If not None, the key under which the per-atom result will be stored
        """
        super(FV, self).__init__()
        self.output_key = output_key
        self.model_outputs = [output_key]
        self.per_atom_output_key = per_atom_output_key
        if self.per_atom_output_key is not None:
            self.model_outputs.append(self.per_atom_output_key)
        self.n_out = n_in

        self.outnet = torch.nn.Identity(128)

    def forward(self, inputs: Dict[str, torch.Tensor]) -> Dict[str, torch.Tensor]:
        # predict atomwise contributions
        y = self.outnet(inputs["scalar_representation"])

        # accumulate the per-atom output if necessary
        if self.per_atom_output_key is not None:
            inputs[self.per_atom_output_key] = y

        inputs[self.output_key] = y
        return inputs


class trained_NN:
    
    def __init__(self, model_dir: str, splits: str, cutoff: float, target: str, device = 'cpu'):
        self.model_dir = model_dir
        self.splits = splits
        self.cutoff = cutoff
        self.target = target
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
                num_nodes=1,
                devices=1, # all devices; 'auto' = based on accerelator; [int,..] list of indicies of the devices
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
        if not hasattr(self.model.representation, "electronic_embeddings"):
            self.model.representation.electronic_embeddings = []
        
        # modification of the output module
        #
        # This is not ideal.
        # TO DO:
        #   - output_key have to be self.target (e.g. DS) as in previous output. It should be modifiable.
        #   - It is not recomended to load whole model. Model should be constructed and only weights loaded. That could solve first issue.
        #
        self.model.get_submodule("output_modules")[0] = FV(
            n_in = 128, 
            output_key = self.target, 
            per_atom_output_key = "fv"
            )
    
    
    def forward(self, inputs):
        return self.model(inputs)
        
    