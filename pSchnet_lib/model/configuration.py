#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 21 09:44:40 2024

@author: j-matuska
"""

import os

def get_models_configuration(modelname, args):

    configuration = {
    "Schnet20_6_10Ang_train80" : {
        "model_dir": "trained_models/Schnet20_6_10Ang_train80/", 
        "cutoff": 10.0,
        "target": "DS"
        },
    "Schnet03_6_10Ang_train80" : {
        "model_dir": "trained_models/Schnet03_6_10Ang_train80/", 
        "cutoff": 10.0,
        "target": "DS"
        },
    "Schnet20_6_5Ang_train80" : {
        "model_dir": "trained_models/Schnet20_6_5Ang_train80/", 
        "cutoff": 5.0,
        "target": "DS"
        },
    "PaiNN20_3_5Ang_train80" : {
        "model_dir": "trained_models/PaiNN20_3_5Ang_train80/", 
        "cutoff": 5.0,
        "target": "DS"
        },
    "pdbqt_M1+M2_PaiNN20_3_5Ang_train80" : {
        "model_dir": "trained_models/pdbqt_M1+M2_PaiNN20_3_5Ang_train80/", 
        "cutoff": 5.0,
        "target": "DS"
        },
    "pdbqt_M1+M2_Schnet20_6_5Ang_train80" : {
        "model_dir": "trained_models/pdbqt_M1+M2_Schnet20_6_5Ang_train80/", 
        "cutoff": 5.0,
        "target": "DS"
        },
    "pdbqt_M1_PaiNN20_3_5Ang_train80" : {
        "model_dir": "trained_models/pdbqt_M1_PaiNN20_3_5Ang_train80/", 
        "cutoff": 5.0,
        "target": "DS"
        },
    "pdbqt_M1_Schnet20_6_5Ang_train80" : {
        "model_dir": "trained_models/pdbqt_M1_Schnet20_6_5Ang_train80/", 
        "cutoff": 5.0,
        "target": "DS"
        },
    "pdbqt_M2_PaiNN20_3_5Ang_train80" : {
        "model_dir": "trained_models/pdbqt_M2_PaiNN20_3_5Ang_train80/", 
        "cutoff": 5.0,
        "target": "DS"
        },
    "pdbqt_M2_Schnet20_6_5Ang_train80" : {
        "model_dir": "trained_models/pdbqt_M2_Schnet20_6_5Ang_train80/", 
        "cutoff": 5.0,
        "target": "DS"
        },
    "pdbqt_M3+M2_PaiNN20_3_5Ang_train80" : {
        "model_dir": "trained_models/pdbqt_M3+M2_PaiNN20_3_5Ang_train80/", 
        "cutoff": 5.0,
        "target": "DS"
        },
    "pdbqt_M3+M2_Schnet20_6_5Ang_train80" : {
        "model_dir": "trained_models/pdbqt_M3+M2_Schnet20_6_5Ang_train80/", 
        "cutoff": 5.0,
        "target": "DS"
        },
    "pdbqt_M3_PaiNN20_3_5Ang_train80" : {
        "model_dir": "trained_models/pdbqt_M3_PaiNN20_3_5Ang_train80/", 
        "cutoff": 5.0,
        "target": "DS"
        },
    "pdbqt_M3_Schnet20_6_5Ang_train80" : {
        "model_dir": "trained_models/pdbqt_M3_Schnet20_6_5Ang_train80/", 
        "cutoff": 5.0,
        "target": "DS"
        },
    "pdbqt_M4_PaiNN20_3_5Ang_train80" : {
        "model_dir": "trained_models/pdbqt_M4_PaiNN20_3_5Ang_train80/", 
        "cutoff": 5.0,
        "target": "DS"
        },
    "pdbqt_M4_Schnet20_6_5Ang_train80" : {
        "model_dir": "trained_models/pdbqt_M4_Schnet20_6_5Ang_train80/", 
        "cutoff": 5.0,
        "target": "DS"
        },
    "pdbqt_Mpro_SchNet" : {
        "model_dir": "trained_models/pdbqt_Mpro_SchNet/", 
        "cutoff": 5.0,
        "target": "energy_Mpro"
        },
    "current" : {
        "model_dir": ".", 
        "cutoff": 5.0,
        "target": args.target
        }
    } 
    
    return configuration[modelname]

def get_model_properties(modelname: str, args):
    
    #json_models_configuration = "models_configuration.json"
    
    #print(os.getcwd())
    
    #with open(json_models_configuration,"r") as r:
    #   models_configuration = json.load(r)
    
    model_conf = get_models_configuration(modelname, args)
    
    if model_conf["model_dir"] == "." : 
        model_dir =  model_conf["model_dir"]
    else:
        dirname = os.path.dirname(__file__)
        model_dir = os.path.join(dirname, model_conf["model_dir"])
    
    cutoff = model_conf["cutoff"]
    
    target = model_conf["target"]
    
    return model_dir, cutoff, target
