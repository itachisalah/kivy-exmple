"""
Instead of objects bouncing off the edge of the wall, create an example in which
an invisible force pushes back on the objects to keep them in the window.
Can you weight the force according to how far the object is from an edge
 — i.e., the closer it is, the stronger the force?
"""

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import ListProperty

import numpy as np
from random import randint
from noise import pnoise1
from lib.pvector import PVector


class Ball(Widget):

    color = ListProperty([0,0,0,0])
    tx = randint(0, 10000)

    def __init__(self, size, **kwargs):
        super(Ball, self).__init__(**kwargs)
        self.size = size, size
        self.mass = size / 5
        self.vel = PVector(0, 0)
        self.acc = PVector(0, 0)
        self.color = [1,1,1,.7]

    def update(self, dt):
        gravity = PVector(0, .1)
        wind = PVector(pnoise1(self.tx), 0) * .5
        # The closer to the wall is, the stronger the bouncing force... it is
        # in some way like the farer away from center, the stronger the attracting force.
        rebounce = (PVector(Window.center) - self.pos - self.size) * .005

        self.applyForce(gravity)
        self.applyForce(wind)
        self.applyForce(rebounce)

        self.checkEdge()
        self.move()

        self.tx += .01

    def move(self):
        self.vel += self.acc
        self.vel.limit(10)
        self.pos = PVector(self.pos) + self.vel
        self.acc *= 0

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

    def applyForce(self, force):
        acc = force / self.mass
        self.acc += acc


class Universe(FloatLayout):

    def __init__(self, **kwargs):
        super(Universe, self).__init__(**kwargs)
        for _ in range(5):
            self.add_child()

    def add_child(self):
        pos_x = randint(0, Window.width)
        pos_y = randint(0, Window.height)
        b = Ball(pos=(pos_x, pos_y), size=randint(10, 50))

        self.add_widget(b)
        Clock.schedule_interval(b.update, .01)


class NatureApp(App):

    def build(self):
        return Universe()



if __name__ == "__main__":
    NatureApp().run()
