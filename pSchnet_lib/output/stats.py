#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 12 20:57:06 2025

@author: jamat
"""

import numpy

def get_ensemble_variance(predictions):
    
    ensemble_variance_list = []
    for p in predictions:
        pn = to_numpy(p)
        ensemble_variance_list.append(
            {
                "ID": p["name"],
                "regression_prediction": pn.mean(),
                "ensemble_variance": pn.var(ddof=1),
                }
            )
            
    return ensemble_variance_list

def to_numpy(p):
    
    split_values = [v for k,v in p.items() if k != "name" ]
    
    return numpy.array(split_values)