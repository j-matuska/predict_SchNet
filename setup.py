#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan  8 12:01:33 2025

@author: jamat
"""

from setuptools import setup
import os

def package_files(directory):
    paths = []
    for (path, directories, filenames) in os.walk(directory):
        for filename in filenames:
            paths.append(os.path.join('..', path, filename))
    return paths

data_files = package_files('./pSchnet_lib/model/trained_models')

setup(
    name="predict",
    version="1.1",
    author="J. Matuska",
    url="https://github.com/j-matuska/predict_SchNet",
    #packages=find_packages("."),
    packages=[
        'pSchnet_lib',
        'pSchnet_lib.parser',
        'pSchnet_lib.data',
        'pSchnet_lib.model',
        'pSchnet_lib.output',
        'pSchnet_lib.model.trained_models'
        ],
    package_dir={"": "."},
    package_data={
        '' : data_files
        },
    scripts=[
        "predict.py",
        "merge.py",
        "predict_feature_vector.py",
        "predict_per_atom.py"
        ],
    python_requires=">=3.6",
    install_requires=[
        "ase>=3.22.1",
        "matplotlib>=3.7.1",
        "numpy>=1.24.2",
        "pandas>=2.0.0",
        "pytorch_lightning>=1.9.4",
        "torch>=2.0.0"
        ],
    description="predict.py - prediction of docking score by Schnet DTNN",
    long_description="""
        Easy way to implement Schnet neural network predictions on already 
        trained model into your workflow."""
    )

