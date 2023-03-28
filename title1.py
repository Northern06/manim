from manim import *


class text(Scene):
    def construct(self):
        word = MathTex(
            "Geometric \\enspace interpretation"
        )

        self.play(Write(word))
        self.wait()
        self.play(FadeOut(word))
        self.wait()

