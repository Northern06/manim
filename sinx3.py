from manim import *

def get_vertical_line_to_graph(axes, function, x, width, color):  #creates line from axis to graph
    result = VGroup() #returns a group
    line = DashedLine( #creates a dashed line from
        start = axes.c2p(x, 0), #the axis (x,0)
        end = axes.c2p(x, function.underlying_function(x)), # to a point on the graph (x,f(x))
        stroke_width = width,
        stroke_color = color,
    )
    result.add(line)#adds line to group
    return result# returns group

class vt(Scene):
    def construct(self):
        e = ValueTracker(0.01) #valuetracker
        plane0 = NumberPlane(x_range=[-3, 3], x_length=15, y_range=[-1.9, 1.9],
                               y_length=10, background_line_style={"stroke_opacity": 0})
        plane0.add_coordinates()
        plane = PolarPlane(radius_max=4, size=8, background_line_style={"stroke_opacity": 0}).scale(1.3)
            #.shift(LEFT*3) #polarplane with radius=2


        circle = ParametricFunction(lambda t : plane.polar_to_point(2, t), t_range=[0, 2*PI], color=GREEN, stroke_width=3) #draws unit circle
        plane0_circle = VGroup(plane0, circle)#组合坐标与单位圆
        #第一幕：sinx在单位圆中的意义
        rotation_center = plane0.c2p(0, 0)

        theta_tracker = ValueTracker(110)
        line1 = Line(plane0.c2p(0, 0), plane0.c2p(1, 0))
        line_moving = Line(plane0.c2p(0, 0), plane0.c2p(1, 0))
        line_ref = line_moving.copy()
        line_moving.rotate(
            theta_tracker.get_value() * DEGREES, about_point=rotation_center
        )
        a = Angle(line1, line_moving, radius=0.3, other_angle=False)
        tex = MathTex(r"\theta").move_to(
            Angle(
                line1, line_moving, radius=0.3 + 3 * SMALL_BUFF, other_angle=False
            ).point_from_proportion(0.5)
        )
        a.add_updater(
            lambda x: x.become(Angle(line1, line_moving, radius=0.3, other_angle=False))
        )
        tex.add_updater(
            lambda x: x.move_to(
                Angle(
                    line1, line_moving, radius=0.3 + 3 * SMALL_BUFF, other_angle=False
                ).point_from_proportion(0.5)
            )
        )

        #############################################################################

        line_moving.add_updater(
            lambda x: x.become(line_ref.copy()).rotate(
                theta_tracker.get_value() * DEGREES, about_point=rotation_center
            )
        )


        polarGraph=always_redraw(lambda: #Not rendered, exists to move dot along x-axis of unit circle from 1 to -1 to 1 again
            ParametricFunction(lambda t: plane.polar_to_point(2*np.cos(t), 0),
            t_range=[0, e.get_value()], color=GREEN, stroke_width=0)
        )
        dot2 = always_redraw(lambda : #Dot at end of polarGraoh
            Dot().move_to(polarGraph.get_end()).set_color(YELLOW).scale(0)
        )

        hypCircle = always_redraw(lambda: #Not rendered, exists to move dot along unit circle
            ParametricFunction(lambda t : plane.polar_to_point(2, t),
            t_range=[0, e.get_value()], color=GREEN, stroke_width=0)
        )
        dot3 = always_redraw(lambda : #Dot at end of hypCircle
            Dot().move_to(hypCircle.get_end()).set_color(RED)
        )

        circle = always_redraw(lambda: #circle representing value of theta
            ParametricFunction(lambda t: plane.polar_to_point(0.2, t),
            t_range=[0, e.get_value()], color=PURPLE, stroke_width=3)
        )



        dashed_line = always_redraw(lambda : #dot representing sin on unit ricrcle
            DashedLine(dot2, dot3).set_color(YELLOW)
        )
        #b1 = Brace(dashed_line)
        #b1text = b1.get_tex("$sin\\theta$")

        line = always_redraw(lambda: #dot representing hypotenuse of unit circle triangle
            Line(plane.get_center(), dot3)
        )

        axes = Axes(x_range=[-1, 8, 1.57], y_range=[-2, 2, 1], x_length=6, y_length=4, tips=False).to_edge(RIGHT).add_coordinates()
        axes_labels = axes.get_axis_labels()
        graph1 = always_redraw(lambda :#plotting sin from 0 to pi
            axes.plot(lambda x: np.sin(x), x_range = [0,e.get_value()], color=RED)
        )
        dot1 = always_redraw(lambda :#dot on end of graph1
            Dot(fill_color=RED).move_to(graph1.get_end()).scale(1.2)
        )

        dot4 = always_redraw(lambda: #dot on x-axis with x-value of graph1
            Dot(fill_color=PURPLE).move_to(axes.c2p(e.get_value(), 0))
        )

        moving_v_line = always_redraw(lambda: #line between x-axis and sin graph
            get_vertical_line_to_graph( #previosuly defined function, returns dashed line
                axes = axes, function = graph1, x = e.get_value(), width=4, color=YELLOW
            )
        )

        label = MathTex("f(\\theta) = sin(\\theta)", color=RED).next_to(axes, UP, buff=0.2) #graph label

        value_label = MathTex("\\theta =").next_to(axes, DOWN).shift(LEFT).set_color(PURPLE)
        value = always_redraw(lambda:
            DecimalNumber(num_decimal_places=1)
            .set_value(e.get_value())
            .next_to(value_label, RIGHT)
            .set_color(PURPLE)
        )

        def shift3(p):
            p=p+(LEFT * 3)
            return p

        self.play(Write(plane0_circle))
        self.play(DrawBorderThenFill(plane))
        self.wait(0.5)
        self.play(Write(line1), Write(line_moving))
        self.add(a, tex)
        self.wait()
        self.play(theta_tracker.animate.set_value(40))
        self.play(theta_tracker.animate.increment_value(140))
        self.play(tex.animate.set_color(RED), run_time=0.5)
        self.play(theta_tracker.animate.set_value(359))
        self.play(FadeOut(line1, line_moving, a, tex))

        self.play(FadeOut(line1))
                  #, FadeOut(line3), FadeOut(b1), FadeOut(b1text))
        self.wait()
        self.play(ApplyPointwiseFunction(shift3, plane0_circle), ApplyPointwiseFunction(shift3, plane), run_time=1)
        #self.play(Transform(plane0_circle, plane01), Transform(plane, plane02))
        self.wait()
        self.play(DrawBorderThenFill(axes))
        self.add(axes_labels)
        self.wait(0.5)
        self.play(Write(circle), Write(dot1), Write(label), Write(dot2), Write(dot3), Write(dashed_line), Write(line), Write(moving_v_line), Write(value_label), Write(value))
        self.add(graph1, polarGraph, hypCircle, circle, dot4)
        self.play(e.animate.set_value(6.3), run_time=10, rate_func=linear)
        self.wait(2)

        group = VGroup(polarGraph, axes)
        plane = NumberPlane(x_range=[-4, 4, 1], y_range=[-4, 4, 1], x_length=8, y_length=8)
        self.play(
            FadeOut(circle),
             FadeOut(dot1),
             FadeOut(label),
             FadeOut(dot2),
             FadeOut(dot3),
             FadeOut(dashed_line),
             FadeOut(line),
             FadeOut(moving_v_line),
             FadeOut(value_label),
             FadeOut(value)
         )
        self.play(FadeOut(group))