from manim import *
import numpy as np

class LaserPulse(VGroup):
    def __init__(
        self,
        start=LEFT * 5,
        end=RIGHT * 5,
        amplitude=0.5,
        sigma=1.0,
        freq=3.0,
        wave_speed=2.0,
        color=BLUE,
        stroke_width=3,
        **kwargs
    ):
        super().__init__(**kwargs)
        self.start_point = np.array(start, dtype=float)
        self.end_point   = np.array(end,   dtype=float)

        self.direction   = self.end_point - self.start_point
        self.length      = np.linalg.norm(self.direction)
        if self.length == 0:
            return
        self.direction /= self.length 
        self.amplitude  = amplitude
        self.sigma      = sigma
        self.freq       = freq
        self.wave_speed = wave_speed
        self.color      = color
        self.stroke_width = stroke_width

        self.time_tracker = ValueTracker(-3 * self.sigma / self.wave_speed)
        self.set_opacity(0)


        self.curve = always_redraw(self._make_pulse_curve)
        self.add(self.curve)

    def _make_pulse_curve(self):
        t = self.time_tracker.get_value()
        center_pos = self.wave_speed * t


        left_bound  = max(0, center_pos - 3*self.sigma)
        right_bound = min(self.length, center_pos + 3*self.sigma)

        if right_bound < left_bound:
            return ParametricFunction(lambda u: self.start_point, t_range=[0, 0])

        def param_func(u):
            x = interpolate(left_bound, right_bound, u)
            point_on_line = self.start_point + x * self.direction

            envelope = np.exp(-((x - center_pos)**2)/(2 * self.sigma**2))
            wave_arg = 2 * PI * self.freq * (x - center_pos)
            oscillation = np.sin(wave_arg)
            perp = rotate_vector(self.direction, 90 * DEGREES)

            offset = self.amplitude * envelope * oscillation
            return point_on_line + offset * perp

        return ParametricFunction(
            param_func,
            t_range=[0, 1, 0.01],
            color=self.color,
            stroke_width=self.stroke_width,
        )

    def animate_pulse(self, run_time=None):
        self.set_opacity(1)
        t_start = -3 * self.sigma / self.wave_speed
        t_end   = (self.length + 3*self.sigma) / self.wave_speed
        self.time_tracker.set_value(t_start)
        if run_time is None:
            run_time = t_end - t_start

        return self.time_tracker.animate(run_time=run_time).set_value(t_end)
'''
example implementation
        start_point = np.array([-5, 0, 0])
        end_point   = np.array([ 3, 0, 0])
        pulse = LaserPulse(
            start=start_point,
            end=end_point,
            amplitude=0.4,
            sigma=0.4,
            freq=3.0,
            wave_speed=1.0,  
            color=GREEN,
            stroke_width=3
        )
        self.add(pulse)
        self.play(pulse.animate_pulse(run_time=8))
        self.wait()
'''