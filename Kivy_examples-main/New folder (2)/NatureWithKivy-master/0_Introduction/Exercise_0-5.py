"""
Exercise 0.5
A Gaussian random walk is defined as one in which the step size (how far the
object moves in a given direction) is generated with a normal distribution.
Implement this variation of our random walk.
"""
from kivy.app import App
from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivy.graphics import Color, Point
from kivy.clock import Clock

from random import randint, gauss
import numpy as np


class Walker(Widget):

    def __init__(self, *args, **kwargs):
        super(Walker, self).__init__(*args, **kwargs)

        # Initialize the Walker
        with self.canvas:
            # Define the color of stroke
            Color(1, 1, 1)
            # Walker's initial position
            self.path = Point(points = Window.center)

        # Update the its own position every 0.1 second
        Clock.schedule_interval(self.update, 0.1)

    def update(self, *args):

        # Get current position
        last_x = self.path.points[-2]
        last_y = self.path.points[-1]

        # Normal distributed multiplier with mean 3 and std 1
        stepsize = gauss(3,1)

        # Generate random steps with different step size
        new_x = randint(-1,1) * stepsize
        new_y = randint(-1,1) * stepsize

        # Add the next step based on the previous position
        self.path.add_point(last_x + new_x, last_y + new_y)


class NatureApp(App):

    def build(self):
        return Walker()


if __name__ == "__main__":
    NatureApp().run()
