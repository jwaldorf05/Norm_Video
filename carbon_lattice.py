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
        atom_color=BLACK,
        bond_color=WHITE,
        **kwargs
    ):
        self.lattice_xrange = lattice_xrange
        self.lattice_yrange = lattice_yrange
        self.lattice_zrange = lattice_zrange
        self.scaling = scaling
        self.atom_color = atom_color
        self.bond_color = bond_color
        
        self.diamond_lattice = VGroup()
        self.lattice_bonds = VGroup()
        
        # Base objects
        base_sphere = Sphere(radius=self.scaling * 0.1,resolution=8, color=BLACK).move_to(ORIGIN).set_fill(color=BLACK, opacity=1)
        base_sphere.z_index = 2
        base_bonds = VGroup(
            Line([0 + (self.scaling * 0.1 /np.sqrt(3)),0 + (self.scaling * 0.1 /np.sqrt(3)),0 + (self.scaling * 0.1 /np.sqrt(3))], self.scaling*np.array([0.25 - ( 0.1 /np.sqrt(3)),0.25 - ( 0.1 /np.sqrt(3)),0.25 - ( 0.1 /np.sqrt(3))])),
            Line(self.scaling*np.array([0.25 + ( 0.1 /np.sqrt(3)),0.25 - ( 0.1 /np.sqrt(3)),0.25 + ( 0.1 /np.sqrt(3))]),self.scaling*np.array([0.5 - ( 0.1 /np.sqrt(3)), 0 + ( 0.1 /np.sqrt(3)), 0.5 - ( 0.1 /np.sqrt(3))])),
            Line(self.scaling*np.array([0.25 - ( 0.1 /np.sqrt(3)),0.25 + ( 0.1 /np.sqrt(3)),0.25 + ( 0.1 /np.sqrt(3))]),self.scaling*np.array([0 + ( 0.1 /np.sqrt(3)), 0.5 - ( 0.1 /np.sqrt(3)), 0.5 - ( 0.1 /np.sqrt(3))])),
            Line(self.scaling*np.array([0.25 + ( 0.1 /np.sqrt(3)),0.25 + ( 0.1 /np.sqrt(3)),0.25 - ( 0.1 /np.sqrt(3))]),self.scaling*np.array([0.5 - ( 0.1 /np.sqrt(3)), 0.5 - ( 0.1 /np.sqrt(3)), 0 + ( 0.1 /np.sqrt(3))])),
        )
        base_bonds.z_index = 1
        for x in lattice_xrange:
            for y in lattice_yrange:
                for z in lattice_zrange:
                    self.lattice_bonds.add(
                        base_bonds.copy().shift(0.5*self.scaling*np.array([x,y,z]))
                    )
        #Make the solid shape
        for x in range(lattice_xrange[0], lattice_xrange[-1] + 2):
            for y in range(lattice_yrange[0], lattice_yrange[-1] + 2):
                for z in range(lattice_zrange[0], lattice_zrange[-1] + 2):
                    self.diamond_lattice.add(
                        base_sphere.copy().shift(0.5*self.scaling*np.array([x,y,z]))
                    )
        for x in lattice_xrange:
            for y in lattice_yrange:
                for z in lattice_zrange:
                    self.diamond_lattice.add(
                        base_sphere.copy().shift(0.5*self.scaling*np.array([x+.5,y+.5,z+.5]))
                    )
                                
        self.diamond_lattice.move_to([0,0,0])
        self.diamond_lattice.z_index = 2
        self.lattice_bonds.move_to([0,0,0])
        self.lattice_bonds.z_index = 2

        

        
    def remove_atom(self, pos):
        '''Fades Out the atom at position pos'''
        for carbon in self.diamond_lattice:
            if (carbon.get_center().tolist() == pos):
                FadeOut(carbon)
        
    def remove_bond(self, pos):
        '''Fades Out the bond at position pos'''
        for bond_group in self.lattice_bonds:
            for bond in bond_group:
                # print(bond.get_center().tolist())
                error_tolerance = 0.01
                if all(abs(a - b) <= error_tolerance for a, b in zip(bond.get_center().tolist(), pos)):
                    FadeOut(bond)
        
    def replace_atom(self, pos, replacement=Sphere):
        '''Replaces the atom at position pos with another 
        sphere object, usually of a different color or size
        '''
        new_atom = replacement
        new_atom.z_index = 2
        
        for carbon in self.diamond_lattice:
            if (carbon.get_center().tolist() == pos):
                Transform(carbon, new_atom)
        
