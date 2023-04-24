"""
String together a series of pendulums so that the endpoint of one is the origin
point of another. Note that doing this may produce intriguing results but will
be wildly inaccurate physically. Simulating an actual double pendulum involves
sophisticated equations, which you can read about here:
http://scienceworld.wolfram.com/physics/DoublePendulum.html.

TODO: Program a draggable pendulum
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


class Pendulum(Widget):

    # Gravitational constant in a simulated world
    g = -1
    # Center of the ball
    ball_x, ball_y = NumericProperty(), NumericProperty()
    pivot_x, pivot_y = NumericProperty(), NumericProperty()

    def __init__(self, pivot, secondP=[], **kwargs):
        super(Pendulum, self).__init__(**kwargs)
        self.size = (30, 30)
        self.r = 250
        self.theta = 45
        self.pivot_x, self.pivot_y = pivot
        self.pos = PVector(self.r * sin(self.theta), -self.r * cos(self.theta))
        self.mass = 1
        self.aVel = 0
        self.aAcc = 0
        self.sP = secondP


    def update(self, *args):
        self.aAcc = self.g * sin(self.theta) / self.r
        self.aVel += self.aAcc
        self.theta += self.aVel

        loc = PVector(self.r * sin(self.theta), -self.r * cos(self.theta))
        self.pos = loc + [self.pivot_x, self.pivot_y]
        self.ball_x, self.ball_y = self.get_ball_pos()

        # Update its pivot based on the other pendulum
        if self.sP:
            self.pivot_x, self.pivot_y = self.sP[0].ball_x, self.sP[0].ball_y

        self.aVel *= .995 # Damping


    def get_ball_pos(self):
        ball_x = self.x + self.size[0] / 2
        ball_y = self.y + self.size[1] / 2
        return ball_x, ball_y


class Universe(Widget):

    def __init__(self, **kwargs):
        super(Universe, self).__init__(**kwargs)
        p1 = Pendulum(pivot=[0, 300])
        p2 = Pendulum(pivot=[p1.ball_x, p1.ball_y], secondP=[p1])

        self.add_widget(p1)
        self.add_widget(p2)

        Clock.schedule_interval(p1.update, .05)
        Clock.schedule_interval(p2.update, .05)


class NatureApp(App):

    def build(self):
        return Universe()



if __name__ == "__main__":
    NatureApp().run()
