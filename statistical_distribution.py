from manim import *
import numpy as np
import random

# manim -pqh statistical_distribution.py StatisticalDistribution
class StatisticalDistribution(Scene):
    def construct(self):
        SHIFT_AMOUNT = 2
        SHIFT_VECTOR = np.array([0, -SHIFT_AMOUNT, 0])

        n_particles = 300
        bin_width = 0.2
        x_min, x_max = -3.0, 3.0
        drop_height = 3.5
        particle_spacing = 0.08
        mu, sigma = 0, 1
        particle_radius = 0.04
        run_time_per_drop = 0.02

        
        n_bins = int((x_max - x_min) / bin_width)
        bin_counts = [0] * n_bins

        
        all_dots = []

        
        x_axis_line = Line(
            start=[x_min - 0.5, 0, 0],
            end=[x_max + 0.5, 0, 0]
        ).set_stroke(width=2)
        
        x_axis_line.shift(SHIFT_VECTOR)

        x_axis_label = Text("measurement").scale(0.4)
        x_axis_label.next_to(x_axis_line, DOWN)
        x_axis_label.shift(SHIFT_VECTOR)

        self.add(x_axis_line, x_axis_label)

       
        for i in range(n_particles):
           
            x_rand = random.gauss(mu, sigma)
            x_rand = max(x_min, min(x_max, x_rand))

            bin_index = int((x_rand - x_min) // bin_width)
            bin_index = max(0, min(n_bins - 1, bin_index))

            x_final = x_min + (bin_index + 0.5) * bin_width
            y_final = bin_counts[bin_index] * particle_spacing

          
            initial_pos = np.array([x_rand, drop_height, 0]) + SHIFT_VECTOR
            final_pos   = np.array([x_final, y_final, 0]) + SHIFT_VECTOR

            dot = Dot(point=initial_pos, radius=particle_radius)
            dot.set_fill(WHITE, opacity=1)
            dot.set_stroke(width=0)

            self.add(dot)
            all_dots.append(dot)

           
            self.play(
                dot.animate.move_to(final_pos),
                run_time=run_time_per_drop
            )

            bin_counts[bin_index] += 1

       
        max_count = max(bin_counts)
        peak_height = max_count * particle_spacing
       
        normal_peak = 1.0 / (sigma * np.sqrt(TAU))
        scale_factor = peak_height / normal_peak

        def normal_pdf(x):
            return (scale_factor
                    * np.exp(-((x - mu) ** 2) / (2 * sigma * sigma))
                    / (sigma * np.sqrt(TAU)))

        
        x_values = np.arange(x_min, x_max, 0.01)
        curve_points = [
            np.array([x, normal_pdf(x), 0]) + SHIFT_VECTOR
            for x in x_values
        ]

        
        curve = VMobject(color=BLUE, stroke_width=3)
        curve.set_points_smoothly(curve_points)

        fill_points = curve_points + [
            np.array([x_max, 0, 0]) + SHIFT_VECTOR,
            np.array([x_min, 0, 0]) + SHIFT_VECTOR
        ]
        fill_region = Polygon(*fill_points)
        fill_region.set_fill(BLUE, opacity=0.2)
        fill_region.set_stroke(width=0)

    
        self.play(Create(fill_region), Create(curve), run_time=2)
        self.wait(1)

        self.play(FadeOut(VGroup(*all_dots)), run_time=2)
        
        sd_line = Line(
            start=[0, 0, 0],
            end=[1, 0, 0],
            color=RED,
            stroke_width=3
        )
        left_tick = Line(
            start=[0, -0.1, 0],
            end=[0, 0.1, 0],
            color=RED,
            stroke_width=3
        )
        right_tick = Line(
            start=[1, -0.1, 0],
            end=[1, 0.1, 0],
            color=RED,
            stroke_width=3
        )
        sd_bar = VGroup(sd_line, left_tick, right_tick)

        above_y = peak_height + 0.3
        sd_bar.shift(SHIFT_VECTOR)        
        sd_bar.shift(UP * above_y)             

        self.play(Create(sd_bar))
        self.wait(0.5)


        propto = Tex(r"$\propto \frac{1}{\sqrt{N}}$")

        propto.next_to(sd_bar, UP, buff=0.2)

        self.play(FadeIn(propto), run_time=1)
        self.wait()
        
        solid_curve = VGroup(fill_region, curve)
        
        self.play(solid_curve.animate.scale(.5, about_edge=DOWN))
        self.wait(0.5)
        self.play(solid_curve.animate.scale([1, 4, 1], about_edge=DOWN), sd_bar.animate.shift(2 * UP), propto.animate.shift(2 * UP), run_time=1)
        
        
