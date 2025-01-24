from manim import *
import numpy as np

class TaperedSpiral3D(ThreeDScene):
    def __init__(
        self,
        orientation=(75 * DEGREES, 30 * DEGREES),
        distance=6,
        position=ORIGIN,
        show_axes=True,
        speed=1.0,
        frequency=1.0,
        turns=4,
        r_max=0.4,
        sigma=0.3,
        x_span=1.0,
        formula=None,
        **kwargs
    ):
        super().__init__(**kwargs)
        self.orientation = orientation
        self.distance = distance
        self.position = position
        self.show_axes = show_axes
        self.speed = speed
        self.frequency = frequency
        self.turns = turns
        self.r_max = r_max
        self.sigma = sigma
        self.x_span = x_span
        self.formula = formula

    def construct(self):
        phi, theta = self.orientation
        self.set_camera_orientation(phi=phi, theta=theta, distance=self.distance)
        if self.show_axes:
            axes = ThreeDAxes(
                x_range=[-1, 1, 0.5],
                y_range=[-1, 1, 0.5],
                z_range=[-1, 1, 0.5],
                x_length=4, y_length=4, z_length=4,
            )
            axes.move_to(self.position)
            self.add(axes)

        def default_wave_packet_func(t):
            x_val = t * self.x_span
            radius = self.r_max * np.exp(-(t ** 2) / (self.sigma ** 2))
            angle = 2 * np.pi * self.turns * self.frequency * t
            y_val = radius * np.cos(angle)
            z_val = radius * np.sin(angle)
            return np.array([x_val, y_val, z_val])

        wave_packet_func = self.formula if self.formula else default_wave_packet_func
        spiral = ParametricFunction(
            wave_packet_func,
            t_range=[-1, -1],
            color=BLUE,
        )
        spiral.shift(self.position)

        particle = Sphere(radius=0.05, color=RED)
        particle.move_to(wave_packet_func(-1) + self.position)

        t_tracker = ValueTracker(-1)

        def spiral_updater(mob):
            current_t = t_tracker.get_value()
            new_spiral = ParametricFunction(
                wave_packet_func,
                t_range=[-1, current_t],
                color=BLUE
            )
            new_spiral.shift(self.position)
            mob.become(new_spiral)

        spiral.add_updater(spiral_updater)

        def particle_updater(mob):
            current_t = t_tracker.get_value()
            mob.move_to(wave_packet_func(current_t) + self.position)

        particle.add_updater(particle_updater)

        self.add(spiral, particle)
        run_time_value = 5.0 / self.speed
        self.play(t_tracker.animate.set_value(1), run_time=run_time_value, rate_func=smooth)
        self.wait()
