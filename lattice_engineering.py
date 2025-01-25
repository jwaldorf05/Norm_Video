from manim import *
import numpy as np
import random
from laserbeam import * # laserbeam.py
# from manim_voiceover import *

# from manim_voiceover.services.azure import AzureService
# from manim_voiceover.services.recorder import RecorderService
# from manim_voiceover.services.coqui import CoquiService

# manim -pqh lattice_engineering.py Lattice_Engineering_Animation

class Lattice_Engineering_Animation(Scene):
    def construct(self):
        # self.set_speech_service(AzureService(voice="en-US-AriaNeural",style="newscast-casual",global_speed=1.25)) # MS Azure Voice
        
        # self.set_speech_service(RecorderService())
        # self.set_speech_service(CoquiService(model_name="tts_models/en/ljspeech/tacotron2-DDC", global_speed=1.25))
        
        # Show a bunch of NV center white dots
        # Define the square
        square = Square(side_length=4)
        square.set_stroke(color=BLUE, width=2)
        square.set_fill(color=BLACK, opacity=1)  # Optional fill for better contrast
        
        nv_label = Text("NV Center Diamond", font_size=36).move_to([0, 2.4 ,0])

        # Generate 100 white dots within the square
        dots = VGroup()  # Group to hold all the dots
        for _ in range(100):
            # Generate random (x, y) within the square's bounds
            x = random.uniform(-1.95, 1.95)  # Slight margin from the edge
            y = random.uniform(-1.95, 1.95)

            # Create a dot and position it
            dot = Dot(point=[x, y, 0], color=WHITE, radius=.03)
            dots.add(dot)

        dots_spawning = AnimationGroup([FadeIn(dots[index],run_time=(0.05 - 0.05*(random.randint(1,50)/100))) for index in np.arange(len(dots))],lag_ratio=1)
        # Add the dots to the scene
        # for index in np.arange(len(dots)):
        #     num = random.randint(1,50)
        #     FadeIn(dots[index],run_time=(0.05 - 0.05*(num/100)))
            # self.wait(0.05 - 0.05*(num/100))
            
        init_group = AnimationGroup(Write(square), FadeIn(nv_label), dots_spawning, lag_ratio=1)
        # Add the square to the scene
        with self.voiceover(text="We developed a technique called lattice engineering to address this problem and create usable ordered structures of Nitrogen Vacancy Centers") as tracker:
            self.play(init_group, run_time = tracker.duration)
        
        # Turn the dimers red, and then back to white
        
        dimers = VGroup()
        normals = VGroup()
        
        # Separating the dots into dimers and normal NV Centers
        for i, dot1 in enumerate(dots):
            close_to_others = False
            for j, dot2 in enumerate(dots):
                if i != j:  # Avoid comparing the dot with itself
                    distance = np.linalg.norm(dot1.get_center() - dot2.get_center())
                    if distance < 0.1:
                        close_to_others = True
                        break  # Stop checking further neighbors for this dot
            if close_to_others:
                dimers.add(dot1)
            else:
                normals.add(dot1)
        
        self.wait(1)
        dimer_mark = AnimationGroup(
            dimers.animate.scale(2),  # Grow
            dimers.animate.set_color(RED),
            # self.wait(1),
            # dimers.animate.scale(.5),  # Shrink back
            dimers.animate.set_color(WHITE),
            lag_ratio=0.5
        )
        self.play(dimer_mark, run_time=.2)
        dimers.set_color(RED)
        self.wait(1)
        dimers.set_color(WHITE)
        self.wait(1)
        
        # Draw Energy Graph and add laser
        energy_label = Text("Energy Levels", font_size=36).move_to([4.25,1.5,0])
        ground_label = Text("Gnd", font_size=24).move_to([5.3,-1,0])
        pos_label = Text("+1", font_size=24).move_to([5.1,1,0])
        neg_label = Text("-1", font_size=24).move_to([5.1,0,0])
        energy_box = VMobject().set_points_as_corners([
            [2.5, 2, 0],
            [6, 2, 0],
            [6, -2, 0],
            [2.5, -2, 0],
            [2.5, 2, 0],
        ]).set_stroke(color=WHITE, width=2)
            
        state_lines = VGroup(
            Line(
            start=[3, 1, 0],  # Starting point (x, y, z)
            end=[3.8, 1, 0],     # Ending point (x, y, z)
            color=WHITE,        # Line color
            stroke_width=4     # Line thickness
            ),
            Line(
            start=[4, 1, 0],  # Starting point (x, y, z)
            end=[4.8, 1, 0],     # Ending point (x, y, z)
            color=WHITE,        # Line color
            stroke_width=4     # Line thickness
            ),
            Line(
            start=[3, 0, 0],  # Starting point (x, y, z)
            end=[3.8, 0, 0],     # Ending point (x, y, z)
            color=WHITE,        # Line color
            stroke_width=4     # Line thickness
            ),
            Line(
            start=[4, 0, 0],  # Starting point (x, y, z)
            end=[4.8, 0, 0],     # Ending point (x, y, z)
            color=WHITE,        # Line color
            stroke_width=4     # Line thickness
            ),
            Line(
            start=[3, -1, 0],  # Starting point (x, y, z)
            end=[3.8, -1, 0],     # Ending point (x, y, z)
            color=WHITE,        # Line color
            stroke_width=4     # Line thickness
            ),
            Line(
            start=[4, -1, 0],  # Starting point (x, y, z)
            end=[4.8, -1, 0],     # Ending point (x, y, z)
            color=WHITE,        # Line color
            stroke_width=4     # Line thickness
            ),
        )

        dimer_dot = Dot(point=[3.4, -1, 0], color=WHITE, radius=.2)
        normal_dot = Dot(point=[4.4, -1, 0], color=WHITE, radius=.2)
        dimer_label = Text("dimer", font_size=24).move_to([3.4, -1.4, 0])
        normal_label = Text("normal", font_size=24).move_to([4.4, -1.4, 0])
        dimer = VGroup(dimer_dot, dimer_label)
        normal = VGroup(normal_dot, normal_label)
        
        
        energy_table_animations = AnimationGroup(
            [FadeIn(x) for x in [energy_box, energy_label]], 
            Create(state_lines),
            [FadeIn(x, shift=RIGHT) for x in [pos_label, neg_label, ground_label]],
            [FadeIn(x) for x in [dimer, normal]],
            lag_ratio=1.0)
        
        with self.voiceover(text="Since NV centers require higher energy the closer together they are,") as tracker:
            self.play(energy_table_animations, run_time = tracker.duration)
        
        
        # Excite and return arrows:
        dimer_excite_arrow = Vector([0,2], color=BLUE).shift([2.9,-.95,0])
        
        dimer_return_arrow = Vector([0,-2], color=BLUE).shift([2.9,.95,0])
        
        normal_excite_arrow = Vector([0,1], color=GREEN).shift([3.9,-.95,0])
        
        normal_return_arrow = Vector([0,-1], color=GREEN).shift([3.9,-.05,0])
        
        dimer_excite_arrow2 = Vector([0,2], color=BLUE).shift([2.9,-.95,0])
        normal_excite_arrow2 = Vector([0,1], color=GREEN).shift([3.9,-.95,0])
        
        dimer_arrow_label = Text("~1ms", font_size=18, color=BLUE).move_to([3.4,-.5,0])
        normal_arrow_label = Text("~10μs", font_size=18, color=GREEN).move_to([4.4,-.5,0])
        
        laser_gun = VMobject()
        laser_label = Text("Laser", font_size=18).move_to([-5.6,0,0])
        laser_gun.set_points_as_corners([[-6, .2, 0], [-5.2, .2, 0], [-5, 0, 0], [-5.2, -.2, 0], [-6, -.2, 0], [-6, .2, 0], ])
        
        # Set style for the open shape
        laser_gun.set_stroke(color=WHITE, width=4)
        
        # Add the open shape to the scene
        with self.voiceover(text="we can apply a low energy light pulse") as tracker:
            self.play(FadeIn(laser_gun),Write(laser_label), run_time = tracker.duration)

        pulse_green = LaserPulse(
            start = np.array([-5, 0, 0]),  
            end = np.array([-2, 0, 0]),   
            amplitude=.5,
            sigma=.4,
            freq=3.0,
            wave_speed=6.0, 
            color=GREEN,
            stroke_width=4,
        ).set_opacity(0)
        pulse_blue = LaserPulse(
            start = np.array([-5, 0, 0]),  
            end = np.array([-2, 0, 0]),   
            amplitude=0.5,
            sigma=.4,
            freq=3.0,
            wave_speed=6.0, 
            color=BLUE,
            stroke_width=4,
        ).set_opacity(0)
        
        self.add(pulse_green,pulse_blue)

        # Raise normal NV centers to -1, make green
        self.wait(1)
        with self.voiceover(text="to the diamond to only excite defects") as tracker:
            self.play(AnimationGroup(pulse_green.animate_pulse(run_time=1)), run_time=tracker.duration)
        # self.play( run_time=.25)
        # self.play(normal.animate.shift(UP))
        normal_raise = AnimationGroup(normal.animate.shift(UP),normal.animate.set_color(GREEN), normals.animate.set_color(GREEN), run_time=0.5)
        with self.voiceover(text="that are far away") as tracker:
            self.play(normal_raise, run_time = tracker.duration)
        with self.voiceover(text="from other defects,") as tracker:
            self.play(FadeIn(normal_excite_arrow), normal.animate.shift(UP), run_time = tracker.duration)
        self.voiceover(text="and bring them into a medium-energy state.")
        
        
        # Raise dimers to +1, make blue
        self.wait(1)
        self.play(FadeOut(normal_excite_arrow), run_time=.25)
        self.play(pulse_blue.animate_pulse(run_time=1))
        # self.play(dimer.animate.shift(2 * UP))
        # self.play(run_time=.25)
        dimer_raise = AnimationGroup(dimer.animate.set_color(BLUE),dimers.animate.set_color(BLUE), run_time=0.5)
        self.play(dimer_raise)
        self.play(FadeIn(dimer_excite_arrow), dimer.animate.shift(2 * UP))
        # dimer_dot.set_color(BLUE).move_to([3.4,1,0])
        # dimer_label.set_color(BLUE).move_to([3.4,.6,0])
        
        
        # Lower normal NV centers to Ground, make white
        self.wait(1)
        self.play(FadeOut(dimer_excite_arrow), run_time=.25)
        self.play(pulse_green.animate_pulse(run_time=1))
        # self.play( run_time=.25)
        normal_lower = AnimationGroup(normal.animate.set_color(WHITE),normals.animate.set_color(WHITE), run_time=0.5)
        self.play(normal_lower)
        self.play(FadeIn(normal_return_arrow), normal.animate.shift(DOWN))
        # normal_dot.set_color(WHITE).move_to([4.4,-1,0])
        # normal_label.set_color(WHITE).move_to([4.4,-1.4,0])
        
        
        # Make blue dimers transparent, show times
        self.wait(1)
        self.play(dimers.animate.set_opacity(0.5), run_time=1)
        self.add(normal_excite_arrow2, dimer_excite_arrow2, dimer_return_arrow)
        self.play(FadeIn(x) for x in [dimer_arrow_label,normal_arrow_label])
        self.wait(1)