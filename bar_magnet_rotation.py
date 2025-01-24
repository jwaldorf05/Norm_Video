from manim import *
import numpy as np
import random
import matplotlib as plt
from magnetic_field import * # magnetic_field.py


# Camera Fix from https://gist.github.com/abul4fia/1419b181e8e3410ef78e6acc25c3df94#file-fixed_fixing-py-L13

# manim -pqh bar_magnet_rotation.py DipoleRotation --disable_caching

class MyCamera(ThreeDCamera):
    def transform_points_pre_display(self, mobject, points):
        if getattr(mobject, "fixed", False):
            return points
        else:
            return super().transform_points_pre_display(mobject, points)

def make_fixed(*mobs):
    for mob in mobs:
        mob.fixed = True
        for submob in mob.family_members_with_points():
            submob.fixed = True

class DipoleRotation(ThreeDScene):
    def __init__(self, camera_class=MyCamera, ambient_camera_rotation=None,
                 default_angled_camera_orientation_kwargs=None, **kwargs):
        super().__init__(camera_class=camera_class, **kwargs)
    
    def construct(self):
        axes = ThreeDAxes(x_range=[-2,2],y_range=[-2,2],z_range=[-2,2],x_length=4,y_length=4,z_length=4)
        
        phi_deg = 60
        theta_deg = 315
        
        rotation_tracker = ValueTracker(0) # For tracking how far the magnet has spun
        
        def rotate_and_track(mob, dt):
            """Rotates the Mobject about the z hat direction, at 'rate' rotations per second"""
            angle_increment = dt * magnet_spin_rate.get_value() * 2 * PI  # Rotation increment per frame
            mob.rotate(angle_increment, axis=OUT)
            rotation_tracker.increment_value(angle_increment)
        
        sphere_radius = 1
        sphere_mesh = Surface(
            lambda u, v: self.sphere_param(u,v,sphere_radius),
            u_range = [0,PI],
            v_range=[0,TAU],
            resolution=(12,24)
        )
        sphere_mesh.set_style(
            stroke_width=1,
            stroke_opacity=0.3,
            fill_opacity=0.1
        )
        sphere_mesh.set_color(GRAY_A)
        
        # Axes labels
        x_label = Text("x").scale(0.4).move_to([2.2,0,0])
        y_label = Text("y").scale(0.4).move_to([0,2.2,0])
        z_label = Text("z").scale(0.4).move_to([0,0,2.2])
        
        # Proton label
        particle_label = Text("proton", font_size=36).move_to([0,1.5,0])
        
        spin_direction = np.array([1,0,0])
        
        spin_arrow = Arrow3D(
            start=ORIGIN,
            end=1.5*spin_direction,
            color=RED,
            # resolution=(2,16)
        )

        self.add(sphere_mesh)
        self.add_fixed_in_frame_mobjects(particle_label)
        self.add_fixed_orientation_mobjects(x_label, y_label, z_label)
        self.remove(x_label, y_label, z_label)
        
        
        # Create fixed orientation text objects to be used later
        north_label = Text("N", color=WHITE).scale(0.5).move_to([0.6,0,0])
        south_label = Text("S", color=WHITE).scale(0.5).move_to([-0.6,0,0])
        B_label_green = Tex(r'$\vec{B}$',color=GREEN).move_to([2.5,2.5,2.5])
        B_label_blue = Tex(r'$\vec{B}$',color=BLUE).move_to([2.5,2.5,2.5])
        # self.fix_orientations(north_label,south_label)
        self.fix_in_frame(B_label_blue, B_label_green)
        
        self.set_camera_orientation(phi=phi_deg * DEGREES,theta=theta_deg * DEGREES)
        
        self.play(FadeOut(particle_label))
        self.play(Write(axes), Write(x_label), Write(y_label), Write(z_label))
        self.wait(1)
        self.play(Create(spin_arrow))
        
        # Create Magnetic Field
        
        # Define the dipole orientation (any arbitrary direction)
        dipole_direction = spin_direction  # Example: A diagonal vector
        dipole_direction = dipole_direction / np.linalg.norm(dipole_direction)  # Normalize
        
        
        dipole_moment = np.array([1, 0, 0], dtype=float)
        dipole_center = np.array([0, 0, 0], dtype=float)
        scale_factor  = 0.05  
        
        seed_points = []
        x_top = 1.1
        # for radius in [0.1]:  
        radius = 1
        for angle_deg in [0, 30, 60, 90, 120, 150, 180, 210, 240, 270, 300, 330]:
        # for angle_deg in [0, 90, 180, 270]:
            angle = angle_deg * DEGREES
            y = radius * np.cos(angle)
            z = radius * np.sin(angle)
            seed_points.append(np.array([x_top, y, z]))

        field_lines = []
        for seed in seed_points:
            plus_trace = trace_field_line(
                start_point=seed,
                field_func=lambda p: dipole_field(
                    p, dipole_moment, dipole_center, scale_factor
                ),
                step_size=0.03,
                n_steps=12000,
                direction=+1
            )
            minus_trace = trace_field_line(
                start_point=seed,
                field_func=lambda p: dipole_field(
                    p, dipole_moment, dipole_center, scale_factor
                ),
                step_size=0.03,
                n_steps=12000,
                direction=-1
            )

            plus_line  = create_field_line_from_points(plus_trace,  color=BLUE, width=2)
            minus_line = create_field_line_from_points(minus_trace, color=BLUE, width=2)
            field_lines.extend([plus_line, minus_line])
        
        
        self.play(FadeIn(B_label_blue), FadeIn(*field_lines))
        self.wait(0.5)
        self.play(FadeOut(B_label_blue), FadeOut(*field_lines))
        
        # Create the bar magnet
        magnet_length = 1.6
        magnet_width = 0.4
        magnet_height = 0.4
        
        # Create the bar magnet (two halves for poles)
        north_pole = Prism(
            dimensions=[magnet_length/2, magnet_width, magnet_height],
            fill_color=BLUE,
            fill_opacity=0.8
        ).shift(LEFT * magnet_length / 4)

        south_pole = Prism(
            dimensions=[magnet_length/2, magnet_width, magnet_height],
            fill_color=RED,
            fill_opacity=0.8
        ).shift(RIGHT * magnet_length / 4)
        
        magnet_bar = VGroup(north_pole, south_pole) # initial magnet to trasnform into without labels
        
        self.wait(1)
        self.play(Transform(spin_arrow, magnet_bar),FadeIn(north_label,south_label))

        self.remove(spin_arrow)
        magnet = VGroup(north_pole, south_pole, north_label, south_label)
        self.add(magnet)

        self.wait(1)
        
        downward_field = lambda pos: IN
        
        magnet_spin_rate = ValueTracker(1)
        
        def length_func(length):
            return 0.45 * sigmoid(length)
        vector_field = ArrowVectorField(downward_field, x_range=[-2,2,0.5], y_range=[-2,2,0.5], color=GREEN, length_func=length_func).shift(1*OUT)
        vector_field_2 = ArrowVectorField(downward_field, x_range=[-2,2,0.5], y_range=[-2,2,0.5], color=GREEN, length_func=length_func).shift(1*OUT)
        def double_length_func(length):
            return 2 * 0.45 * sigmoid(length)
        long_vector_field = ArrowVectorField(downward_field, x_range=[-2,2,0.5], y_range=[-2,2,0.5], color=GREEN, length_func=double_length_func).shift(1*OUT)
        [vector.rotate(theta_deg * DEGREES, axis=OUT) for vector in vector_field]
        [vector.rotate(theta_deg * DEGREES, axis=OUT) for vector in long_vector_field]
        [vector.rotate(theta_deg * DEGREES, axis=OUT) for vector in vector_field_2]
        
        dot_field = VGroup()
        for x in np.arange(-2, 2.25, 0.5):
            for y in np.arange(-2, 2.25, 0.5):
                pos = np.array([x, y, 1])
                dot = Dot(
                    point=pos,
                    color=GREEN,
                    radius=0.05
                )
                dot_field.add(dot)

        # Add the vector field to the scene
        self.play(Create(vector_field),FadeIn(B_label_green))
        
        # Rotate the prism about its z-axis (or any axis you choose)
        magnet_spin_rate.set_value(0.5)
        magnet.add_updater(lambda mob, dt: rotate_and_track(mob, dt))
        
        self.wait(1)
        
        self.play(
            Transform(vector_field, long_vector_field),B_label_green.animate.set_stroke(width=2), magnet_spin_rate.animate.set_value(1))
        
        self.wait(1)
        self.play(
            Transform(vector_field, vector_field_2),B_label_green.animate.set_stroke(width=.5), magnet_spin_rate.animate.set_value(0.5))

        # magnet.clear_updaters()
        # magnet.add_updater(lambda mob, dt: rotate_and_track(mob, dt, rate=.5))
        
        
        self.wait(1.25)
        
        magnet_spin_rate.set_value(0)
        self.move_camera(phi=0 * DEGREES, theta=270 * DEGREES, added_anims=[FadeOut(z_label), FadeOut(axes.z_axis), Transform(vector_field, dot_field)])
        
        self.wait(1)
        
        precession_clock_tracker = ValueTracker(0) # For tracking how far the magnet has spun
        
        theta_label = Tex(r"$\theta_1$").move_to([1.4 * np.cos(rotation_tracker.get_value()),1.4 * np.sin(rotation_tracker.get_value()),0]).scale(0.5)
        theta_marker = Line(start=[1 * np.cos(rotation_tracker.get_value()),1 * np.sin(rotation_tracker.get_value()),0], end=[1.2 * np.cos(rotation_tracker.get_value()),1.2 * np.sin(rotation_tracker.get_value()),0])
        t_marker = MarkupText(text = f"t = {precession_clock_tracker.get_value()}.00 s", font_size=36).move_to([4.25, 0, 0])
        t_marker.add_updater(
            lambda mob: mob.become(MarkupText(f"t = {precession_clock_tracker.get_value():.2f} s").move_to([4.25, 0, 0]))
        )
        
        def update_time(dt):
            precession_clock_tracker.increment_value(dt)
        
        inside_dots = VGroup()
        outside_dots = VGroup()
        for x in np.arange(-2, 2.25, 0.5):
            for y in np.arange(-2, 2.25, 0.5):
                pos = np.array([x, y, 1])
                dot = Dot(
                    point=pos,
                    color=GREEN,
                    radius=0.05
                )
                if np.linalg.norm([x,y,0]) <= 1.1:
                    inside_dots.add(dot)
                else:
                    outside_dots.add(dot)
                
        self.remove(vector_field)
        self.add(inside_dots, outside_dots)
        
        self.play(Write(theta_label), Write(theta_marker), Write(t_marker), inside_dots.animate.set_opacity(0.5))
        self.wait(1)

        magnet_spin_rate.set_value(0.25)
        self.add_updater(update_time)
        
        self.wait(1.01)

        magnet.clear_updaters()
        self.remove_updater(update_time)
        
        theta2_label = Tex(r"$\theta_2$").move_to([1.4 * np.cos(rotation_tracker.get_value()),1.4 * np.sin(rotation_tracker.get_value()),0]).scale(0.5)
        theta2_marker = Line(start=[1 * np.cos(rotation_tracker.get_value()),1 * np.sin(rotation_tracker.get_value()),0], end=[1.2 * np.cos(rotation_tracker.get_value()),1.2 * np.sin(rotation_tracker.get_value()),0])
        self.play(Write(theta2_label), Write(theta2_marker))
        self.wait(1)
        
        omega_eq = Tex(r"$\omega = \Delta \theta / \Delta t$").move_to([-4,0.5,0])
        B_eq = Tex(r"$B = \omega / \gamma$").move_to([-4,-0.5,0])
        
        const_label = Text("constant", font_size=24, color=BLUE).move_to([-3.2,-1.5,0])
        const_arrow = Vector([0,0.5,0], color=BLUE).move_to([-3.2,-1.1,0])
        self.play(FadeIn(omega_eq, shift=LEFT), FadeIn(B_eq, shift=LEFT))
        self.play(Write(const_label), Write(const_arrow), B_eq[0][4].animate.set_color(BLUE), run_time=1)
        
        self.wait(1)
        
        self.play(FadeOut(*self.mobjects),FadeOut(t_marker))
        
        
    def sphere_param(self, u, v, R):
        x = R * np.sin(u) * np.cos(v)
        y = R * np.sin(u) * np.sin(v)
        z = R * np.cos(u)
        return np.array([x, y, z])

    def fix_orientations(self, *mob):
        # camera_orientation = self.camera.generate_rotation_matrix()
        # for obj in mob:
        #     obj.apply_matrix(camera_orientation)
        self.add_fixed_orientation_mobjects(*mob)
        self.remove(*mob)
        
    def fix_in_frame(self, *mob):
        self.add_fixed_in_frame_mobjects(*mob)
        self.remove(*mob)