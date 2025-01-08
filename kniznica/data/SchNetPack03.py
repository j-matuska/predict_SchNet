# -*- coding: utf-8 -*-

from schnetpack import AtomsConverter
from ase.io import read


def load_xyz(xyz_name):
    
    atoms = read(xyz_name, index=':')
    
    return atoms

# obsolete
# def load_converter(device = 'cpu'):
    
#     converter = AtomsConverter(device=device)

#     return converter
    