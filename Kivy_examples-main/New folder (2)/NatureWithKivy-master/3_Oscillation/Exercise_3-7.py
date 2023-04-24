"""
Try initializing each Oscillator object with velocities and amplitudes that are
not random to create some sort of regular pattern. Can you make the oscillators
appear to be the legs of a insect-like creature?
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
import numpy as np



class Oscillator(Widget):

    def __init__(self, loc, angle, **kwargs):
        super(Oscillator, self).__init__(**kwargs)
        self.size = (30, 30)
        self.pos = loc, 0
        self.amp = 100
        self.angle = angle
        self.vel = .1

        Clock.schedule_interval(self.update, .05)

    def update(self, dt):
        self.angle += self.vel

        self.y = self.amp * sin(self.angle)


class Universe(Widget):

    def __init__(self, **kwargs):
        super(Universe, self).__init__(**kwargs)
        # Location of pos x
        locs = np.arange(-350, 400, 50).tolist()
        # location of pos y
        angle = .2

        for loc in locs:
            self.add_widget(Oscillator(loc, angle))
            # advance in phase
            angle += .4


class NatureApp(App):

    def build(self):
        return Universe()



if __name__ == "__main__":
    NatureApp().run()
