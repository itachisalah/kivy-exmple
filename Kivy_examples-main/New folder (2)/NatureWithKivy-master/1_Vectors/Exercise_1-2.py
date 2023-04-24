"""
Exercise 1-2
Take one of the walker examples from the introduction and convert it to use Vectors.
"""

from kivy.app import App
from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivy.graphics import Color, Point
from kivy.clock import Clock
from kivy.vector import Vector

from random import randint, random
import numpy as np


class Walker(Widget):

    def __init__(self, **kwargs):
        super(Walker, self).__init__(**kwargs)

        with self.canvas:
            self.point = Point(points=[*Window.center])


    def update(self, *args):

        # Get current position
        last_pos = Vector(self.point.points[-2], self.point.points[-1])

        # With 50% chance moving to where the mouse is
        if random() <= 0.5:
            direction = np.sign(Vector(Window.mouse_pos) - last_pos)
            new_pos = Vector(direction) + last_pos
        else:
            new_pos = Vector(randint(-1,1), randint(-1,1)) + last_pos

        # Add the next step based on the previous position
        self.point.add_point(new_pos.x, new_pos.y)


class WalkerApp(App):

    def build(self):
        w = Walker()

        # Update the its own position every 0.1 second
        Clock.schedule_interval(w.update, 0.1)
        return w


if __name__ == "__main__":
    WalkerApp().run()
