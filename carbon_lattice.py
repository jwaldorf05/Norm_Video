from manim import *
import numpy as np
import random
import matplotlib as plt

class CarbonLattice(VGroup):
    def __init__(
        self,
        lattice_xrange = [-1,0],
        lattice_yrange = [-1,0],
        lattice_zrange = [-1,0],
        scaling=3.0,
        wave_speed=2.0,
        atom_color=BLACK,
        bond_color=WHITE,
        **kwargs
    ):
        

        
    def remove_atom(self, pos):
        '''Removes the atom at position pos'''
        
        
    def remove_bond(self, pos):
        '''Removes the bond at position pos'''
        
        
    def replace_atom(self, pos, replacement=Sphere):
        '''Replaces the atom at position pos with another 
        sphere object, usually of a different color or size
        '''
        
        
    