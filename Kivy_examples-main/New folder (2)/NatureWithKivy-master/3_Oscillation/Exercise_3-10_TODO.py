"""
Encapsulate the above examples into a Wave class and create a sketch that
displays two waves (with different amplitudes/periods) as in the screenshot
below. Move beyond plain circles and lines and try visualizing the wave in a
more creative way.

TODO: Creative way!
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
        self.vel = .1


        Clock.schedule_interval(self.update, .05)

    def update(self, dt):
        self.angle += self.vel
        self.y = self.amp * sin(self.angle)


class Wave(Widget):

    def __init__(self, ypos, interval, step, **kwargs):
        super(Wave, self).__init__(**kwargs)

        # location of pos x
        ymin, ymax = ypos
        locs = np.arange(ymin, ymax, interval).tolist()
        # phase between two oscillators
        angle = 0

        for loc in locs:
            self.add_widget(Oscillator(loc, angle))
            angle += step


class Universe(Widget):

    def __init__(self, **kwargs):
        super(Universe, self).__init__(**kwargs)
        wave1 = Wave(ypos=(-250, 0), interval=10, step=.1)
        wave2 = Wave(ypos=( 150,300), interval=10, step=.4)

        self.add_widget(wave1)
        self.add_widget(wave2)


class NatureApp(App):

    def build(self):
        return Universe()



if __name__ == "__main__":
    NatureApp().run()
