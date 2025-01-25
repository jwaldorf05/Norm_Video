from manim import *
import numpy as np

# Class test code
# manim -pqh waveform.py My3DScene
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
        particle_opacity=1,
        **kwargs
    ):
      
        super().__init__(**kwargs)

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

        def default_wave_packet(t):
            '''Returns a set of coordinates np.array([x,y,z]) for some given
            parametric value t for the default wave function.'''
            x_val = t * self.x_span
            radius = self.r_max * np.exp(-(t**2) / (self.sigma**2))
            angle = 2 * np.pi * self.turns * self.frequency * t
            y_val = radius * np.cos(angle)
            z_val = radius * np.sin(angle)
            return np.array([x_val, y_val, z_val])
        
        self.wave_packet_func = formula if formula else default_wave_packet

        self.t_tracker = ValueTracker(-1)

        self.spiral = ParametricFunction(
            self.wave_packet_func,
            t_range=[-1, -1],
            color=self.color,
        )

        self.particle = Sphere(radius=0.05, color=self.particle_color).set_opacity(self.particle_opacity)
        self.particle.move_to(self.wave_packet_func(-1))

        def spiral_updater(mob):
            current_t = self.t_tracker.get_value()
            new_spiral = ParametricFunction(
                self.wave_packet_func,
                t_range=[-1, current_t],
                color=self.color
            )
            mob.become(new_spiral).rotate(x_angle * DEGREES, axis=RIGHT, about_point=ORIGIN).rotate(y_angle * DEGREES, axis=UP, about_point=ORIGIN).rotate(z_angle * DEGREES, axis=OUT, about_point=ORIGIN)
        
        self.spiral.add_updater(spiral_updater)

        def particle_updater(mob):
            current_t = self.t_tracker.get_value()
            mob.move_to(self.wave_packet_func(current_t))

        self.particle.add_updater(particle_updater)

        if self.show_axes:
            self.axes = ThreeDAxes(
                x_range=[-1, 1, 0.5],
                y_range=[-1, 1, 0.5],
                z_range=[-1, 1, 0.5],
                x_length=4,
                y_length=4,
                z_length=4,
            )
            self.add(self.axes)
        self.add(self.spiral, self.particle)
        self.shift(self.position)
        x_angle, y_angle, z_angle = self.orientation
        self.rotate(x_angle * DEGREES, axis=RIGHT, about_point=ORIGIN)
        self.rotate(y_angle * DEGREES, axis=UP, about_point=ORIGIN)
        self.rotate(z_angle * DEGREES, axis=OUT, about_point=ORIGIN)
    
        # def rotate_spiral(dt, rate, axis, spin_center):
        #     self.spiral.rotate(dt * 2 * PI * rate, axis=axis, about_point=spin_center)

    def get_spiral_animation(self, run_time=None, rate_func=smooth):
        '''Makes the wave equation rotate for run_time seconds.  '''
        if run_time is None:
            run_time = 5.0 / self.speed
        return self.t_tracker.animate.set_value(1).set_run_time(run_time).set_rate_func(rate_func)
        

    
    
    def precess_spiral(self, axis, rate, spin_center=ORIGIN):
        '''Makes the waveform '''
        self.spin_rate = rate
        self.spin_axis = axis
        self.spin_center = spin_center
        self.spiral.add_updater(lambda mob, dt: mob.rotate(dt * 2 * PI * self.spin_rate, axis=self.spin_axis, about_point=ORIGIN))
        
        
    def stop_precession(self):
        self.spiral.remove_updater(lambda mob, dt: mob.rotate(dt * 2 * PI * self.spin_rate, axis=self.spin_axis, about_point=self.spin_center))


# example implementation 
class My3DScene(ThreeDScene):
    def construct(self):
        spiral_mobject = WaveFunc3d(
            orientation=(75, 30, 0),
            position=ORIGIN,
            show_axes=True,
            speed=2.0,
            frequency=1.5,
            turns=5,
            r_max=0.5,
            sigma=0.4,
            x_span=1.5,
            color=BLUE,
            particle_color=RED,
        )
        self.add(spiral_mobject)
        self.set_camera_orientation(phi=70 * DEGREES, theta=35 * DEGREES, distance=6)
        self.play(spiral_mobject.get_spiral_animation(run_time=3))  
        spiral_mobject.add_updater(lambda mob, dt: mob.rotate(dt * 2 * PI, axis=UP))
        self.wait(5)
