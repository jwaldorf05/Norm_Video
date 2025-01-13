from manim import *
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.animation as animation

class TaperedSpiral3D(ThreeDScene):
        def __init__(
                self,
                speed = 1.0,
                turns=4,
                r_max = 0.4,
                sigma = 0.3,
                x_span = 1.0,
                **kwargs
        ):
            super().__init__(**kwargs)
            self.speed = speed
            self.turns = turns
            self.r_max = r_max
            self.sigma = sigma
            self.x_span = x_span

            def construct(self):
              self.set_camera_orientation(phi=75*DEGREES, theta =30*DEGREES, distance=6)
              # Axes
              axes = ThreeDAxes(
                x_range=[-1,1,.5],
                y_range=[-1,1,.5],
                z_range=[-1,1,0.5],
                x_length=4, y_length=4, z_length =4,
                )
              self.add(axes)

              def wave_packet_func(t):
                x_val = t *self.x_span
                radius = self.r_max *np.exp(-(t**2)/(sigma**2))
                angle = self.turns *2*np.pi *t
                y_val = radius * np.cos(angle)
                z_val = radius * np.sin(angle)
                return np.array([x_val, y_val, z_val])
              
              spiral = ParametricFunction(
                 wave_packet_func, 
                 t_range = [-1,-1], # start "collapsed" at t=-1..-1
                 color = BLUE
              )  
              particle = Sphere(radius = 0.05, color=RED)
              particle.move_to(wave_packet_func(-1))
              
              t_tracker = ValueTracker(-1)
              def spiral_updater(mob):
                current_t = t_tracker.get_value()
                new_spiral = ParametricFunction(
                    wave_packet_func,
                    t_range=[-1, current_t],
                    color=BLUE
                )
                mob.become(new_spiral)
               
              spiral.add_updater(spiral_updater)

              def particle_updater(mob):
                current_t = t_tracker.get_value()
                mob.move_to(wave_packet_func(current_t))
              
              particle.add_updater(particle_updater)

              self.add(spiral, particle)
              run_time_value = 5.0/self.speed
              self.play(t_tracker.animate.set_value(1), run_time=run_time_value, rate_func=smooth)

              self.wait()

