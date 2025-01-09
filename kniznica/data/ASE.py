# -*- coding: utf-8 -*-

from ase.io import read

def load_xyz(xyz_name: str):
    
    atoms = read(xyz_name, index=':')
    
    return atoms

def get_expected(atoms: list):
    
    # extreme comprehension
    # value DS will be 1e6 if the is no 
    # else added to cover new version of ASE where "energy" is keyword and it is imported to core of Atoms object
    # in future modification to custom keyword have to be implemented
    expected_list = [{"name": str(at.info["name"]), "DS": float(at.info["energy"])} if "energy" in at.info else {"name": str(at.info["name"]), "DS": at.get_total_energy()} for at in atoms]
    
    return expected_list