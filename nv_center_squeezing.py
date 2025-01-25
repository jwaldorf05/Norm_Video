from manim import *
import numpy as np
import random
import matplotlib as plt
# from waveform import * # waveform.py
from carbon_lattice import * # carbon_lattice.py
# from manim.opengl import *
# config.renderer="opengl"
# config.write_to_movie=True


# manim -pqh nv_center_squeezing.py NVCenter

class NVCenter(ThreeDScene):
    def construct(self):
        
        # Draw big diamond
        diamond_shape = VMobject()
        diamond_shape.set_points_as_corners([[-2,2,0], [2,2,0], [4, 0, 0], [0, -4, 0], [-4, 0, 0], [-2,2,0],]).set_stroke(color=WHITE, width=12).move_to([0,-.5,0])
        self.add(diamond_shape)
        self.set_camera_orientation(distance = 1000)
        
        
        
        # Define tetrahedron vertex positions
        a = 3  # Length scale for the tetrahedron
        lattice_xrange = [-1,0]
        lattice_yrange = [-1,0]
        lattice_zrange = [0]
        
        diamond_lattice = VGroup()
        lattice_bonds = VGroup()
        
        # Base objects
        base_sphere = Sphere(radius=a * 0.1,resolution=8, color=BLACK).move_to(a*np.array([0,0,0])).set_fill(color=BLACK, opacity=1)
        base_sphere.z_index = 2
        base_bonds = VGroup(
            Line([0 + (a * 0.1 /np.sqrt(3)),0 + (a * 0.1 /np.sqrt(3)),0 + (a * 0.1 /np.sqrt(3))],a*np.array([0.25 - ( 0.1 /np.sqrt(3)),0.25 - ( 0.1 /np.sqrt(3)),0.25 - ( 0.1 /np.sqrt(3))])),
            Line(a*np.array([0.25 + ( 0.1 /np.sqrt(3)),0.25 - ( 0.1 /np.sqrt(3)),0.25 + ( 0.1 /np.sqrt(3))]),a*np.array([0.5 - ( 0.1 /np.sqrt(3)), 0 + ( 0.1 /np.sqrt(3)), 0.5 - ( 0.1 /np.sqrt(3))])),
            Line(a*np.array([0.25 - ( 0.1 /np.sqrt(3)),0.25 + ( 0.1 /np.sqrt(3)),0.25 + ( 0.1 /np.sqrt(3))]),a*np.array([0 + ( 0.1 /np.sqrt(3)), 0.5 - ( 0.1 /np.sqrt(3)), 0.5 - ( 0.1 /np.sqrt(3))])),
            Line(a*np.array([0.25 + ( 0.1 /np.sqrt(3)),0.25 + ( 0.1 /np.sqrt(3)),0.25 - ( 0.1 /np.sqrt(3))]),a*np.array([0.5 - ( 0.1 /np.sqrt(3)), 0.5 - ( 0.1 /np.sqrt(3)), 0 + ( 0.1 /np.sqrt(3))])),
        )
        base_bonds.z_index = 1
        for x in lattice_xrange:
            for y in lattice_yrange:
                for z in lattice_zrange:
                    lattice_bonds.add(
                        base_bonds.copy().shift(0.5*a*np.array([x,y,z]))
                    )
        #Make the solid shape
        for x in range(lattice_xrange[0], lattice_xrange[-1] + 2):
            for y in range(lattice_yrange[0], lattice_yrange[-1] + 2):
                for z in range(lattice_zrange[0], lattice_zrange[-1] + 2):
                    diamond_lattice.add(
                        base_sphere.copy().shift(0.5*a*np.array([x,y,z]))
                    )
        for x in lattice_xrange:
            for y in lattice_yrange:
                for z in lattice_zrange:
                    diamond_lattice.add(
                        base_sphere.copy().shift(0.5*a*np.array([x+.5,y+.5,z+.5]))
                    )
                                
        diamond_lattice.scale(0.5).move_to([0,0,0])
        diamond_lattice.z_index = 2
        lattice_bonds.scale(0.5).move_to([0,0,0])
        lattice_bonds.z_index = 2
        # diamond_lattice.set_opacity(min(1, max(0, 1 - dist / lens_border.radius)))
        self.add(lattice_bonds, diamond_lattice)
        
        lens_border = Circle(radius=2, color=BLUE_B).set_stroke(width=6)
        handle = Rectangle(height=2.5, width=0.4, color=BLUE_B).set_fill(color=BLUE_B, opacity=1)
        lens_border.to_edge(LEFT, buff=-2)
        handle.next_to(lens_border, DOWN, buff=0)
        handle.rotate(PI / 6, about_point=lens_border.get_center())  # Rotate by 30 degrees

        self.play(AnimationGroup(FadeIn(lens_border), FadeIn(handle), lens_border.animate.move_to([0,0,0]), handle.animate.move_to([(2 * 0.5)+(1.25 * 0.5),(-2 * np.sqrt(3)/2) - (1.25 * np.sqrt(3)/2),0]), lag_ratio = 0.0),run_time=1)
        magnifying_glass = VGroup(lens_border, handle)
        
        self.wait(1)
        # Fade out diamond shape, and zoom in on the pattern

        self.play(FadeOut(diamond_shape, scale = 2), FadeOut(magnifying_glass, scale=2), diamond_lattice.animate.scale(2), lattice_bonds.animate.scale(2))
        
        # Rotate the camera for a more 3d view
        # self.move_camera(phi=62.5 * DEGREES, theta=-63.5 * DEGREES)
        self.wait(1)
        
        # Replace C with N, add vacancy
        replacement_location = np.array([0.75,-0.75,0])
        
        nitrogen = Sphere(radius=a * 0.1,resolution=8, color=BLUE, stroke_opacity=0).move_to(replacement_location).set_fill(color=BLUE, opacity=1)
        nitrogen.z_index = 2
        error_tolerance = 0.01
        
        for carbon in diamond_lattice:
            print(carbon.get_center().tolist())
            if (all(abs(a - b) <= error_tolerance for a, b in zip(np.array(carbon.get_center().tolist()), replacement_location))):
                a1 = Transform(carbon, nitrogen)
                
        for bond_group in lattice_bonds:
            for bond in bond_group:
                # print(bond.get_center().tolist())
                if all(abs(a - b) <= error_tolerance for a, b in zip(bond.get_center().tolist(), replacement_location + np.array([-0.375, 0.375, 0.375]))):
                    a2 = FadeOut(bond)
        
        NV_replacement = AnimationGroup(a1, a2)
        self.play(NV_replacement)
        vacancy_location = np.array([0,0,0.75])
        
        # Add nitrogen electron pair
        e1_pos = replacement_location + np.array([-0.25,0.25,0.25]) + np.array([0.09375, 0.09375, 0])
        e2_pos = replacement_location + np.array([-0.25,0.25,0.25]) - np.array([0.09375, 0.09375, 0])
        e1 = Sphere(radius=a * 0.025,resolution=8, color=BLUE, stroke_opacity=0).move_to(e1_pos).set_fill(color=BLUE, opacity=0.5)
        e2 = Sphere(radius=a * 0.025,resolution=8, color=BLUE, stroke_opacity=0).move_to(e2_pos).set_fill(color=BLUE, opacity=0.5)
        electron_pair = VGroup(e1, e2)
        electron_pair.z_index = 2
        self.play(FadeIn(electron_pair))
        
        # Create Vacancy
        for carbon in diamond_lattice:
            if all(abs(a - b) <= error_tolerance for a, b in zip(bond.get_center().tolist(), vacancy_location)):
                self.play(FadeOut(carbon))
        
        self.wait(1)
        # Move electron pair into hole, and make it into a spinning wave equation
        # wave_eq = waveform.
        self.play(electron_pair.animate.move_to(vacancy_location))
        x_angle, y_angle, z_angle = float(0.0), float(45.0), float(45.0)
        wave_eq = WaveFunc3d(
            orientation=(x_angle, y_angle, z_angle),
            position=vacancy_location,
            show_axes=False,
            speed=2.0,
            frequency=1.5,
            turns=5,
            r_max=0.5,
            sigma=0.4,
            x_span=1,
            color=BLUE,
            particle_color=RED,
            particle_opacity=0,
        )
        spin_dot = Dot(point= vacancy_location + np.array([1.0,0.0,0.0]))
        spin_dot.rotate(x_angle * DEGREES, axis=RIGHT, about_point= vacancy_location)
        spin_dot.rotate(y_angle * DEGREES, axis=UP, about_point= vacancy_location)
        spin_dot.rotate(z_angle * DEGREES, axis=OUT, about_point= vacancy_location)
        spin_loc = spin_dot.get_center()
        
        spin_arrow = Arrow3D(
            start=vacancy_location,
            end=vacancy_location + 0.2 * (spin_loc - vacancy_location),
            color=RED,
            thickness=0.015,
            height=0.06,
            base_radius=0.03,
        )

        # spin_arrow.rotate(x_angle * DEGREES, axis=RIGHT, about_point=[0,0,1.5])
        # spin_arrow.rotate(y_angle * DEGREES, axis=UP, about_point=[0,0,1.5])
        # spin_arrow.rotate(z_angle * DEGREES, axis=OUT, about_point=[0,0,1.5])

        self.add(spin_arrow)

        self.add(wave_eq)
        self.play(wave_eq.get_spiral_animation(run_time=2), FadeOut(electron_pair))  
        self.play(spin_arrow.animate.put_start_and_end_on(vacancy_location, spin_loc))
        # wave_particle = VGroup(wave_eq, spin_arrow)
        # wave_eq.add_updater(lambda mob, dt: mob.rotate(dt * 2 * PI, axis=UP, about_point=ORIGIN))
        # wave_eq.precess_spiral(axis=[0,1,0], rate=1, spin_center=vacancy_location)
        
        spin_arrow.add_updater(lambda mob, dt: mob.rotate(dt * 2 * PI, axis=UP, about_point=vacancy_location))
        wave_eq.spiral.add_updater(lambda mob, dt: mob.rotate(dt * 2 * PI, axis=UP, about_point=ORIGIN))
        
        
        # Spin the wave packet around
        
        self.wait(3)