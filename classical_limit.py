from manim import *
import numpy as np

# manim -pqk classical_limit.py Classical_Limit_Animation

class Classical_Limit_Animation(ThreeDScene):
    def construct(self):
        
        # Generate Particle with spin
        
        circle = Circle()  # create a circle
        circle.set_fill(BLUE, opacity=0.5)  # set the color and transparency
        self.play(Create(circle))  # show the circle on screen
        
        # Shake and blur particle
        
        # Particle turns into wave equation, rotating by e^i t theta
        
        # Break up into position and Momentum Waveforms
        position_text = Text("Position", font_size=144)
        momentum_text = Text("Momentum", font_size=144)
        
        # Draw ruler under positon waveform
        
        # Position ruler measures, position squishes, momentum snaps
        
        # Bakck to position and momentum waveforms 
        
        # Draw ruler under momentum waveform
        
        # Position ruler measures, momentum squishes, position snaps
        
        momentum_text = Text("Heisenberg's Uncertainty Principle", font_size=144)
        

        # Draw four waveform objects spinning in random directions with arrows
        
        # Have all the particles entangle together and have their spins align
        
        # One of the spins deviates, and the other spinds move to correct it
        
        # Each of the spins gets shortened and fattened, arrows move much slower
        
        # Four waveforms transform into one larger waveform in the center of the scree 
        jhat = Tex('\\hat{J} total system', tex_template=TexTemplateLibrary.ctex, font_size=144)
        self.add(jhat)
        
        # Show the 1/N distribution
        