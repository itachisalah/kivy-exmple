"""
Create an example that simulates a box sliding down the incline with friction.
Note that the magnitude of the friction force is equal to the normal force.
"""

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.properties import ListProperty, NumericProperty
from kivy.graphics import *

from lib.pvector import PVector
from random import randint, uniform
from math import sin, cos, pi
from noise import pnoise1
import numpy as np
from functools import partial


class Sled(Widget):

    # Gravitational constant in a simulated world
    g = PVector(0, -.1)

    theta = NumericProperty()

    def __init__(self, **kwargs):
        super(Sled, self).__init__(**kwargs)
        self.size = 50, 30
        self.pos = 0, 500
        self.theta = PVector(800, 0).angle((800, 500))


    def update(self, *args):
        pass



class Universe(Widget):

    def __init__(self, **kwargs):
        super(Universe, self).__init__(**kwargs)

        self.add_widget(Sled())

class NatureApp(App):

    def build(self):
        return Universe()



if __name__ == "__main__":
    NatureApp().run()
