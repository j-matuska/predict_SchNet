#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan  8 12:01:33 2025

@author: jamat
"""

from setuptools import setup

setup(
    name="predict",
    version="0.2",
    author="J. Matuska",
    url="https://github.com/j-matuska/predict_SchNet",
    #packages=find_packages("."),
    packages=[
        'kniznica',
        'kniznica.parser',
        'kniznica.data',
        'kniznica.model',
        'kniznica.output',
        ],
    package_dir={"": "."},
    package_data={
        'kniznica.model' : ["trained_models"]
        },
    scripts=[
        "predict.py"
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

