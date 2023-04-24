"""
Create pockets of friction in a Processing sketch so that objects only
experience friction when crossing over those pockets. What if you vary the
strength (friction coefficient) of each area? What if you make some pockets
feature the opposite of friction—i.e., when you enter a given pocket you
actually speed up instead of slowing down?
"""

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import ListProperty

import numpy as np
from random import random, randint
from noise import pnoise1
from lib.pvector import PVector


class Pocket(Widget):

    color = ListProperty([0,0,0,0])

    def __init__(self, size, pos, c, coef=1, **kwargs):
        super(Pocket, self).__init__(**kwargs)
        self.size = size
        self.pos = pos
        self.fric_coef = coef

        if isinstance(c, list):
            self.color = c
        elif isinstance(c, str):
            if c == "r":
                self.color = [.5, 0, 0, 1]
            elif c == "g":
                self.color = [0, .5, 0, 1]
            elif c == "b":
                self.color = [0, 0, .5, 1]
            else:
                r = random()
                self.color = [r(), r(), r(), 1]


class Ball(Widget):

    g = PVector(0, -.1)

    def __init__(self, size, pockets, **kwargs):
        super(Ball, self).__init__(**kwargs)
        self.pockets = pockets
        self.size = size, size
        self.mass = size / 5
        self.vel = PVector(0, 0)
        self.acc = PVector(0, 0)

    def update(self, dt):
        gravity =  self.g * self.mass
        friction = - self.vel.normalize() * .05

        # Check whether the balls are inside the pockets, and
        # speed up or down depends on the coef of the pocket
        collisions = map(self.collide_widget, self.pockets)
        for i, collision in enumerate(collisions):
            if collision:
                friction *= self.pockets[i].fric_coef

        self.applyForce(gravity)
        self.applyForce(friction)

        self.checkEdge()
        self.move()

    def applyForce(self, force):
        acc = force / self.mass
        self.acc += acc

    def checkEdge(self):
        # check horizontal border
        if self.x + self.size[0] > Window.width:
            self.vel.x *= -1
            self.x = Window.width - self.size[0]
        elif self.x < 0:
            self.vel.x *= -1
            self.x = 0

        # check vertical border
        if self.y + self.size[1] > Window.height:
            self.vel.y *= -1
            self.y = Window.height - self.size[1]
        elif self.y < 0:
            self.vel.y *= -1
            self.y = 0

    def move(self):
        self.vel += self.acc
        self.vel.limit(10)
        self.pos = PVector(self.pos) + self.vel
        self.acc *= 0


class Universe(FloatLayout):

    def __init__(self, **kwargs):
        super(Universe, self).__init__(**kwargs)
        # add pockets for speeding-up/down balls
        p_up = Pocket(size=(Window.width/2, 100), pos=(0,100), c="r", coef=2)
        p_down = Pocket(size=(Window.width/2, 100), pos=(Window.width/2,100), c="g", coef=-2)
        self.add_widget(p_up)
        self.add_widget(p_down)

        # add balls
        for _ in range(10):
            self.add_balls(pockets=[p_up, p_down])

    def add_balls(self, pockets):
        pos_x = randint(0, Window.width)
        pos_y = 400 # randint(0, Window.height)

        wid = Ball(pos=(pos_x, pos_y), size=20, pockets=pockets)

        self.add_widget(wid)
        Clock.schedule_interval(wid.update, .01)


class NatureApp(App):

    def build(self):
        return Universe()



if __name__ == "__main__":
    NatureApp().run()
