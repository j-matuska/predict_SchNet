# -*- coding: utf-8 -*-

from ase.io import read

def load_xyz(xyz_name: str):
    
    atoms = read(xyz_name, index=':')
    
    return atoms

def get_expected(atoms: list):
    
    # extreme comprehension
    # value DS will be 1e6 if the is no 
    expected_list = [{"name": str(at.info["name"]), "DS": float(at.info["energy"])} for at in atoms if "energy" in at.info]
    
    return expected_list