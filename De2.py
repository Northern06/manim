from manimlib.once_useful_constructs.graph_scene import GraphScene

from manimlib import *

class myGraph(GraphScene):

    CONFIG = {
        "y_max": 4,
        "y_min": -4,
        "x_max": 5,
        "x_min": -5,
        #"y_tick_frequency": 1,
        #"x_tick_frequency": 1,
        "axes_color": WHITE,
        "graph_origin": ORIGIN,
        "x_label_direction": DOWN,
        "y_label_direction": LEFT
    }

    def construct(self):
        self.setup_axes(animate=True)

        graph = self.get_graph(lambda x: x**2, color=YELLOW)

        self.play(ShowCreation(graph), run_time=2)


class chapter_01(Scene):
    def construct(self):
        t1 = ValueTracker(0.001)
        t2 = ValueTracker(1)
        t3 = ValueTracker(0.001)
        tex_color = {"{k}": RED_A, "{f(x)}": YELLOW}
        position = [UP, DOWN, LEFT, RIGHT, UR, UL, DR, DL]

        axes = Axes(x_range=(0, 5), y_range=(0, 5), height=5, width=5).shift(np.array([-3, 0, 0]))
        x_y = axes.get_axis_labels()


        def get_tangent(a, b, step):
            curve_group = VGroup()
            for n in np.arange(0, 4, step):
                k = 2 * a * n + b
                y1 = a * (n ** 2)
                curve = axes.get_graph(lambda x: k * x - k * (n) + y1, color=BLUE_B)
                curve_group.add(curve)
            return curve_group

        def get_point_of_tangency(a, b, step):
            dot_group = VGroup()
            for n in np.arange(0, 4, step):
                dot = SmallDot(axes.coords_to_point(n, a * (n ** 2) + b * n), color=BLUE_B)
                dot_group.add(dot)
            return dot_group

        def get_x_dots(step):
            dot_group = VGroup()
            for n in np.arange(0, 4, step):
                dot = SmallDot(axes.coords_to_point(n, 0), color=TEAL)
                dot_group.add(dot)
            return dot_group

        curve3 = axes.get_graph(lambda x: 0.3 * (x ** 2), x_range=[0, 4], color=YELLOW).add_updater(
            lambda obj: obj.become(axes.get_graph(lambda x: 0.3 * (x ** 2), x_range=[0, t3.get_value()], color=YELLOW)))
        l2_h = axes.get_h_line_to_graph(0.001, curve3).add_updater(
            lambda obj: obj.become(axes.get_h_line_to_graph(t3.get_value(), curve3)))
        l2_v = axes.get_v_line_to_graph(0.001, curve3).add_updater(
            lambda obj: obj.become(axes.get_v_line_to_graph(t3.get_value(), curve3)))
        self.play(FadeIn(axes, shift=UP))
        self.add(curve3, l2_h, l2_v)
        self.play(t3.set_value, 4, run_time=2, rate_func=linear)
        self.play(Uncreate(l2_h), Uncreate(l2_v))
        self.wait(2)
        curve3.clear_updaters()

        dot_g1 = get_x_dots(0.5)
        dot_g2 = get_point_of_tangency(0.3, 0, 0.5)
        tangent_g1 = get_tangent(0.3, 0, 0.5)
        tangent_g2 = get_tangent(0.3, 0, 0.2)
        tangent_g3 = get_tangent(0.3, 0, 0.1)
        tangent_g4 = get_tangent(0.3, 0, 0.08)
        self.play(LaggedStart(*[FadeIn(i, shift=DOWN * n) for i, n in zip(dot_g1, np.arange(0, 4, 0.5))]))
        self.play(LaggedStart(*[ReplacementTransform(a, b) for a, b in zip(dot_g1, dot_g2)]))
        self.play(LaggedStart(*[ReplacementTransform(c, d) for c, d in zip(dot_g2, tangent_g1)]))
        self.wait(4.5)
        self.play(ReplacementTransform(tangent_g1, tangent_g2))
        self.play(ReplacementTransform(tangent_g2, tangent_g3))
        self.play(ReplacementTransform(tangent_g3, tangent_g4))
        self.wait(0.5)
        self.play(LaggedStart(*[FadeOut(i, shift=random.choice(position) * 3) for i in tangent_g4]))
        self.play(FadeOut(curve3), FadeOut(axes), FadeOut(x_y))




