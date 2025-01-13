from manim import *
import numpy as np


class LaserPulse(VGroup):
    def __init__(
        self,
        start=LEFT*5,
        end=RIGHT*2,
        amplitude=0.2,      
        wave_freq=3.0,       
        color=GREEN,
        stroke_width=4,
        wave_speed=1.0,      
        **kwargs
    ):
        super().__init__(**kwargs)

        self.start = np.array(start)
        self.end   = np.array(end)
        self.amplitude    = amplitude
        self.wave_freq    = wave_freq
        self.color        = color
        self.stroke_width = stroke_width
        self.wave_speed   = wave_speed

        self.start_alpha = ValueTracker(0.0)
        self.end_alpha   = ValueTracker(0.0)

        self.phase_tracker = ValueTracker(0.0)

        self.beam = always_redraw(self._make_beam)

        self.add(self.beam)

    def _make_beam(self) -> ParametricFunction:
       
        start_alpha = self.start_alpha.get_value()
        end_alpha   = self.end_alpha.get_value()
        phase       = self.phase_tracker.get_value()

        if end_alpha < start_alpha:
            return ParametricFunction(
                lambda t: self.start,  
                t_range=[0, 0],
            )

        def param_func(t):
            line_pos = interpolate(self.start, self.end, t)
            direction = self.end - self.start
            dist = np.linalg.norm(direction)
            if dist == 0:
                return line_pos

            
            dir_hat = direction / dist

            perp = rotate_vector(dir_hat, 90 * DEGREES)
            distance_along = t * dist
            wave_argument = (self.wave_freq * distance_along) - (self.wave_speed * phase)
            
            
            offset = self.amplitude * np.sin(wave_argument)

            return line_pos + offset * perp

        return ParametricFunction(
            param_func,
            t_range = [start_alpha, end_alpha, 0.01],
            color = self.color,
            stroke_width = self.stroke_width,
        )


    def get_grow_animation(self, run_time=2.0):
     
        return self.end_alpha.animate.set_value(1).set_run_time(run_time)

    def get_retract_animation(self, run_time=2.0):
        return self.start_alpha.animate.set_value(1).set_run_time(run_time)

    def get_phase_animation(self, run_time=4.0, rate=1.0):
        return self.phase_tracker.animate.increment_value(rate).set_run_time(run_time)

'''example implemenation
class LaserScene(Scene):
    def construct(self):
  
        gun_outline = VMobject().set_points_as_corners([
            [-6,  0.2, 0],
            [-5.2,0.2, 0],
            [-5,  0,   0],
            [-5.2,-0.2,0],
            [-6,  -0.2,0],
            [-6,  0.2, 0],
        ])
        gun_outline.set_stroke(WHITE, 3)
        gun_label = Text("Laser", font_size=18).move_to([-5.6, 0, 0])
        self.add(gun_outline, gun_label)

        pulse = LaserPulse(
            start = np.array([-5, 0, 0]),
            end   = np.array([3, 0, 0]),
            amplitude = 0.2,
            wave_freq = 3,
            color = GREEN,
            stroke_width = 4,
            wave_speed = 2.0,  
        )
        self.add(pulse)

        self.play(
            pulse.get_grow_animation(run_time=2),
            pulse.get_phase_animation(run_time=2, rate=2)  
        )

       
        self.play(
            pulse.get_phase_animation(run_time=2, rate=4)
        )

        self.play(
            pulse.get_retract_animation(run_time=2),
            pulse.get_phase_animation(run_time=2, rate=2)
        )

        self.wait()
'''