from manim import *
import numpy as np
def dipole_field(
    point,
    moment=np.array([0, 0, 1], dtype=float),
    center=np.array([0, 0, 0], dtype=float),
    scale=0.05
):
    r = point - center
    r_norm = np.linalg.norm(r)
    if r_norm < 1e-7:
        return np.zeros(3, dtype=float)
    r_hat = r / r_norm
    return scale * ((3 * np.dot(moment, r_hat) * r_hat) - moment) / (r_norm**3)

def trace_field_line(
    start_point,
    field_func,
    step_size=0.03,
    n_steps=8000,
    direction=+1.0
):
    points = [np.array(start_point, dtype=float)]
    current = np.array(start_point, dtype=float)

    for _ in range(n_steps):
        B = field_func(current)
        norm_B = np.linalg.norm(B)
        if norm_B < 1e-9:
            break
        current += direction * step_size * (B / norm_B)
        points.append(np.array(current))

    return points
def create_field_line_from_points(points, color=YELLOW, width=2):
    line = VMobject()
    line.set_points_as_corners(points)
    line.set_stroke(color=color, width=width)
    return line

class MagneticFieldScene(ThreeDScene):
    def construct(self):
        axes = ThreeDAxes(
            x_range=[-2, 2, 1],
            y_range=[-2, 2, 1],
            z_range=[-2, 2, 1],
            axis_config={"stroke_width": 2}
        )
        self.add(axes)

        self.set_camera_orientation(phi=65 * DEGREES, theta=-45 * DEGREES, distance=7)

        dipole_moment = np.array([0, 0, 1], dtype=float)
        dipole_center = np.array([0, 0, 0], dtype=float)
        scale_factor  = 0.05  
        magnet = Cylinder(
            radius=0.2,
            height=2,
            direction=UP,
            v_range=[-1, 1],
            fill_opacity=0.6,
            fill_color=BLUE,
        )
        self.add(magnet)

        seed_points = []
        z_top = 1.1
        for radius in np.arange(0.1, 0.2, 0.1):  
            for angle_deg in [0, 90, 180, 270]:
                angle = angle_deg * DEGREES
                x = radius * np.cos(angle)
                y = radius * np.sin(angle)
                seed_points.append(np.array([x, y, z_top]))

        field_lines = []
        for seed in seed_points:
      
            plus_trace = trace_field_line(
                start_point=seed,
                field_func=lambda p: dipole_field(
                    p, dipole_moment, dipole_center, scale_factor
                ),
                step_size=0.03,
                n_steps=8000,
                direction=+1
            )
            minus_trace = trace_field_line(
                start_point=seed,
                field_func=lambda p: dipole_field(
                    p, dipole_moment, dipole_center, scale_factor
                ),
                step_size=0.03,
                n_steps=8000,
                direction=-1
            )

            plus_line  = create_field_line_from_points(plus_trace,  color=YELLOW, width=2)
            minus_line = create_field_line_from_points(minus_trace, color=YELLOW, width=2)
            field_lines.extend([plus_line, minus_line])
        self.add(*field_lines)
        self.wait(4)