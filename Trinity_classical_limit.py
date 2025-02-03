from manim import * 
import numpy as np
from waveform import * 

# manim -pqh Trinity_classical_limit.py ClassicalLimitAnimation
class ClassicalLimitAnimation(ThreeDScene):
    def construct(self):
        
        # rotation_tracker = ValueTracker(0.0) # For tracking how far the vector has spun
        axis_x = ValueTracker(1.0)
        axis_y = ValueTracker(0.0)
        axis_z = ValueTracker(0.0)
        vector_spin_rate = ValueTracker(1.0)
        sphere_shake_rate = ValueTracker(20)
        sphere_shake_amplitude = ValueTracker(0.5)
        
        def rotate_spin_vector(mob, dt):
            """Rotates the Mobject about the 'rotation_axis', at 'rate' rotations per second"""
            angle_increment = dt * vector_spin_rate.get_value() * 2 * PI  # Rotation increment per frame
            rotation_axis = np.array([axis_x.get_value(),axis_y.get_value(),axis_z.get_value()])
            mob.rotate(angle_increment, axis=rotation_axis, about_point=ORIGIN)
            # rotation_tracker.increment_value(angle_increment)

        # def shake_object(mob, dt):
        #     """Shakes Mobject about the 'shake_direction', at 'rate' cycles per second"""
        #     movement_increment = sphere_shake_amplitude.get_value() * dt * np.cos(dt * sphere_shake_rate.get_value() * 2 * PI)  # Rotation increment per frame
        #     mob.shift(movement_increment * UP)
        
        
        self.set_camera_orientation(phi=80 * DEGREES,theta=30*DEGREES, distance = 6)
        sphere_radius = float(2)
        sphere_mesh = Surface(
            lambda u, v: self.sphere_param(u,v,sphere_radius),
            u_range = [0,PI],
            v_range=[0,TAU],
            resolution=(24,48)
        )
        sphere_mesh.set_style(
            stroke_width=1,
            stroke_opacity=0.3,
            fill_opacity=0.1
        )
        sphere_mesh.set_color(BLUE)
        
        particle_label = Text("particle", font_size=36).move_to([0,2.5,0]) # Particle label

        #Axes labels
        x_label = Text("x").scale(0.4).move_to([sphere_radius+0.3,0,0])
        y_label = Text("y").scale(0.4).move_to([0,sphere_radius+0.3,0])
        z_label = Text("z").scale(0.4).move_to([0,0,sphere_radius+0.3])

        arrow_3d = Arrow3D(
            start=ORIGIN,
            end=np.array([0,0,sphere_radius]),
            color=RED
        )

        self.add(sphere_mesh, arrow_3d)
        self.add_fixed_in_frame_mobjects(particle_label)
        # self.add_fixed_orientation_mobjects(x_label, y_label, z_label)
        self.wait(1)
        
        arrow_3d.add_updater(lambda mob, dt: rotate_spin_vector(mob, dt))
        # arrow_3d.add_updater(lambda mob, dt: shake_object(mob, dt))
        # sphere_mesh.add_updater(lambda mob, dt: shake_object(mob, dt))
        
        vector_spin_rate.set_value(0.6)
        sphere_shake_amplitude.set_value(0.5)
        self.wait(0.25)
        vector_spin_rate.set_value(-1.2)
        sphere_shake_amplitude.set_value(1)
        self.wait(0.25)
        vector_spin_rate.set_value(0.6)
        sphere_shake_amplitude.set_value(0.5)
        self.wait(0.25)
        vector_spin_rate.set_value(0)

        # wave_3d = Surface(
        #     lambda u, v: self.gaussian_3d(u,v, amplitude=1.5, spread=1.0),
        #     u_range = [-2,2],
        #     v_range=[-2,2],
        #     resolution=(40,40)
        # )
        # wave_3d.set_style(fill_opacity=0.6, stroke_opacity=0.2).set_color(BLUE_E)
        
        # wave_line_3d = self.create_2d_wave_function(x_min=-4, x_max = 4).rotate(PI/2, axis=[0,1,0], about_point=ORIGIN).rotate(PI/2, axis=[1,0,0], about_point=ORIGIN)
        # wave_line_3d = WaveFunc3d(
        #     orientation=(75, 30, 0),
        #     position=ORIGIN,
        #     show_axes=False,
        #     speed=2.0,
        #     frequency=1.5,
        #     turns=5,
        #     r_max=0.5,
        #     sigma=0.4,
        #     x_span=1.5,
        #     color=BLUE,
        #     particle_color=RED,
        # )
        wave_line_3d = WaveFunc3d(
            orientation=(75, 30, 0),
            position=ORIGIN,
            show_axes=False,
            param_range=(-3,3),
            frequency=1.5,
            turns=3,
            r_max=2,
            sigma=0.4,
            x_span=1.5,
            spiral_color=BLUE,
            arrow_color=RED,
            arrow_show=False,
            arrow_endpoint="end",
        )
        wave_line_spin = Arrow3D(
            start=ORIGIN,
            end=np.array([0,1,0]),
            color=RED
        )

        self.play(
            FadeOut(arrow_3d),
            # ReplacementTransform(sphere_mesh, wave_line_3d),
            run_time=1
        )
        self.wait(1)
        

        schrodinger_eq = MathTex(r"-\frac{\hbar^2}{2m}\nabla^2 \psi + V\psi = i\hbar \frac{\partial \psi}{\partial t}")
        self.add_fixed_in_frame_mobjects(schrodinger_eq)
        schrodinger_eq.to_corner(UL)
        self.play(FadeIn(schrodinger_eq, shift=UP), FadeIn(wave_line_spin), run_time=0.5)
        wave_line_3d.add_updater(lambda mob, dt: mob.rotate(dt * 2 * PI, axis=[0,1,0], about_point=ORIGIN))
        
        self.wait(1)
        
        wave_line_2d = self.create_1d_wave_function(x_min=-4, x_max = 4).rotate(PI/2, axis=[0,1,0], about_point=ORIGIN).rotate(PI/2, axis=[1,0,0], about_point=ORIGIN)
        # wave_line_2d.move_to(IN*2)

        self.play(
            FadeOut(wave_line_3d),
            FadeIn(wave_line_2d),
            # ReplacementTransform(wave_line_3d, wave_line_2d),
            run_time=2
        )
        self.wait(1)
        
        position_label = Text('Position', font_size=36).move_to([0,0,3])
        momentum_label = Text('Position', font_size=36).move_to([0,0,-1])
        self.play(FadeIn(position_label, momentum_label))

        # bracket_left = Line(UP, DOWN).set_stroke(width=5).move_to(LEFT*5 + DOWN*2)
        # bracket_right = Line(UP, DOWN).set_stroke(width=5).move_to(LEFT*5 + DOWN*2)
        # bracket_right.rotate(PI)
        # bracket = VGroup(bracket_left, bracket_right).move_to(LEFT*5 + DOWN*2)

        # self.play(FadeIn(bracket, shift=LEFT), run_time=1)
        # self.play(
        #     bracket.animate.move_to(ORIGIN + DOWN*2),  # center on wave
        #     run_time=2
        # )

        # wave_line_2d = Line(LEFT * 4, RIGHT * 4)  # Example placeholder

        # # Stretch the wave_line_2d about its center
        # self.play(
        #     wave_line_2d.animate.stretch(0.3, 0, about_point=wave_line_2d.get_center()),
        #     run_time=1
        # )

        # # Create the momentum wave
        # momentum_wave = self.create_1d_wave_function(x_min=-4, x_max=4, color=RED, amplitude=0.2)
        # momentum_wave.move_to(DOWN * 3.5)

        # # Scale the momentum wave about its center
        # momentum_wave.scale(0.3, about_point=momentum_wave.get_center())

        # self.play(FadeIn(momentum_wave, shift=DOWN), run_time=1)

        # # Broaden the momentum wave about its center
        # self.play(
        #     momentum_wave.animate.stretch(5, 0, about_point=momentum_wave.get_center()),
        #     run_time=2
        # )

        # self.wait(1)

        # self.play(FadeOut(bracket, shift=RIGHT), run_time = 1)

        # self.play(
        #     FadeOut(wave_line_2d),
        #     FadeOut(momentum_wave),
        #     FadeOut(schrodinger_eq),
        #     sphere_mesh.animate.set_opacity(0.3),
        #     run_time=2
        # )
        # ensemble_arrows = VGroup()
        # n_spins =6
        # for i in range(n_spins):
        #     theta = np.random.uniform(0,PI)
        #     phi = np.random.uniform(0,TAU)
        #     direction = self.spherical_to_cartesian(sphere_radius*0.9, theta, phi)
        #     arrow = Arrow3D(ORIGIN, direction).set_color(BLUE)
        #     ensemble_arrows.add(arrow)

        # self.play(
        #     FadeIn(ensemble_arrows, scale = 0.5), 
        #     run_time=2
        # )
        # self.wait(1)

        def squeeze_updater(mob, alpha):
            for i, arrow in enumerate(mob):
                end = arrow.get_end()
                r = np.linalg.norm(end)
                x, y, z = end /r if r !=0 else (0,0,1)

                z_new = z * (1 -0.8*alpha)
                y_new = y * (1+0.5*alpha)
                new_end = np.array([x*r, y_new*r, z_new*r])

                arrow.put_start_and_end_on(ORIGIN, new_end)

        # self.play(UpdateFromAlphaFunc(ensemble_arrows, squeeze_updater), run_time=3)
        # self.wait(1)

        spin_squeeze_eq = MathTex(r"\Delta J_{\perp} \sim \frac{1}{\sqrt{N}}")
        self.add_fixed_in_frame_mobjects(spin_squeeze_eq)
        spin_squeeze_eq.to_edge(UP)
        self.play(Write(spin_squeeze_eq), run_time=2)
        self.wait(2)

        self.play(
            # FadeOut(ensemble_arrows),
            FadeOut(spin_squeeze_eq),
            FadeOut(sphere_mesh),
            FadeOut(x_label),
            FadeOut(y_label),
            FadeOut(z_label),
            run_time=2
        )
        self.wait()


    def sphere_param(self, u, v, R):
        x = R * np.sin(u) * np.cos(v)
        y = R * np.sin(u) * np.sin(v)
        z = R * np.cos(u)
        return np.array([x, y, z])

    def gaussian_3d(self, x, y, amplitude=1, spread=1.0):
        z = amplitude * np.exp(-((x**2 + y**2)/(2*spread**2)))
        return np.array([x, y, z])

    def create_1d_wave_function(self, x_min=-4, x_max=4, color=BLUE_E, amplitude=1.0, spread = 5, twist = 0.5):
        func = lambda x: amplitude * np.exp(-(1/spread) * x**2) * np.cos(2 * PI * twist * x)
        resolution = 200
        points = []
        for i in range(resolution + 1):
            x = x_min + (x_max - x_min)*i/resolution
            y = func(x)
            points.append([x, y, 0])
        wave_line = VMobject()
        wave_line.set_points_as_corners(points)
        wave_line.set_stroke(color, width=2)
        return wave_line
    
    def create_2d_wave_function(self, x_min=-4, x_max=4, color=BLUE_E, amplitude=1.0, spread = 5, twist = 0.5):
        func = lambda x: [amplitude * np.exp(-(1/spread) * x**2) * np.cos(2 * PI * twist * x), amplitude * np.exp(-(1/spread) * x**2) * np.sin(2 * PI * twist * x)]
        resolution = 200
        points = []
        for i in range(resolution + 1):
            x = x_min + (x_max - x_min)*i/resolution
            y = func(x)[0]
            z = func(x)[0]
            points.append([x, y, z])
        wave_line = VMobject()
        wave_line.set_points_as_corners(points)
        wave_line.set_stroke(color, width=2)
        return wave_line

    def spherical_to_cartesian(self, r, theta, phi):
        x = r * np.sin(theta) * np.cos(phi)
        y = r * np.sin(theta) * np.sin(phi)
        z = r * np.cos(theta)
        return np.array([x, y, z])


