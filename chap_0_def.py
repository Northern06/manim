from manim import *
#chap0 导数的定义
#lim (x+delta)/delta delta->0
class Paradox(Scene):
    def construct(self):

        axes = (
            Axes(
                x_range=[0, 10, 1],
                x_length=9,
                y_range=[0, 20, 5],
                y_length=6,
                axis_config={"include_numbers": True, "include_tip": False},
            )
            .to_edge(DL)
            .set_color(GREY)
        )
        axes_labels = axes.get_axis_labels()

        func = axes.plot(
            lambda x: 0.1 * (x - 2) * (x - 5) * (x - 7)+7, x_range=[0, 10], color=BLUE
        )

        x = ValueTracker(7)
        dx = ValueTracker(2)

        secant = always_redraw(
            lambda: axes.get_secant_slope_group(
                x=x.get_value(),
                graph=func,
                dx=dx.get_value(),
                dx_line_color=YELLOW,
                dy_line_color=ORANGE,
                dx_label="\\Delta x",
                dy_label="\\Delta y",
                secant_line_color=GREEN,
                secant_line_length=8,
            )
        )
        dot1 = always_redraw(
            lambda: Dot()
            .scale(0.7)
            .move_to(axes.c2p(x.get_value(), func.underlying_function(x.get_value())))
        )
        dot2 = always_redraw(
            lambda: Dot()
            .scale(0.7)
            .move_to(
                axes.c2p(
                    (x).get_value() + dx.get_value(),
                    func.underlying_function(x.get_value() + dx.get_value()),
                )
            )
        )
        #文本
        #tex1 = MTex("({x_{1}}, {y_{1}})", tex_to_color_map=tex_color).next_to(d1, RIGHT * 0.5)
        #tex2 = MTex("({x_{2}}, {y_{2}})", tex_to_color_map=tex_color).next_to(d2, RIGHT * 0.5)
        #tex3 = MTex("{y_{1}} = {k} {x_{1}} + b ", tex_to_color_map=tex_color).shift(RIGHT * 3.5 + UP * 2)
       # tex4 = MTex("{y_{2}} = {k} {x_{2}} + b ", tex_to_color_map=tex_color).next_to(tex3, DOWN * 0.8, aligned_edge=LEFT)aligned_edge=LEFT)
        #tex5 = MTex("{y_{1}} - {y_{2}} = {k} {x_{1}} - {k} {x_{2}} + b - b", tex_to_color_map=tex_color).next_to(tex4,DOWN * 0.8)

        tex1 = Tex("Derivative")
        tex1.to_edge(UP*1.6+LEFT*5.2)
        equal = MathTex("=")
        tex2_l = MathTex("k", color=GREEN)
        tex2_r = MathTex("\\frac{\\Delta y}{\\Delta x}")
        tex3_r = MathTex("\\frac{f(a+\\Delta x) -f(a)}{\\Delta x}}")

        tex2 = VGroup(equal, tex2_l, tex2_r)
        equal.next_to(tex1, DOWN, buff=0.9)
        tex2_l.next_to(equal, LEFT)
        tex2_r.next_to(equal, RIGHT)
        tex3_r.next_to(equal, RIGHT)
        tex3 = VGroup(equal, tex2_l, tex3_r)

        num1 = MathTex("\\frac{f(a+1) -f(a)}{1}}")
        num1.next_to(equal, RIGHT)
        num2 = MathTex("\\frac{f(a+0.1) -f(a)}{0.1}}")
        num2.next_to(equal, RIGHT)
        num3 = MathTex("\\frac{f(a+0.01) -f(a)}{0.01}}")
        num3.next_to(equal, RIGHT)
        num4 = MathTex("\\frac{f(a+0.001) -f(a)}{0.001}}")
        num4.next_to(equal, RIGHT)
        num5 = MathTex("\\frac{f(a+0.0001) -f(a)}{0.0001}}")
        num5.next_to(equal, RIGHT)

        rectangle = Rectangle(height=3.3, width=6)
        rectangle.to_edge(UP*1.2+LEFT*4.2)
        rectangle2 = Rectangle(height=0.9, width=6)
        rectangle2.to_edge(UP * 1.2 + LEFT * 4.2)

        brace = Brace(tex3_r, DOWN, buff=SMALL_BUFF)
        t1 = brace.get_text("$\\Delta x \\rightarrow 0$")
        self.add(axes, axes_labels, func)
        self.play(Create(VGroup(dot1, dot2, secant)))
        self.play(dx.animate.set_value(0.001), run_time=8)
        self.wait(2)
        self.play(Write(tex1))
        self.play(Write(tex2))
        self.play(Write(rectangle))
        self.wait(0.5)
        self.play(TransformMatchingTex(tex2_r, tex3_r))
        self.wait(0.5)
        self.play(TransformMatchingTex(tex3_r, num1))
        self.wait(0.5)
        self.play(TransformMatchingTex(num1, num2))
        self.wait(0.5)
        self.play(TransformMatchingTex(num2, num3))
        self.play(TransformMatchingTex(num3, num4))
        self.play(TransformMatchingTex(num4, num5))
        self.wait(0.5)
        self.play(TransformMatchingTex(num5, tex3_r))
        self.wait(0.5)
        self.play(GrowFromCenter(brace),
                  FadeIn(t1))
        self.wait(0.5)
        self.play(FadeOut(brace),
                  FadeOut(t1))
        self.play(FadeOut(tex3))
        self.play(Transform(rectangle,rectangle2), run_time=1)
        self.wait(0.5)
        self.play(x.animate.set_value(1), run_time=5)
        self.wait()
        self.play(x.animate.set_value(7), run_time=5)
        self.wait()
        self.play(dx.animate.set_value(2), run_time=6)
        self.wait()




