"""
Take a look at our formula for drag again: drag force = coefficient * speed * speed.
The faster an object moves, the greater the drag force against it. In fact, an
object not moving in water experiences no drag at all. Expand the example to
drop the balls from different heights. How does this affect the drag as they
hit the water?
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


class Box(Widget):

    g = PVector(0, -.1)

    def __init__(self, width, pockets, **kwargs):
        super(Box, self).__init__(**kwargs)
        self.pockets = pockets
        self.size = width, 20
        self.mass = self.size[0] / .1
        self.vel = PVector(0, 0)
        self.acc = PVector(0, 0)

    def update(self, dt):
        gravity = self.g * self.mass
        # Apply drag when the ball is in the water
        drag = self.inWater()

        self.applyForce(gravity)
        self.applyForce(drag)

        self.checkEdge()
        self.move()

    def inWater(self):
        drag = PVector(0,0)

        collisions = map(self.collide_widget, self.pockets)
        for i, collision in enumerate(collisions):
            if collision:
                magnitude = 2 * self.vel.length2() * self.size[0] # surface area
                drag = -1 * self.vel.normalize() * magnitude

        return drag

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
        water = Pocket(size=(Window.width, 150), pos=(0,0), c=[.5, .5, .5, 1])
        self.add_widget(water)

        # add balls
        for width, pos in zip([50, 100, 150],[100, 300, 600]):
            self.add_balls(width=width, pos=pos, pockets=[water])

    def add_balls(self, width, pos, pockets):
        wid = Box(width=width, pos=(pos, 400), pockets=pockets)

        self.add_widget(wid)
        Clock.schedule_interval(wid.update, .01)


class NatureApp(App):

    def build(self):
        return Universe()


if __name__ == "__main__":
    NatureApp().run()
