from manim import *
import numpy as np
import random
import matplotlib as plt

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
        self.add(axes)
        
        phi_deg = 60
        theta_deg = 315
        
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
        particle_label = Text("p+", font_size=36).move_to(ORIGIN)
        
        spin_arrow = Arrow3D(
            start=ORIGIN,
            end=[sphere_radius,0,0],
            color=RED
        )
        
        spin_direction = np.array([1,0,0])
        
        self.add(sphere_mesh)
        self.add_fixed_orientation_mobjects(particle_label, x_label, y_label, z_label)
        
        
        # Create fixed orientation text objects to be used later
        north_label = Text("N", color=WHITE).scale(0.5).move_to([0.6,0,0])
        south_label = Text("S", color=WHITE).scale(0.5).move_to([-0.6,0,0])
        B_label_green = Tex(r'$\vec{B}$',color=GREEN).move_to([2,2,2])
        B_label_blue = Tex(r'$\vec{B}$',color=BLUE).move_to([2,2,2])
        self.fix_orientations(north_label,south_label)
        self.fix_in_frame(B_label_blue, B_label_green)
        
        self.set_camera_orientation(phi=phi_deg * DEGREES,theta=theta_deg * DEGREES, distance = 6)
        
        self.wait(1)
        self.play(Transform(particle_label,spin_arrow))
        
        # Create Magnetic Field
        
        
        # Define the dipole orientation (any arbitrary direction)
        dipole_direction = spin_direction  # Example: A diagonal vector
        dipole_direction = dipole_direction / np.linalg.norm(dipole_direction)  # Normalize
        
        def magnetic_field(pos):
            x, y, z = pos
            r = np.sqrt(x**2 + y**2 + z**2) + 1e-8  # Avoid division by zero
            m = 1  # Magnetic dipole moment
            mu_0 = 1  # Magnetic constant (scaled for visualization)

            # Project the position vector onto the dipole direction
            pos_vector = np.array([x, y, z])
            projection = np.dot(pos_vector, dipole_direction) * dipole_direction  # Parallel component
            perpendicular = pos_vector - projection  # Perpendicular component

            # Compute the magnetic field
            B = (
                mu_0 * m / (4 * np.pi * r**5) *
                (3 * np.dot(pos_vector, dipole_direction) * dipole_direction - pos_vector)
            )
            
            return B
        
        # stream_lines = StreamLines(
        #     magnetic_field,
        #     x_range=[-3, 3],
        #     y_range=[-3, 3],
        #     z_range=[-3, 3],
        #     stroke_width=2,
        #     padding=3,
        #     color=BLUE,
        #     max_anchors_per_line=50,
        # )
        # self.play(stream_lines.create())
        self.play(FadeIn(B_label_blue))
        self.wait(0.5)
        self.play(FadeOut(B_label_blue))
        
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
        
        magnet = VGroup(north_pole, south_pole) # initial magnet to trasnform into without labels
        
        self.wait(1)
        self.play(Transform(particle_label, magnet),FadeIn(north_label,south_label))
        
        particle_label.add(north_label,south_label)

        self.wait(1)
        
        def downward_field(pos):
            return np.array([0, 0, -4])  # All vectors point downward in the y-direction

        # Create the vector field
        # vector_field = ArrowVectorField(
        #     downward_field,
        #     three_dimensions=True,
        #     x_range=[-2, 2, 1],  # Define the x-axis range and spacing
        #     y_range=[-2, 2, 1],  # Define the y-axis range and spacing
        #     z_range=[-2, 2, 1],  # Define the y-axis range and spacing
        #     color=GREEN
        # )
        vector_field = VGroup()
        for x in np.arange(-2, 2.5, 1):
            for y in np.arange(-2, 2.5, 1):
                pos = np.array([x, y, 2])
                vector = downward_field(pos)
                arrow = Arrow3D(
                    start=pos,
                    end=pos + vector,  # Scale the vector to control arrow length
                    color=GREEN,
                )
                vector_field.add(arrow)

        # Add the vector field to the scene
        self.add(vector_field,B_label_green)
        # self.play(Create(vector_field),FadeIn(B_label_green))
        
        self.wait(1)
        
        self.move_camera(phi=0 * DEGREES, theta=270 * DEGREES)
        
        self.wait(1)
        
        # self.begin_ambient_camera_rotation(rate=0.1)
        # self.wait(5)
        # self.play(self.camera.animate.set_phi(PI / 4).set_theta(PI / 3))
        # self.play(self.camera.animate.set_camera_orientation(phi=70 * DEGREES,theta=30*DEGREES, distance = 6))
        
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
    