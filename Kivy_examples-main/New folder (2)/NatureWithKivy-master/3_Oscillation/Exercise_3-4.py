"""
Using Example 3.4 as a basis, draw a spiral path. Start in the center and move
outwards. Note that this can be done by only changing one line of code and
adding one line of code!
"""

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.properties import ListProperty, NumericProperty, ObjectProperty
from kivy.graphics import *

from lib.pvector import PVector
from random import randint
from math import sin, cos


class Universe(Widget):


    def __init__(self, **kwargs):
        super(Universe, self).__init__(**kwargs)
        self.pos = Window.center
        self.size = 20, 20
        self.r = 10
        self.theta = 0

        with self.canvas:
            self.line = Point(points=(self.x + self.r*sin(self.theta), \
                                      self.y + self.r*cos(self.theta)),\
                              pointsize=5)

        Clock.schedule_interval(self.update, .05)

    def update(self, dt):
        self.r += .2
        self.theta += .05
        new_x = self.x + self.r*sin(self.theta)
        new_y = self.y + self.r*cos(self.theta)

        self.line.add_point(new_x, new_y)


class NatureApp(App):

    def build(self):
        return Universe()



if __name__ == "__main__":
    NatureApp().run()
