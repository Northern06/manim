from manim import *

# HELPERS FOR COMPLEX SCENES, you can always create your own :)
def get_horizontal_line_to_graph(axes, function, x, width, color):
    result = VGroup()
    line = DashedLine(
        start=axes.c2p(0, function.underlying_function(x)),
        end=axes.c2p(x, function.underlying_function(x)),
        stroke_width=width,
        stroke_color=color,
    )
    dot = Dot().set_color(color).move_to(axes.c2p(x, function.underlying_function(x)))
    result.add(line, dot)
    return result


def get_arc_lines_on_function(
    graph, plane, dx=1, line_color=WHITE, line_width=1, x_min=None, x_max=None
):

    dots = VGroup()
    lines = VGroup()
    result = VGroup(dots, lines)

    x_range = np.arange(x_min, x_max, dx)
    colors = color_gradient([BLUE_B, GREEN_B], len(x_range))

    for x, color in zip(x_range, colors):
        p1 = Dot().scale(0.7).move_to(plane.input_to_graph_point(x, graph))
        p2 = Dot().scale(0.7).move_to(plane.input_to_graph_point(x + dx, graph))
        dots.add(p1, p2)
        dots.set_fill(colors, opacity=0.8)

        line = Line(
            p1.get_center(),
            p2.get_center(),
            stroke_color=line_color,
            stroke_width=line_width,
        )
        lines.add(line)

    return result


class Derivatives(Scene):
    def construct(self):

        k = ValueTracker(0)  # Tracking the end values of stuff to show

        # Adding Mobjects for the first plane
        plane1 = (
            NumberPlane(x_range=[0, 12, 1], x_length=13, y_range=[-1.9, 1.9, 1], y_length=7)
            .add_coordinates()
            .shift(UP * 1.63)
        )

        func1 = plane1.plot(
            lambda x: np.sin(x), x_range=[0, 12], color=RED_C
        )

        plane2 = (
            NumberPlane(x_range=[0, 12, 1], x_length=13, y_range=[-1.9, 1.9, 1], y_length=7)
            .add_coordinates()
            .shift(DOWN * 1.65)
        )
        func1_lab = (
            MathTex("f(x)=sin(x)")
            .set(width=2.5)
            .next_to(plane2, UP, buff=0.2)
            .set_color(RED_C)
        )

        moving_slope = always_redraw(
            lambda: plane1.get_secant_slope_group(
                x=k.get_value(),
                graph=func1,
                dx=0.05,
                secant_line_length=4,
                secant_line_color=YELLOW,
            )
        )

        dot = always_redraw(
            lambda: Dot().move_to(
                plane1.c2p(k.get_value(), func1.underlying_function(k.get_value()))
            )
        )

        # Adding Mobjects for the second plane


        func2 = always_redraw(
            lambda: plane2.plot(
                lambda x: np.cos(x), x_range=[0, k.get_value()], color=GREEN
            )
        )
        func2_lab = (
            MathTex("f'(x)=cos(x)?")
            .set(width=2.5)
            .next_to(plane1, DOWN, buff=0.2)
            .set_color(GREEN)
        )

        moving_h_line = always_redraw(
            lambda: get_horizontal_line_to_graph(
                axes=plane2, function=func2, x=k.get_value(), width=4, color=YELLOW
            )
        )
        group2 = VGroup(plane2, moving_h_line)
        def shift3(p):
            p=p+(UP * 3.3)
            return p
        # Adding the slope value stuff
        slope_value_text = (
            Tex("Slope value: ")
            .next_to(func2_lab, RIGHT*1.2, buff=0.1)
            .set_color(YELLOW)
            .add_background_rectangle()
        )

        slope_value = always_redraw(
            lambda: DecimalNumber(num_decimal_places=1)
            .set_value(func2.underlying_function(k.get_value()))
            .next_to(slope_value_text, RIGHT, buff=0.1)
            .set_color(YELLOW)
        ).add_background_rectangle()
        group1 = VGroup(slope_value_text, slope_value)
        # Playing the animation
        self.play(
            LaggedStart(
                DrawBorderThenFill(plane1),
                DrawBorderThenFill(plane2),
                Create(func1),
                Write(func1_lab),
                run_time=5,
                lag_ratio=0.5,
            )
        )
        self.add(moving_slope, moving_h_line, func2, slope_value, slope_value_text, dot)
        self.play(k.animate.set_value(11), run_time=15, rate_func=linear)
        self.wait()
        self.play(ApplyPointwiseFunction(shift3, group2), run_time=1)
        self.wait(0.5)
        self.play(FadeOut(group1))
        self.wait(0.5)
        self.play(Write(func2_lab))
        self.wait()
        self.wait()



