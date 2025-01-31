#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 31 16:37:50 2025

@author: jamat
"""

import csv

def load_csv(csv_name):
    
    with open(csv_name, 'r') as csvsubor:
        
        citac = csv.DictReader(csvsubor, delimiter=';')
    
    return citac

def load_csvs(csv_name : str, splits: list()):
    """
    Read the files in ecah of the split folder.

    Parameters
    ----------
    csv_name : str
        Name of the csv file.
    splits : list()
        Folder names of the splits in list.

    Returns
    -------
    predictions : TYPE
        List of lists of dictionaries containing names of the molecules and their predicted docking scores.
        
    """
    # read the files
    prediction_tmp = []
    for s in splits:
        expanded_csv_name = "./{s}/{csv_name}".format(s=s, csv_name=csv_name)
        prediction_tmp.append(
            load_csv(expanded_csv_name)
            )
    
    return prediction_tmp

def collate_csvs(expected_list, prediction_tmp):
    
    n_mol = len(expected_list)
    predictions = [{"name": e["name"]} for e in expected_list]
    for split_p in prediction_tmp:
        for p in split_p:
            for key in p.keys():
                if key != "name":
                    predictions[key] = p[key]
    
    return predictions

def fill_empty_predictions(predictions, splits):
    
    for p in predictions:
        for s in splits:
            if s not in p.keys():
                p[s]=""
    
    return predictions