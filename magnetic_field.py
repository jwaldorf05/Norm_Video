from manim import *
import numpy as np

class MyCurves(VGroup):
    def __init__(
        self,
        t_min=0,
        t_max=PI,
        x1_values=None,
        base_color=BLUE,
        family_color=RED,
        base_n_samples=100,
        family_n_samples=100,
        show_arrows=True,        
        arrow_count_base=5,       
        arrow_count_family=5,      
        arrow_scale=0.1,           
        arrow_color=WHITE,
        flow_forward=True,         
        **kwargs
    ):
        super().__init__(**kwargs)

        if x1_values is None:
            x1_values = [(k * np.pi/4) for k in range(8)]

        self.t_min = t_min
        self.t_max = t_max
        self.x1_values = x1_values
        self.base_color = base_color
        self.family_color = family_color
        self.show_arrows = show_arrows
        self.arrow_count_base = arrow_count_base
        self.arrow_count_family = arrow_count_family
        self.arrow_scale = arrow_scale
        self.arrow_color = arrow_color
        self.flow_forward = flow_forward
        base_step = (t_max - t_min) / base_n_samples
        family_step = (t_max - t_min) / family_n_samples

        def base_func(t):
            return np.array([
                (2 / np.sqrt(3)) * np.cos((4/3)*t - np.pi/6),
                0,
                np.sin(t),
            ])

        base_curve = ParametricFunction(
            base_func,
            t_range=(t_min, t_max, base_step),
            color=self.base_color,
        )
        self.add(base_curve)

        if self.show_arrows and self.arrow_count_base > 0:
            arrows_for_base = self._make_arrows_along_curve(
                base_curve, base_func, self.arrow_count_base
            )
            self.add(*arrows_for_base)

        def family_func_factory(x1):
            
            def f(t):
                return np.array([
                    (2 / np.sqrt(3)) * np.cos((4/3)*t - np.pi/6),
                    np.sin(x1) * np.sin(t),
                    np.cos(x1) * np.sin(t),
                ])
            return f

        for x1 in self.x1_values:
            ffunc = family_func_factory(x1)
            family_curve = ParametricFunction(
                ffunc,
                t_range=(t_min, t_max, family_step),
                color=self.family_color,
            )
            self.add(family_curve)

            if self.show_arrows and self.arrow_count_family > 0:
                arrows_for_this = self._make_arrows_along_curve(
                    family_curve, ffunc, self.arrow_count_family
                )
                self.add(*arrows_for_this)

    def _make_arrows_along_curve(self, curve_mobj, func, n_arrows):
        arrows = []
        t_vals = np.linspace(self.t_min, self.t_max, n_arrows)

        for t in t_vals:
            point = func(t)
            tangent = self._approx_tangent(func, t)

            if not self.flow_forward:
                tangent = -tangent

            arrow = Cone(
                base_radius=self.arrow_scale * 0.5, 
                height=self.arrow_scale,
                direction=OUT,  
                show_base=False,
                fill_opacity=1.0,
                color=self.arrow_color
            ).set_fill(color = self.arrow_color, opacity = .75)
           
            arrow.set_direction(tangent)

            arrow.shift(point)

            arrows.append(arrow)
        return arrows

    def _approx_tangent(self, func, t, eps=1e-5):
        p1 = func(t + eps)
        p2 = func(t - eps)
        tangent = p1 - p2
        norm = np.linalg.norm(tangent)
        if norm < 1e-12:

            return OUT
        return tangent / norm
    
    
#example implemetnation
class ShowCurves(ThreeDScene):
    def construct(self):
        curve_group = MyCurves(
            t_min=0,
            t_max=PI,
            x1_values=[k*np.pi/4 for k in range(8)],
            base_color=BLUE,
            family_color=RED,
            base_n_samples=150,
            family_n_samples=150,
            show_arrows=True,
            arrow_count_base=5,
            arrow_count_family=5,
            arrow_scale=0.1,
            arrow_color=RED,
            flow_forward=True,  
        )
        self.set_camera_orientation(phi=70*DEGREES, theta=30*DEGREES, distance=6)
        self.add(curve_group)
        self.wait(3)