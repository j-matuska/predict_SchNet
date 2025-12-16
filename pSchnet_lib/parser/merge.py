#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse

def parse_cmd():
    
    parser = argparse.ArgumentParser(description='Process comand-line inputs for merge.py.')
    

    
    # choise predicted variable; name of the variable have to be identical to name in XYZ file
    parser.add_argument("--csvfile", 
                        action = 'store',
                        #nargs = '+',
                        default = "custom.csv",
                        type = str,
                        #choices = [ '01', '02', '03', '04', '05'],
                        required = True,
                        help = "Name of the csv file in split folder. It should be the same in each split folder. Default: 'custom.csv' ",
                        metavar = "CSVFILE"
                        )
    
    # choise predicted variable; name of the variable have to be identical to name in XYZ file
    parser.add_argument("--target", 
                        action = 'store',
                        #nargs = '+',
                        default = "DS",
                        type = str,
                        #choices = [ '01', '02', '03', '04', '05'],
                        required = False,
                        help = "Choise of variable name to predict (target name). Necessary in case of hte 'custom' model. Name have to be identical to name in XYZ file and custom model. Default: 'DS' ",
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
    
    # choise output mode
    parser.add_argument("--output", 
                        action = 'store',
                        #nargs = 1,
                        default = 'predicted',
                        type = str,
                        choices = ['predicted', 'expected_predicted'],
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
                        help = "Full name of xyz file in extended xyz file format containing structure of the molecules. It is base for merging.",
                        metavar = "XYZ file"
                        )
    
    
    args = parser.parse_args()
    
    args.splits = args.splits.split(" ")

    return args
