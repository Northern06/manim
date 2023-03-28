from manim import *


class text(Scene):
    def construct(self):
        word = Title(
            "Review: Derivative and its application",
            font_size=60
        )
        tex = BulletedList(
            "Geometric interpretation",
            "Apply: $(sinx)'=cosx$"
        )
        VGroup(word, tex).arrange(DOWN, buff=0.6)
        self.play(Write(word))
        self.wait()
        self.play(Write(tex))
        self.wait()
        self.play(FadeOut(word))
        self.play(FadeOut(tex))
        self.wait()


