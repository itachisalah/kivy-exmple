"""
Exercise 0.3
Create a random walker with dynamic probabilities.
For example, can you give it a 50% chance of moving in the direction of the mouse?
"""
from kivy.app import App
from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivy.graphics import Color, Point
from kivy.clock import Clock

from random import randint, random
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

        # With 50% chance moving to where the mouse is
        if random() <= 0.5:
            new_x = np.sign(Window.mouse_pos[0] - last_x)
            new_y = np.sign(Window.mouse_pos[1] - last_y)
        else:
            new_x = randint(-1,1)
            new_y = randint(-1,1)

        # Add the next step based on the previous position
        self.path.add_point(last_x + new_x, last_y + new_y)


class NatureApp(App):

    def build(self):
        return Walker()


if __name__ == "__main__":
    NatureApp().run()
