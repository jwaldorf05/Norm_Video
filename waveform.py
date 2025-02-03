from manim import *
import numpy as np

class WaveFunc3d(VGroup):
    """
    A class to create a 3D wave function visualized as a spiral curve.
    Includes options for showing axes and adding a directional arrow.

    Attributes:
        orientation (tuple): The rotation (x, y, z) of the wave in degrees.
        position (np.array): The position of the wave in the 3D space.
        show_axes (bool): Whether to display axes.
        param_range (tuple): The range of the parameter (min, max) for the spiral curve.
        frequency (float): The frequency of the wave.
        turns (int): The number of turns in the spiral.
        r_max (float): The maximum radius of the spiral.
        sigma (float): The Gaussian envelope parameter.
        x_span (float): The x-axis span of the wave.
        spiral_color (Color): The color of the spiral.
        arrow_color (Color): The color of the arrow.
        arrow_show (bool): Whether to show an arrow at the spiral's end/start.
        arrow_endpoint (str): Determines if the arrow points to the "start" or "end" of the spiral.
    """

    def __init__(
        self,
        orientation=(0, 0, 0), 
        position=ORIGIN,
        show_axes=False,
        param_range=(-1, 1),
        frequency=1.0,
        turns=4,
        r_max=0.4,
        sigma=0.3,
        x_span=1.0,
        spiral_color=BLUE,
        arrow_color=YELLOW,
        arrow_show=True,
        arrow_endpoint="end",  
        **kwargs
    ):
        super().__init__(**kwargs)

        # Initialize attributes
        self.orientation = orientation
        self.position = position
        self.show_axes = show_axes
        self.param_range = param_range
        self.frequency = frequency
        self.turns = turns
        self.r_max = r_max
        self.sigma = sigma
        self.x_span = x_span
        self.spiral_color = spiral_color
        self.arrow_color = arrow_color
        self.arrow_show = arrow_show
        self.arrow_endpoint = arrow_endpoint

        # Create the spiral function
        self._spiral_func = self._make_spiral_func()

        # Add optional axes
        if self.show_axes:
            self.axes = ThreeDAxes(
                x_range=[-1, 1],
                y_range=[-1, 1],
                z_range=[-1, 1],
                x_length=4,
                y_length=4,
                z_length=4,
            )
            self.add(self.axes)

        # Add the spiral
        t_min, t_max = self.param_range
        self.spiral = ParametricFunction(
            self._spiral_func,
            t_range=(t_min, t_max),
            color=self.spiral_color
        ).set_z_index(1)  # Ensure spiral appears behind other elements like arrows
        self.add(self.spiral)

        # Add the directional arrow
        if self.arrow_show:
            start_pt = self._spiral_func(t_min)
            end_pt = self._spiral_func(t_max)
            arrow_target = end_pt if (self.arrow_endpoint.lower() == "end") else start_pt

            self.arrow = Arrow3D(
                start=ORIGIN,
                end=arrow_target,
                color=self.arrow_color,
                thickness=0.02,
            ).set_z_index(2)  # Ensure arrow is always on top
            self.add(self.arrow)
        else:
            self.arrow = None

        # Apply orientation and position adjustments
        x_angle_deg, y_angle_deg, z_angle_deg = self.orientation
        self.rotate(x_angle_deg * DEGREES, axis=RIGHT, about_point=ORIGIN)
        self.rotate(y_angle_deg * DEGREES, axis=UP, about_point=ORIGIN)
        self.rotate(z_angle_deg * DEGREES, axis=OUT, about_point=ORIGIN)
        self.shift(self.position)

    def _make_spiral_func(self):
        """
        Creates the mathematical function representing the spiral.

        Returns:
            function: A parametric function of t that outputs (x, y, z) coordinates.
        """
        def spiral_func(t):
            x_val = t * self.x_span
            envelope = self.r_max * np.exp(-(t**2)/(self.sigma**2))  # Gaussian envelope
            angle = 2 * np.pi * self.turns * self.frequency * t  # Angular frequency
            y_val = envelope * np.cos(angle)
            z_val = envelope * np.sin(angle)
            return np.array([x_val, y_val, z_val])
        return spiral_func

    def animate_spiral_creation(self, run_time=3, rate_func=smooth):
        """
        Animates the creation of the spiral curve.

        Args:
            run_time (float): Duration of the animation.
            rate_func (function): The easing function for the animation.

        Returns:
            Animation: The animation object for creating the spiral.
        """
        t_min, t_max = self.param_range
        tracker = ValueTracker(t_min)
        # if self.arrow_show:
        #     self.remove(self.arrow)

        # Remove existing spiral and add a collapsed version
        self.remove(self.spiral)
        collapsed_spiral = ParametricFunction(
            self._spiral_func,
            t_range=(t_min, t_min),
            color=self.spiral_color
        )
        self.spiral = collapsed_spiral
        self.spiral.set_z_index(1)
        self.add(self.spiral)

        # Define updater to dynamically extend the spiral
        def partial_draw_updater(mob):
            current_t = tracker.get_value()
            new_spiral = ParametricFunction(
                self._spiral_func,
                t_range=(t_min, current_t),
                color=self.spiral_color
            )
            new_spiral.rotate(self.orientation[0] * DEGREES, axis=RIGHT, about_point=ORIGIN)
            new_spiral.rotate(self.orientation[1] * DEGREES, axis=UP, about_point=ORIGIN)
            new_spiral.rotate(self.orientation[2] * DEGREES, axis=OUT, about_point=ORIGIN)
            new_spiral.shift(self.position)
            mob.become(new_spiral.set_z_index(1))  # Keep spiral layered properly

        self.spiral.add_updater(partial_draw_updater)

        # Animate the tracker value to grow the spiral
        if self.arrow_show:
            anim = AnimationGroup(tracker.animate.set_value(t_max).set_run_time(run_time).set_rate_func(rate_func), Write(self.arrow))
        else:
            anim = tracker.animate.set_value(t_max).set_run_time(run_time).set_rate_func(rate_func)
        # if self.arrow_show:
        #     anim = AnimationGroup(anim, GrowArrow(self.arrow))
        return anim

    def reconfigure_wave(self, new_sigma=None, new_rmax=None):
        """
        Reconfigures the wave by updating sigma and/or r_max.

        Args:
            new_sigma (float): The new sigma value for the Gaussian envelope.
            new_rmax (float): The new maximum radius of the spiral.
        """
        if new_sigma is not None:
            self.sigma = new_sigma
        if new_rmax is not None:
            self.r_max = new_rmax

        t_min, t_max = self.param_range

        # Remove the current spiral and arrow
        self.remove(self.spiral)
        if self.arrow is not None:
            self.remove(self.arrow)

        # Create a new spiral with updated parameters
        updated_func = self._make_spiral_func()
        new_spiral = ParametricFunction(updated_func, t_range=(t_min, t_max), color=self.spiral_color)
        self.spiral = new_spiral.move_to(self.position)
        self.spiral.set_z_index(1)
        self.add(self.spiral)

        # Add a new arrow with updated endpoints
        if self.arrow_show:
            start_pt = updated_func(t_min)
            end_pt = updated_func(t_max)
            arrow_target = end_pt if (self.arrow_endpoint == "end") else start_pt
            new_arrow = Arrow3D(ORIGIN, arrow_target, color=self.arrow_color, thickness=0.02)
            self.arrow = new_arrow
            self.arrow.set_z_index(2)  # Ensure arrow is layered above the spiral
            self.add(self.arrow)


class ExampleScene(ThreeDScene):
    """
    Example scene demonstrating the WaveFunc3d class.
    Includes animations and transformations.
    """
    def construct(self):
        # Create a WaveFunc3d object
        wave_obj = WaveFunc3d(
            orientation=(45, 0, 0),
            position=ORIGIN,
            show_axes=True,
            param_range=(-1,1),
            frequency=1.5,
            turns=3,
            r_max=0.5,
            sigma=0.25,
            x_span=1,
            spiral_color=BLUE,
            arrow_color=YELLOW,
            arrow_show=True,
            arrow_endpoint="end",
        )
        self.add(wave_obj)

        # Set camera orientation
        self.set_camera_orientation(phi=70*DEGREES, theta=30*DEGREES, distance=6)

        # Animate the spiral creation
        self.play(wave_obj.animate_spiral_creation(run_time=3))
        self.wait(1)

        # Optionally remove the updater after the animation
        wave_obj.spiral.clear_updaters()

        # Scale transformation
        self.play(wave_obj.animate.scale(1.5))
        self.wait(1)

        # Adjust the wave by reconfiguring sigma
        wave_obj.reconfigure_wave(new_sigma=0.2)
        self.wait(2)

        # Rotate the group about the Z-axis
        self.play(Rotate(wave_obj, angle=PI/2, axis=OUT), run_time=2)
        self.wait()



# from manim import *
# import numpy as np

# class WaveFunc3d(VGroup):
#     def __init__(
#         self,
#         orientation=(0, 0, 0), 
#         position=ORIGIN,
#         show_axes=False,
#         param_range=(-1, 1),
#         frequency=1.0,
#         turns=4,
#         r_max=0.4,
#         sigma=0.3,
#         x_span=1.0,
#         spiral_color=BLUE,
#         arrow_color=YELLOW,
#         arrow_show=True,
#         arrow_endpoint="end",  
#         **kwargs
#     ):
#         super().__init__(**kwargs)

#         self.orientation = orientation
#         self.position = position
#         self.show_axes = show_axes
#         self.param_range = param_range
#         self.frequency = frequency
#         self.turns = turns
#         self.r_max = r_max
#         self.sigma = sigma
#         self.x_span = x_span
#         self.spiral_color = spiral_color
#         self.arrow_color = arrow_color
#         self.arrow_show = arrow_show
#         self.arrow_endpoint = arrow_endpoint

#         self._spiral_func = self._make_spiral_func()

#         if self.show_axes:
#             self.axes = ThreeDAxes(
#                 x_range=[-1, 1],
#                 y_range=[-1, 1],
#                 z_range=[-1, 1],
#                 x_length=4,
#                 y_length=4,
#                 z_length=4,
#             )
#             self.add(self.axes)

#         t_min, t_max = self.param_range
#         self.spiral = ParametricFunction(
#             self._spiral_func,
#             t_range=(t_min, t_max),
#             color=self.spiral_color
#         ).set_z_index(1)
#         self.add(self.spiral)

#         if self.arrow_show:
#             start_pt = self._spiral_func(t_min)
#             end_pt = self._spiral_func(t_max)
#             arrow_target = end_pt if (self.arrow_endpoint.lower() == "end") else start_pt

#             self.arrow = Arrow3D(
#                 start=ORIGIN,
#                 end=arrow_target,
#                 color=self.arrow_color,
#                 thickness=0.02,
#             ).set_z_index(2)
#             self.add(self.arrow)
#         else:
#             self.arrow = None

#         x_angle_deg, y_angle_deg, z_angle_deg = self.orientation
#         self.rotate(x_angle_deg * DEGREES, axis=RIGHT, about_point=ORIGIN)
#         self.rotate(y_angle_deg * DEGREES, axis=UP, about_point=ORIGIN)
#         self.rotate(z_angle_deg * DEGREES, axis=OUT, about_point=ORIGIN)
#         self.shift(self.position)

#     def _make_spiral_func(self):
#         def spiral_func(t):
#             x_val = t * self.x_span
#             envelope = self.r_max * np.exp(-(t**2)/(self.sigma**2))
#             angle = 2 * np.pi * self.turns * self.frequency * t
#             y_val = envelope * np.cos(angle)
#             z_val = envelope * np.sin(angle)
#             return np.array([x_val, y_val, z_val])
#         return spiral_func


#     def animate_spiral_creation(self, run_time=3, rate_func=smooth):
        
#         t_min, t_max = self.param_range

#         tracker = ValueTracker(t_min)

#         self.remove(self.spiral)

#         collapsed_spiral = ParametricFunction(
#             self._spiral_func,
#             t_range=(t_min, t_min),
#             color=self.spiral_color
#         )
#         self.spiral = collapsed_spiral
#         self.spiral.set_z_index(1)
#         self.add(self.spiral)

#         def partial_draw_updater(mob):
#             current_t = tracker.get_value()
#             new_spiral = ParametricFunction(
#                 self._spiral_func,
#                 t_range=(t_min, current_t),
#                 color=self.spiral_color
#             )
#             new_spiral.rotate(self.orientation[0] * DEGREES, axis=RIGHT, about_point=ORIGIN)
#             new_spiral.rotate(self.orientation[1] * DEGREES, axis=UP, about_point=ORIGIN)
#             new_spiral.rotate(self.orientation[2] * DEGREES, axis=OUT, about_point=ORIGIN)
#             new_spiral.shift(self.position)
#             mob.become(new_spiral.set_z_index(1))

#         self.spiral.add_updater(partial_draw_updater)

#         anim = tracker.animate.set_value(t_max).set_run_time(run_time).set_rate_func(rate_func)

#         return anim

#     def reconfigure_wave(self, new_sigma=None, new_rmax=None):
    
#         if new_sigma is not None:
#             self.sigma = new_sigma
#         if new_rmax is not None:
#             self.r_max = new_rmax

#         t_min, t_max = self.param_range

#         self.remove(self.spiral)
#         if self.arrow is not None:
#             self.remove(self.arrow)

#         updated_func = self._make_spiral_func()
#         new_spiral = ParametricFunction(updated_func, t_range=(t_min, t_max), color=self.spiral_color)
#         self.spiral = new_spiral.move_to(self.position)
#         self.spiral.set_z_index(1)
#         self.add(self.spiral)

#         if self.arrow_show:
#             start_pt = updated_func(t_min)
#             end_pt = updated_func(t_max)
#             arrow_target = end_pt if (self.arrow_endpoint == "end") else start_pt
#             new_arrow = Arrow3D(ORIGIN, arrow_target, color=self.arrow_color, thickness=0.02)
#             self.arrow = new_arrow
#             self.arrow.set_z_index(2)
#             self.add(self.arrow)



# class ExampleScene(ThreeDScene):
#     def construct(self):
#         wave_obj = WaveFunc3d(
#             orientation=(45, 0, 0),
#             position=ORIGIN,
#             show_axes=True,
#             param_range=(-1,1),
#             frequency=1.5,
#             turns=3,
#             r_max=0.5,
#             sigma=0.25,
#             x_span=1,
#             spiral_color=BLUE,
#             arrow_color=YELLOW,
#             arrow_show=True,
#             arrow_endpoint="end",
#         )
#         self.add(wave_obj)

#         self.set_camera_orientation(phi=70*DEGREES, theta=30*DEGREES, distance=6)

#         # Animate the spiral 'creation'
#         self.play(wave_obj.animate_spiral_creation(run_time=3))
#         self.wait(1)
        
#         # Optionally remove the updater after creation is done:
#         wave_obj.spiral.clear_updaters()

#         # Try a transform
#         self.play(wave_obj.animate.scale(1.5))
#         self.wait(1)

#         # Re-squish the wave by adjusting sigma:
#         wave_obj.reconfigure_wave(new_sigma=0.2)
#         self.wait(2)

#         # Rotate the entire group about Z:
#         self.play(Rotate(wave_obj, angle=PI/2, axis=OUT), run_time=2)
#         self.wait()
