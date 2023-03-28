from manim import *
import numpy as np

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
class circle1(ZoomedScene):
    def __init__(self, **kwargs):
        ZoomedScene.__init__(
            self,
            zoom_factor=0.35,
            zoomed_display_height=3,
            zoomed_display_width=4,
            image_frame_stroke_width=20,
            zoomed_camera_config={
                "default_frame_stroke_width": 3,
            },
            **kwargs
        )

    def construct(self):
        e = ValueTracker(0.01) #valuetracker
        plane0 = NumberPlane(x_range=[-3, 3], x_length=15, y_range=[-1.9, 1.9],
                               y_length=10, background_line_style={"stroke_opacity": 0})
        plane0.add_coordinates()
        plane = PolarPlane(radius_max=4, size=8, background_line_style={"stroke_opacity": 0}).scale(1.3)
            #.shift(LEFT*3) #polarplane with radius=2


        circle = ParametricFunction(lambda t : plane.polar_to_point(2, t), t_range=[0, 2*PI], color=GREEN, stroke_width=3) #draws unit circle
        plane0_circle = VGroup(plane0, circle)#组合坐标与单位圆

    ############################################
        rotation_center = plane0.c2p(0, 0)

        theta_tracker = ValueTracker(110)
        line1 = Line(plane0.c2p(0, 0), plane0.c2p(1.03, 0))
        line_moving = Line(plane0.c2p(0, 0), plane0.c2p(1.03, 0))
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
        line_moving.add_updater(
            lambda x: x.become(line_ref.copy()).rotate(
                theta_tracker.get_value() * DEGREES, about_point=rotation_center
            )
        )
    ######################################
        #arc1 = ArcBetweenPoints(plane0.c2p(1.03, 0), plane0.c2p(0.83, 0.63))

        def ruler(sc: Scene, p1, p2, angle=PI, axis=OUT):
            d1 = Dot(point=p1, color=WHITE)
            d2 = Dot(point=p2, color=YELLOW)
            dl = DashedLine(d1.get_center(), d2.get_center())

            r = np.linalg.norm(p2 - p1)
            arc = ArcBetweenPoints(p2, p2)

            dl.add_updater(lambda z: z.become(DashedLine(d1.get_center(), d2.get_center())))
            if np.array_equal(axis, OUT):
                arc.add_updater(
                    lambda z: z.become(
                        ArcBetweenPoints(p2, d2.get_center(), radius=r, stroke_color=YELLOW)
                    )
                )
            if np.array_equal(axis, IN):
                arc.add_updater(
                    lambda z: z.become(
                        ArcBetweenPoints(d2.get_center(), p2, radius=r, stroke_color=YELLOW)
                    )
                )

            sc.add(d1, d2, dl, arc)
            sc.play(
                Rotate(
                    d2,
                    about_point=d1.get_center(),
                    axis=axis,
                    angle=angle,
                    rate_func=linear,
                )
            )

            arc.clear_updaters()
            dl.clear_updaters()
            sc.remove(d1, d2, dl)
            return arc
        ##################################################
        #移动视角
        dot = Dot([1.68, 1.8, 0])
        zoomed_camera = self.zoomed_camera
        zoomed_display = self.zoomed_display
        frame = zoomed_camera.frame
        zoomed_display_frame = zoomed_display.display_frame

        frame.move_to(dot)
        frame.set_color(WHITE)
        zoomed_display_frame.set_color(WHITE)
        zoomed_display.shift(DOWN)
        ##########################
        line2 = Line(start=[1.98, 1.65, 0], end=[1.57, 2.04, 0], color=PINK, stroke_width=1)
        line3 = Line(start=[1.57, 2.04, 0], end=[1.57, 1.65, 0], color=GREEN, stroke_width=1)
        line4 = DashedLine(start=[1.57, 1.65, 0], end=[1.98, 1.65, 0], stroke_width=1)
        b2 = Brace(line2, UR, buff=0.00005, sharpness=3, stroke_width=0)
        b2text = b2.get_text("$\\Delta \\theta$", buff=-0.34)
        b2text.scale(0.27)
        b3 = Brace(line3, LEFT, buff=0.02, sharpness=3, stroke_width=0.01)
        b3text = b3.get_text("$\\Delta (sin \\theta )$", buff=-0.88)
        b3text.scale(0.27)
        ##########################(RIGHT,UP,LEFT)
        tri1 = Polygon([1.98, 1.65, 0], [1.57, 2.04, 0], [1.57, 1.65, 0], stroke_width=1, stroke_color=YELLOW, fill_color=GREEN, fill_opacity=0.5)
        tri2 = Polygon([1.98, 0, 0], [1.98, 1.65, 0], [0, 0, 0], stroke_width=1, stroke_color=YELLOW, fill_color=GREEN, fill_opacity=0.5)
        theta1 = ArcBetweenPoints(start=[1.57, 1.93, 0], end=[1.66, 1.95, 0], angle=PI / 6, color=RED, stroke_width=1.3)
        theta2 = MathTex("\\theta", color=RED).scale(0.3).next_to(theta1, DOWN*0.2+RIGHT*0.01)
        ##########################
        tex1 = MathTex("f(x)=sin(x)")
        tex1.to_edge(UP * 1.6 + LEFT * 2.5)
        equal = MathTex("=")
        tex2_l = MathTex("f'(x)", color=GREEN)
        tex2_r = MathTex("\\frac{\\Delta y}{\\Delta x}")
        tex3_r = MathTex("\\frac{\\Delta (sin (\\theta))}{\\Delta \\theta}}")

        tex2 = VGroup(equal, tex2_l, tex2_r)
        equal.next_to(tex1, DOWN, buff=0.9)
        tex2_l.next_to(equal, LEFT)
        tex2_r.next_to(equal, RIGHT)
        tex3_r.next_to(equal, RIGHT)
        tex3 = VGroup(equal, tex2_l, tex3_r)

        tex4 = MathTex("= \\frac{Adj.}{Hyp.}", color=PINK)
        tex4.next_to(tex3, RIGHT)
        tex5 = MathTex("=cos (\\theta)", color=PINK)
        tex5.next_to(tex3, RIGHT)

        tex6 = Tex("What about cos(x)?", color=YELLOW)
        tex6.next_to(tex1, DOWN, buff=0.9)
        ############################################################################
        #chap0
        self.play(Write(plane0_circle))
        self.play(DrawBorderThenFill(plane))
        self.wait(0.5)
        self.play(Write(line1), Write(line_moving))
        self.add(a, tex)
        self.wait()
        self.play(theta_tracker.animate.set_value(40))
        #self.play(theta_tracker.animate.increment_value(140))
        self.play(tex.animate.set_color(YELLOW), run_time=0.5)
        #self.play(theta_tracker.animate.set_value(359))
        self.play(FadeOut(line1))
        self.wait()
        ##############
        #chap1
        #self.play(Write(arc1))
        ruler(self, np.array([0, 0, 0]), np.array([2.56, 0, 0]), angle=(1.1*PI/5))
        self.wait(2)
        ###########
        self.play(Create(frame))
        self.activate_zooming()
        self.wait()
        self.play(Write(line2), Write(line3))
        self.wait()
        self.play(Write(line4))
        self.wait()
        self.play(FadeIn(b2text))
        self.play(FadeIn(b3text))
        self.wait()
        self.play(Write(tri1))
        self.wait()
        self.play(Write(tex1))
        self.play(Write(tex2))
        self.wait(0.7)
        self.play(TransformMatchingTex(tex2_r, tex3_r))
        self.wait()
        self.play(TransformFromCopy(tri1, tri2))
        self.wait()
        self.play(Write(theta1))
        self.wait(0.5)
        self.play(Write(theta2))
        self.wait(2)
        self.play(Write(tex4))
        self.wait(2)
        self.play(Transform(tex4, tex5))
        self.wait(2)
        self.play(FadeOut(tex3, tex5, tex4))
        self.wait()
        self.play(Write(tex6))
        self.wait()







