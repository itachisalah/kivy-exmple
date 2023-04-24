"""
Exercise 0.7
In the above random walker, the result of the noise function is mapped directly
to the Walker’s location. Create a random walker where you instead map the
result of the noise() function to a Walker’s step size.
"""
from kivy.app import App
from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivy.graphics import Color, Point, Ellipse
from kivy.clock import Clock

from random import randint, random
from noise import pnoise1
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

        # Set a starting point for Perlin noise
        self.tx = randint(1,10000)
        self.ty = randint(1,10000)

        # Update the its own position every 0.1 second
        Clock.schedule_interval(self.update, .1)

    def update(self, *args):

        # Get current position
        last_x = self.path.points[-2]
        last_y = self.path.points[-1]

        # Pick a step size according to how far the step is
        newStepX, newStepY = self.pickStep()

        # Generate random steps with different step size
        new_x = randint(-1,1) * newStepX
        new_y = randint(-1,1) * newStepY

        # Add the next step based on the previous position
        self.path.add_point(last_x + new_x, last_y + new_y)

        # Update tx and ty for next movement
        self.tx += .01
        self.ty += .01

    def pickStep(self):

        newStepX = np.interp(pnoise1(self.tx), [-1,1], [0,10])
        newStepY = np.interp(pnoise1(self.ty), [-1,1], [0,10])

        return newStepX, newStepY


class NatureApp(App):

    def build(self):
        return Walker()


if __name__ == "__main__":
    NatureApp().run()
