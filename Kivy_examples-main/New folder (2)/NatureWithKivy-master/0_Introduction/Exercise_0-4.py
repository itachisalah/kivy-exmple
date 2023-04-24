"""
Exercise 0.4
Consider a simulation of paint splatter drawn as a collection of colored dots.
Most of the paint clusters around a central location, but some dots do splatter
out towards the edges.
Can you use a normal distribution of random numbers to generate the locations
of the dots? Can you also use a normal distribution of random numbers to
generate a color palette?
"""
from kivy.app import App
from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivy.graphics import Color, Ellipse
from kivy.clock import Clock

from functools import partial
from random import gauss


class NatureApp(App):

    def add_dots(self, wid, *args):

        # Generate normal random position with mean in center of the window
        ran_x = gauss(Window.width/2, 80)
        ran_y = gauss(Window.height/2, 50)

        # Generate normal random values between 0 and 1
        ran_r = gauss(0.5, 0.2)
        ran_g = gauss(0.5, 0.2)
        ran_b = gauss(0.5, 0.2)

        # Draw dots
        with wid.canvas:
            Color(ran_r, ran_g, ran_b)
            Ellipse(pos=(ran_x, ran_y), size= (8, 8))

    def build(self):

        root = Widget()
        Clock.schedule_interval(partial(self.add_dots, root), 0.1)

        return root



if __name__ == "__main__":
    NatureApp().run()
