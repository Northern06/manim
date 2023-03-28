from manim import *

class Shapes(Scene):
    def construct(self):
        t = ValueTracker(0)
        cir = Circle(radius=2).shift(LEFT*5)
        dot_o = Dot(LEFT*5)
        dot_a = Dot(LEFT*3)
        l_oa = Line(LEFT*5,LEFT*3)
        dot_p = Dot().add_updater(lambda a:a.move_to(
            np.array([-5+2*np.cos(t.get_value()),2*np.sin(t.get_value()),0])
        ))
        l_op = Line(LEFT*5,LEFT*3).add_updater(lambda a:a.put_start_and_end_on(
            dot_o.get_center(),dot_p.get_center()
        ))
        arc = Arc(angle=0).add_updater(lambda a:a.become(
            Arc(start_angle=0,angle=t.get_value()%TAU,color=ORANGE).shift(LEFT*5)
        ))

        self.add(cir,dot_o,dot_a,dot_p,l_oa,l_op,arc)
        self.play(t.set_value,2*TAU,run_time=8,rate_func=linear)
