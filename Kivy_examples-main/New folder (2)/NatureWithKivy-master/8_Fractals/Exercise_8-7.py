"""
Vary the strokeWeight() for each branch. Make the root thick and each subsequent branch thinner.
"""

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.graphics import Line
from kivy.graphics.context_instructions \
    import PushMatrix, PopMatrix, Rotate, Translate
from kivy.core.window import Window


class Universe(Widget):

    def __init__(self, **kwargs):
        super(Universe, self).__init__(**kwargs)
        self.theta = 20
        with self.canvas:
            # Center the tree
            Translate(Window.width / 2, 0, 0)
            self.branch(length=100, thickness=6)

    def branch(self, length, thickness):
            # Draw the trunk
            Line(points=[0, 0, 0, length], width=thickness)
            Translate(0, length, 0)

            length *= .8
            thickness *= .75

            if length > 10:
                # Draw the branches
                PushMatrix()
                Rotate(angle=-self.theta, axis=(0, 0, 1), origin=(0, 0))
                self.branch(length, thickness)
                PopMatrix()

                PushMatrix()
                Rotate(angle= self.theta, axis=(0, 0, 1), origin=(0, 0))
                self.branch(length, thickness)
                PopMatrix()


class NatureApp(App):
    def build(self):
        return Universe()


if __name__ == "__main__":
    NatureApp().run()