from manim import *
import numpy as np

class WaveFunc3d(VGroup):
    def __init__(
        self,
        orientation=(0, 0, 0),
        position=ORIGIN,
        show_axes=True,
        speed=1.0,
        frequency=1.0,
        turns=4,
        r_max=0.4,
        sigma=0.3,
        x_span=1.0,
        formula=None,
        color=BLUE,
        particle_color=RED,
        particle_opacity=1.0,
        arrow_color=YELLOW,
        arrow_scale=0.3,
        **kwargs
    ):
        """
        A 3D wavefunction spiral with:

         - A 'spiral' (ParametricFunction) from t=-1..+1
         - A moving 'particle' (Sphere)
         - An 'arrow' at the origin that follows e^{i theta} or some param in the XY-plane
         - The entire group can be oriented & shifted, so it behaves like one object.

        Parameters
        ----------
        orientation : (x_deg, y_deg, z_deg)
            Euler angles in degrees for an initial rotation about (X, Y, Z).
        position : np.ndarray
            Shift the entire wavefunction in 3D.
        show_axes : bool
            Whether to show an internal ThreeDAxes.
        speed : float
            Affects the default spiral run_time (5.0 / speed).
        frequency, turns, r_max, sigma, x_span, formula, etc.
            Standard spiral parameters.
        color : Color
            Spiral color.
        particle_color : Color
            Moving sphere color.
        particle_opacity : float
            Opacity of the sphere (0 => invisible).
        arrow_color : Color
            The color of the small arrow.
        arrow_scale : float
            Scale factor for the arrow size.
        """
        super().__init__(**kwargs)

        # ------------------------------------------------------------
        # 1) Store parameters
        # ------------------------------------------------------------
        self.orientation = orientation
        self.position = position
        self.show_axes = show_axes
        self.speed = speed
        self.frequency = frequency
        self.turns = turns
        self.r_max = r_max
        self.sigma = sigma
        self.x_span = x_span
        self.color = color
        self.particle_color = particle_color
        self.particle_opacity = particle_opacity
        self.arrow_color = arrow_color
        self.arrow_scale = arrow_scale

        # Default wave-packet if no formula is supplied
        def default_wave_packet(t):
            x_val = t * self.x_span
            radius = self.r_max * np.exp(-(t**2) / (self.sigma**2))
            angle = 2 * np.pi * self.turns * self.frequency * t
            y_val = radius * np.cos(angle)
            z_val = radius * np.sin(angle)
            return np.array([x_val, y_val, z_val])

        self.wave_packet_func = formula if formula else default_wave_packet

        # ------------------------------------------------------------
        # 2) Parametric Spiral + Particle
        # ------------------------------------------------------------
        self.t_tracker = ValueTracker(-1)

        self.spiral = ParametricFunction(
            self.wave_packet_func,
            t_range=[-1, -1],  # collapsed initially
            color=self.color,
        )

        self.particle = Sphere(radius=0.05, color=self.particle_color)
        self.particle.set_opacity(self.particle_opacity)
        self.particle.move_to(self.wave_packet_func(-1))

        # Spiral updater
        def spiral_updater(mob):
            current_t = self.t_tracker.get_value()
            new_spiral = ParametricFunction(
                self.wave_packet_func,
                t_range=[-1, current_t],
                color=self.color
            )
            mob.become(new_spiral)

        self.spiral.add_updater(spiral_updater)

        # Particle updater
        def particle_updater(mob):
            current_t = self.t_tracker.get_value()
            mob.move_to(self.wave_packet_func(current_t))

        self.particle.add_updater(particle_updater)

        # ------------------------------------------------------------
        # 3) Optionally show internal 3D axes
        # ------------------------------------------------------------
        if self.show_axes:
            self.axes = ThreeDAxes(
                x_range=[-1, 1, 0.5],
                y_range=[-1, 1, 0.5],
                z_range=[-1, 1, 0.5],
                x_length=4, y_length=4, z_length=4,
            )
            self.add(self.axes)

        # ------------------------------------------------------------
        # 4) A small "flow arrow" at the origin that tracks e^{i theta}
        # ------------------------------------------------------------
        self.arrow_theta = ValueTracker(0)  # we'll animate or update this
        # A simple 3D arrow from origin to (somewhere in x-y plane)
        # We'll just make an Arrow3D from (0,0,0) to (arrow_scale, 0, 0) initially
        self.flow_arrow = Arrow3D(
            start=ORIGIN,
            end=self.arrow_scale * RIGHT,
            color=self.arrow_color,
            thickness=0.01,
        )

        # Updater to revolve the arrow tip around the origin in the XY-plane
        def arrow_updater(mob):
            theta = self.arrow_theta.get_value()
            # We place tip at arrow_scale * [cos(theta), sin(theta), 0]
            new_tip = self.arrow_scale * np.array([np.cos(theta), np.sin(theta), 0])
            mob.put_start_and_end_on(ORIGIN, new_tip)

        self.flow_arrow.add_updater(arrow_updater)

        # Add spiral, particle, arrow
        self.add(self.spiral, self.particle, self.flow_arrow)

        # ------------------------------------------------------------
        # 5) Shift + Rotate the entire group (so arrow, spiral, etc. move together)
        # ------------------------------------------------------------
        x_angle, y_angle, z_angle = self.orientation
        self.rotate(x_angle * DEGREES, axis=RIGHT, about_point=ORIGIN)
        self.rotate(y_angle * DEGREES, axis=UP, about_point=ORIGIN)
        self.rotate(z_angle * DEGREES, axis=OUT, about_point=ORIGIN)
        self.shift(self.position)

    # ----------------------------------------------------------------
    # PUBLIC METHODS
    # ----------------------------------------------------------------

    def get_spiral_animation(self, run_time=None, rate_func=smooth):
        """
        Animates the drawing of the spiral from t=-1 to t=+1.
        """
        if run_time is None:
            run_time = 5.0 / self.speed
        return self.t_tracker.animate.set_value(1).set_run_time(run_time).set_rate_func(rate_func)

    def get_arrow_animation(self, theta_end=TAU, run_time=2, rate_func=linear):
        """
        Animate the arrow's phase from 0 to theta_end (like e^{i theta}).
        If you want to start from something other than 0, set self.arrow_theta.set_value(...) first.
        """
        return self.arrow_theta.animate.set_value(theta_end).set_run_time(run_time).set_rate_func(rate_func)

    def precess_spiral(self, axis=UP, rate=0.5, spin_center=ORIGIN):
        """
        Continuously rotates the spiral about 'axis' at 'rate' revolutions per second, 
        and also rotates the arrow with it, since they are all in one VGroup.
        """
        # This is a continuous rotation, done by an updater on the entire group 'self'.
        self.add_updater(
            lambda mob, dt: mob.rotate(dt * 2 * PI * rate, axis=axis, about_point=spin_center)
        )

    def stop_precession(self):
        """
        Removes the continuous rotation updater from the wavefunction group.
        """
        self.clear_updaters()


class My3DScene(ThreeDScene):
    def construct(self):
        wave = WaveFunc3d(
            orientation=(0, 0, 0),
            position=ORIGIN,
            show_axes=True,
            speed=1.5,
            frequency=1.0,
            turns=4,
            r_max=0.5,
            sigma=0.3,
            x_span=1.0,
            color=BLUE,
            particle_color=RED,
            arrow_color=YELLOW,
            arrow_scale=0.5,
        )
        self.add(wave)
        self.set_camera_orientation(phi=70*DEGREES, theta=30*DEGREES, distance=5)

        self.play(wave.get_spiral_animation(run_time=3))

        self.play(wave.get_arrow_animation(theta_end=TAU, run_time=2))

        self.wait(1)

        wave.precess_spiral(axis=OUT, rate=0.25)  # 0.25 rev/sec
        self.wait(6)
        wave.stop_precession()

        self.wait(2)

