from manim import *
import numpy as np
import random
import matplotlib as plt
config.media_embed = True

# manim -pqh statistical_distribution.py StatisticalDistribution
class StatisticalDistribution(Scene):
    def construct(self):
        SHIFT_AMOUNT = 3
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

        np.random.seed(5318008) # Seeding random function for consistency

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
            dot.set_fill(WHITE, opacity=0)
            dot.set_stroke(width=0)

            self.add(dot)
            all_dots.append(dot)

            self.play(
                dot.animate.move_to(final_pos).set_opacity(1), # Dropping balls and fading them in as they fall
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
        
        axes = Axes(
            x_range=[-3,3,1],
            y_range=[-3,3,1],
            x_length=6,
            y_length=6,
            tips=False,
            x_axis_config={"include_ticks": False, "include_numbers": False, "stroke_opacity": 0},
            y_axis_config={"include_ticks": False, "include_numbers": False, "stroke_opacity": 0}
        ).move_to([0,-SHIFT_AMOUNT,0])
        self.add(axes)
        xmax = ValueTracker(-2.9999)
        plot = always_redraw(lambda:
            axes.plot(
                normal_pdf,
                x_range=[-3, xmax.get_value()]
            )
        )
        area = always_redraw(lambda:
            axes.get_area(
                axes.plot(normal_pdf),
                x_range=[-3, xmax.get_value()]
            )
        )
        self.add(plot,area)
        self.wait()
        self.play(xmax.animate.set_value(3), run_time=3)
        self.wait()
        
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
        sd = Tex(r"$\sigma$")
        sd2 = Tex(r"$\frac{\sigma}{2}$")
        
        N_samples = Text("N Samples", font_size=36).move_to([0,-SHIFT_AMOUNT - 0.5,0])
        more_samples = Text("4N Samples", font_size=36).move_to(N_samples.get_center())

        propto.next_to(sd_bar, UP, buff=0.2)
        sd.move_to(propto.get_center() + 0.25 * DOWN)
        sd2.move_to(propto.get_center() + 0.25 * DOWN)

        self.play(FadeIn(propto), run_time=1)
        self.wait()
        
        # solid_curve = VGroup(area, curve)
        solid_curve = VGroup(area, plot)
        self.play(Transform(propto, sd), FadeIn(N_samples))
        
        
        [obj.clear_updaters() for obj in solid_curve]
        self.play(solid_curve.animate.scale(.5, about_edge=DOWN),sd_bar.animate.shift(1.1 * DOWN).scale([.5, 1, 1], about_edge=LEFT), propto.animate.shift(1.1 * DOWN + 0.25 * LEFT))
        self.wait(0.5)
        self.play(solid_curve.animate.scale([1, 4, 1], about_edge=DOWN), sd_bar.animate.shift(3.5 * UP), propto.animate.shift(3.5 * UP), Transform(N_samples, more_samples), run_time=1)
        sd2.move_to(propto.get_center() + 0.125 * LEFT + 0.2 * UP)
        self.play(sd_bar.animate.scale([.5, 1, 1], about_edge=LEFT), Transform(propto, sd2))
        
        
