#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse

def parse_cmd():
    
    parser = argparse.ArgumentParser(description='Process comand-line inputs for predict.py.')
    
    # choise model
    parser.add_argument("--model", 
                        action = 'store',
                        #nargs = 1,
                        default = 'Schnet20_6_10Ang_train80', # na himalaya; inde bude ina
                        type = str,
                        choices = ['Schnet20_6_5Ang_train80', 
                                   'Schnet20_6_10Ang_train80', 
                                   'Schnet03_6_10Ang_train80', 
                                   'PaiNN20_3_5Ang_train80', 
                                   'pdbqt_M1+M2_PaiNN20_3_5Ang_train80', 
                                   'pdbqt_M1+M2_Schnet20_6_5Ang_train80', 
                                   'pdbqt_M1_PaiNN20_3_5Ang_train80', 
                                   'pdbqt_M1_Schnet20_6_5Ang_train80', 
                                   'pdbqt_M2_PaiNN20_3_5Ang_train80', 
                                   'pdbqt_M2_Schnet20_6_5Ang_train80', 
                                   'pdbqt_M3+M2_PaiNN20_3_5Ang_train80', 
                                   'pdbqt_M3+M2_Schnet20_6_5Ang_train80', 
                                   'pdbqt_M3_PaiNN20_3_5Ang_train80', 
                                   'pdbqt_M3_Schnet20_6_5Ang_train80', 
                                   'pdbqt_M4_PaiNN20_3_5Ang_train80', 
                                   'pdbqt_M4_Schnet20_6_5Ang_train80',
                                   'pdbqt_Mpro_SchNet',
                                   'current'],
                        required = False,
                        help = "Optional choise of the pretrained NN model. Default: 'Schnet20_6_10Ang_train80' ",
                        metavar = "MODEL"
                        )
    
    # choise predicted variable; name of the variable have to be identical to name in XYZ file
    parser.add_argument("--target", 
                        action = 'store',
                        #nargs = '+',
                        default = "DS",
                        type = str,
                        #choices = [ 'DS', 'feature_vector'],
                        required = False,
                        help = "Choise of variable name to predict (target name). Necessary in case of the 'custom' model. Name have to be identical to name in XYZ file and custom model. Default: 'DS' ",
                        metavar = "TARGET"
                        )
    
    # choise split, default = all, but possibility to choose only one split
    parser.add_argument("--splits", 
                        action = 'store',
                        #nargs = '+',
                        default = "01 02 03 04 05",
                        type = str,
                        #choices = [ '01', '02', '03', '04', '05'],
                        required = False,
                        help = "Optional choise of cross-validation instance from the pretrained NN model. Separated by space. Default: '01 02 03 04 05' ",
                        metavar = " '01 ...', "
                        )
    
    # choise mode
    parser.add_argument("--mode", 
                        action = 'store',
                        #nargs = 1,
                        default = 'serial',
                        type = str,
                        choices = ['serial', 'parallel'],
                        required = False,
                        help = "Optional choise of the computer resources. Mode 'serial' allocate 4 cpu and one graphic card. Mode 'parallel' aim to take all possible graphic cards (not fully functional). Default: 'serial' ",
                        metavar = "MODE"
                        )
    
    # choise device
    parser.add_argument("--device", 
                        action = 'store',
                        #nargs = 1,
                        default = 'cuda',
                        type = str,
                        choices = ['cuda', 'cpu'],
                        required = False,
                        help = "Optional choise of the computer resources. Mode 'cuda' is loading model to one graphic card. Mode 'cpu' is loading model into the cpu. Default: 'cuda' ",
                        metavar = "DEVICE"
                        )
    
    # choise output mode
    parser.add_argument("--output", 
                        action = 'store',
                        #nargs = 1,
                        default = 'predicted',
                        type = str,
                        choices = ['predicted', 'expected_predicted', 'ensemble_variance'],
                        required = False,
                        help = "Optional choise of the output format. Default: 'predicted' ",
                        metavar = "FORMAT"
                        )
                    
    # choise xyz file
    parser.add_argument("xyz_file",
                        action = 'store',
                        #nargs = 1,
                        type = argparse.FileType('r'),
                        #choices = [],
                        #required = True,
                        help = "Full name of xyz file in extended xyz file format containing structure of the molecules.",
                        metavar = "XYZ file"
                        )
    
    
    args = parser.parse_args()
    
    args.splits = args.splits.split(" ")

    return args
