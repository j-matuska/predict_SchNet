#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 21 09:44:40 2024

@author: j-matuska
"""

import os

def get_models_configuration():

    configuration = {
    "Schnet20_6_10Ang_train80" : {
        "model_dir": "trained_models/Schnet20_6_10Ang_train80/", 
        "cutoff": 10.0
        },
    "Schnet03_6_10Ang_train80" : {
        "model_dir": "trained_models/Schnet03_6_10Ang_train80/", 
        "cutoff": 10.0
        },
    "Schnet20_6_5Ang_train80" : {
        "model_dir": "trained_models/Schnet20_6_5Ang_train80/", 
        "cutoff": 5.0
        }
    } 
    
    return configuration

def get_model_properties(modelname: str):
    
    #json_models_configuration = "models_configuration.json"
    
    #print(os.getcwd())
    
    #with open(json_models_configuration,"r") as r:
    #   models_configuration = json.load(r)
    
    models_configuration = get_models_configuration()
    
    model_conf = models_configuration[modelname]
    
    dirname = os.path.dirname(__file__)
    
    model_dir = os.path.join(dirname, model_conf["model_dir"])
    cutoff = model_conf["cutoff"]
    
    return model_dir, cutoff
