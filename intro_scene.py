from manim import *
import numpy as np

# manim -pqh intro_scene.py Intro_Scene
class Intro_Scene(Scene):
    def construct(self):
        # # Harvard, Yao Group Logo
        # Harvard_logo = ImageMobject("Harvard_University_logo.jpg").move_to([0,2.5,0]).scale(0.4)
        # self.add(Harvard_logo)
        # Yao_group_logo = ImageMobject("Yao_Group_logo.jpg").move_to([0,-1,0])
        
        group_diamond = VMobject()
        group_diamond.set_points_as_corners([[-1,1,0], [1,1,0], [2, 0, 0], [0, -2, 0], [-2, 0, 0], [-1,1,0],]).set_stroke(color=WHITE, width=12)
        group_circle = Circle(radius=.35, color=WHITE, fill_opacity=1).shift([0,-.4,0])
        group_vector = Vector([1.6,0.6],color=WHITE, stroke_width=10).shift([-.8,-.7,0])
        
        yao_group = Text("Yao Group",font_size=144).move_to([1, 0, 0])
        
        group_logo = VGroup(group_diamond, group_vector,group_circle).scale(.5).move_to([-4.5,0,0])
        # group_logo.add(yao_group, )
        
        
        
        self.add(group_diamond, group_circle, group_vector, yao_group)
        
        # Generate spinning hydrogen atom
        
        # Zoom out to a molecule and then a cell
        
        # Zoom out to a hand
        
        # Zoom out to the full body
        
        # Show the FMRI Machine around the body