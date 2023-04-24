"""
Exercise 0.1
Create a random walker that has a tendency to move down and to the right.
"""
from kivy.app import App
from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivy.graphics import Color, Point
from kivy.clock import Clock

from random import randint, choice, random


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

        # With a tendency (60%) moving down and right
        new_x = choice([-1]*2 + [0]*2 + [1]*6)
        new_y = choice([-1]*6 + [0]*2 + [1]*2)

        # Add the next step based on the previous position
        self.path.add_point(last_x + new_x, last_y + new_y)


class NatureApp(App):

    def build(self):
        return Walker()


if __name__ == "__main__":
    NatureApp().run()
