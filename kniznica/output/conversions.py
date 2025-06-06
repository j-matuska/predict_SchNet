#!/usr/bin/env python3
# -*- coding: utf-8 -*-

def collate_expected_predicted(expected:list , predicted:list, split:str, target:str):
    
    property_list = []
    
    if len(expected) != len(predicted):
        
        print("Incopatible lists.",
              "Lenght of 'expected' is:", len(expected),
              "Lenght of 'predicted' is:", len(predicted),
              "Please provide 'energy' in xyz file."
              )
        return 0
    
    for e,p in zip(expected,predicted):
        
        if e["name"] == p["name"]:
            property_list.append(
                {"name" : e["name"],
                 "expected" : e[target],
                 "predicted" : p[split]
                 }
                )
    
    return property_list

def collate_expected_predicted_all(expected:list , predicted:list, target:str):
    
    property_list = []
    
    if len(expected) != len(predicted):
        
        print("Incopatible lists.",
              "Lenght of 'expected' is:", len(expected),
              "Lenght of 'predicted' is:", len(predicted),
              "Please provide 'energy' in xyz file."
              )
        return 0
    
    for e,p in zip(expected,predicted):
        
        if e["name"] == p["name"]:
        
            property_item = { "name" : e["name"],
                              "expected" : e[target],
                            }
                            
            for key in p.keys():
                if key != "name":
                    property_item[key] = p[key]
                    
            property_list.append(
                property_item
                )
    
    return property_list

def collate_ensemble_variance_target(expected_list:list, target:str):
    
    output_list = []
    
    for el in expected_list:
        
        output_list.append(
            {
                "ID": el["name"],
                "regression_property": el[target]
                }
            )
        
    return output_list