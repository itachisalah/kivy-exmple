"""
Try using the Perlin noise function instead of sine or cosine with the above example.
"""

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.properties import ListProperty, NumericProperty, ObjectProperty
from kivy.graphics import *

from lib.pvector import PVector
from random import randint, uniform
from math import sin, cos, pi
from noise import pnoise1
import numpy as np


class Oscillator(Widget):

    def __init__(self, loc, angle, **kwargs):
        super(Oscillator, self).__init__(**kwargs)
        self.size = (30, 30)
        self.pos = loc, 0
        self.amp = 100
        self.angle = angle
        self.vel = .01
        self.acc = .001

        Clock.schedule_interval(self.update, .05)

    def update(self, dt):
        self.vel += self.acc
        self.angle += self.vel
        self.y = self.amp * pnoise1(self.angle)
        

class Universe(Widget):

    def __init__(self, **kwargs):
        super(Universe, self).__init__(**kwargs)
        # Location of pos x
        locs = np.arange(-350, 400, 50).tolist()
        # location of pos y
        angle = .2

        for loc in locs:
            self.add_widget(Oscillator(loc, angle))
            angle += .4


class NatureApp(App):

    def build(self):
        return Universe()



if __name__ == "__main__":
    NatureApp().run()
