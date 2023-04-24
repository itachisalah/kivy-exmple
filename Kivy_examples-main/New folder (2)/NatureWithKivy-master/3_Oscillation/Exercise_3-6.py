"""
Using the sine function, create a simulation of a weight (sometimes referred to
as a “bob”) that hangs from a spring from the top of the window. Use the map()
function to calculate the vertical location of the bob. Later in this chapter,
we’ll see how to recreate this same simulation by modeling the forces of a spring
according to Hooke’s law.
"""

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.properties import ListProperty, NumericProperty, ObjectProperty
from kivy.graphics import *

from lib.pvector import PVector
from random import randint
from math import sin, cos, pi


class Universe(Widget):


    def __init__(self, **kwargs):
        super(Universe, self).__init__(**kwargs)
        self.size = 20, 20
        self.frameCount = 0
        self.amp = 150

        with self.canvas:
            Color(1,1,1,1)
            self.bob = Ellipse(pos=self.center, size=self.size)
            self.line = Line(points=(self.x + 10, Window.height, self.x + 10, self.y + 10), width=2)

        self.bind(pos=self.update_canvas)

        Clock.schedule_interval(self.update, .01)

    def update(self, dt):
        self.y = Window.center[1] + self.amp * sin(2 * pi * self.frameCount / 100)
        self.frameCount += 1

    def update_canvas(self, *args):
        self.bob.pos = self.pos
        self.line.points = (self.x + 10, Window.height, self.x + 10, self.y + 10)

class NatureApp(App):

    def build(self):
        return Universe(pos=Window.center)



if __name__ == "__main__":
    NatureApp().run()
