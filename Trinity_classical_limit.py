from manim import * 
import numpy as np

class ClassicalLimitAnimation(ThreeDScene):
    def construct(self):
        self.set_camera_orientation(phi=70 * DEGREES,theta=30*DEGREES, distance = 6)
        sphere_radius = 2
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

        #Axes labels
        x_label = Text("x").scale(0.4).move_to([sphere_radius+0.3,0,0])
        y_label = Text("y").scale(0.4).move_to([0,sphere_radius+0.3,0])
        z_label = Text("z").scale(0.4).move_to([0,0,sphere_radius+0.3])

        arrow_3d = Arrow3D(
            start=ORIGIN,
            end=[0,0,sphere_radius],
            color=RED
        )

        self.add(sphere_mesh, arrow_3d, x_label, y_label, z_label)
        self.wait(1)

        self.play(
            arrow_3d.animate.rotate(0.2, axis=UR),
            run_time=1
        )
        self.play(
            arrow_3d.animate.rotate(-0.4,axis=UR),
            run_time=1
        )
        self.play(
            arrow_3d.animate.rotate(0.2,axis=UR),
            run_time=1
        )

        self.play(
            FadeOut(arrow_3d, shift=0.1 *UP),
            sphere_mesh.animate.set_opacity(0.05),
            run_time=1
        )

        wave_3d = Surface(
            lambda u, v: self.gaussian_3d(u,v, amplitude=1.5, spread=1.0),
            u_range = [-2,2],
            v_range=[-2,2],
            resolution=(40,40)
        )
        wave_3d.set_style(fill_opacity=0.6, stroke_opacity=0.2)
        wave_3d.set_color(BLUE_E)

        self.play(FadeIn(wave_3d,scale=0.5), run_time=2)
        self.wait(1)

        wave_line_2d = self.create_1d_wave_function(x_min=-4, x_max = 4)
        wave_line_2d.move_to(DOWN*2)

        self.play(
            ReplacementTransform(wave_3d, wave_line_2d),
            run_time=2
        )
        self.wait(1)

        schrodinger_eq = MathTex(r"-\frac{\hbar^2}{2m}\nabla^2 \psi + V\psi = i\hbar \frac{\partial \psi}{\partial t}")
        self.add_fixed_in_frame_mobjects(schrodinger_eq)
        schrodinger_eq.to_corner(UL)
        self.play(FadeIn(schrodinger_eq, shift=UP), run_time=1)
        self.wait(1)

        bracket_left = Line(UP, DOWN).set_stroke(width=5).move_to(LEFT*5 + DOWN*2)
        bracket_right = Line(UP, DOWN).set_stroke(width=5).move_to(LEFT*5 + DOWN*2)
        bracket_right.rotate(PI)
        bracket = VGroup(bracket_left, bracket_right).move_to(LEFT*5 + DOWN*2)

        self.play(FadeIn(bracket, shift=LEFT), run_time=1)
        self.play(
            bracket.animate.move_to(ORIGIN + DOWN*2),  # center on wave
            run_time=2
        )

        wave_line_2d = Line(LEFT * 4, RIGHT * 4)  # Example placeholder

        # Stretch the wave_line_2d about its center
        self.play(
            wave_line_2d.animate.stretch(0.3, 0, about_point=wave_line_2d.get_center()),
            run_time=1
        )

        # Create the momentum wave
        momentum_wave = self.create_1d_wave_function(x_min=-4, x_max=4, color=RED, amplitude=0.2)
        momentum_wave.move_to(DOWN * 3.5)

        # Scale the momentum wave about its center
        momentum_wave.scale(0.3, about_point=momentum_wave.get_center())

        self.play(FadeIn(momentum_wave, shift=DOWN), run_time=1)

        # Broaden the momentum wave about its center
        self.play(
            momentum_wave.animate.stretch(5, 0, about_point=momentum_wave.get_center()),
            run_time=2
        )

        self.wait(1)

        self.play(FadeOut(bracket, shift=RIGHT), run_time = 1)

        self.play(
            FadeOut(wave_line_2d),
            FadeOut(momentum_wave),
            FadeOut(schrodinger_eq),
            sphere_mesh.animate.set_opacity(0.3),
            run_time=2
        )
        ensemble_arrows = VGroup()
        n_spins =6
        for i in range(n_spins):
            theta = np.random.uniform(0,PI)
            phi = np.random.uniform(0,TAU)
            direction = self.spherical_to_cartesian(sphere_radius*0.9, theta, phi)
            arrow = Arrow3D(ORIGIN, direction).set_color(BLUE)
            ensemble_arrows.add(arrow)

        self.play(
            FadeIn(ensemble_arrows, scale = 0.5), 
            run_time=2
        )
        self.wait(1)

        def squeeze_updater(mob, alpha):
            for i, arrow in enumerate(mob):
                end = arrow.get_end()
                r = np.linalg.norm(end)
                x, y, z = end /r if r !=0 else (0,0,1)

                z_new = z * (1 -0.8*alpha)
                y_new = y * (1+0.5*alpha)
                new_end = np.array([x*r, y_new*r, z_new*r])

                arrow.put_start_and_end_on(ORIGIN, new_end)

        self.play(UpdateFromAlphaFunc(ensemble_arrows, squeeze_updater), run_time=3)
        self.wait(1)

        spin_squeeze_eq = MathTex(r"\Delta J_{\perp} \sim \frac{1}{\sqrt{N}}")
        self.add_fixed_in_frame_mobjects(spin_squeeze_eq)
        spin_squeeze_eq.to_edge(UP)
        self.play(Write(spin_squeeze_eq), run_time=2)
        self.wait(2)

        self.play(
            FadeOut(ensemble_arrows),
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

    def create_1d_wave_function(self, x_min=-4, x_max=4, color=BLUE, amplitude=1.0):
        func = lambda x: amplitude * np.exp(-0.1*x**2) * np.sin(2*x)
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

    def spherical_to_cartesian(self, r, theta, phi):
        x = r * np.sin(theta) * np.cos(phi)
        y = r * np.sin(theta) * np.sin(phi)
        z = r * np.cos(theta)
        return np.array([x, y, z])


