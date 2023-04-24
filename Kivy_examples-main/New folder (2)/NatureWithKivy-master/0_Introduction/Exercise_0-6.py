"""
Exercise 0.6
Use a custom probability distribution to vary the size of a step taken by the
random walker. The step size can be determined by influencing the range of
values picked. Can you map the probability exponentially — i.e. making the
likelihood that a value is picked equal to the value squared?
"""
from kivy.app import App
from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivy.graphics import Color, Point
from kivy.clock import Clock

from random import randint
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

        # Pick a step size according to how far the step is
        stepsize = self.pickStep()

        # Generate random steps with different step size
        new_x = randint(-1,1) * stepsize
        new_y = randint(-1,1) * stepsize

        # Add the next step based on the previous position
        self.path.add_point(last_x + new_x, last_y + new_y)

    def pickStep(self):

        while True:
            newStep = randint(1,10)
            threshold = randint(1,100)

            # The bigger the step the greater the possibility to get chosen.
            if threshold <= (newStep ** 2):
                break
            else:
                pass

        return newStep


class NatureApp(App):

    def build(self):
        return Walker()


if __name__ == "__main__":
    NatureApp().run()
