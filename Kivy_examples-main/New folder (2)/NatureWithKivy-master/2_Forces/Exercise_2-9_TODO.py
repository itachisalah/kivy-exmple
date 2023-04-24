"""
In the example above, we have a system (i.e. array) of Mover objects and one
Attractor object. Build an example that has systems of both movers and attractors.
What if you make the attractors invisible? Can you create a pattern/design from
the trails of objects moving around attractors? See the Metropop Denim project
by Clayton Cubitt and Tom Carden for an example.
"""

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import ListProperty
from kivy.graphics import Point

import numpy as np
from random import randint
from noise import pnoise1
from lib.pvector import PVector


class Attractor(Widget):

    color = ListProperty([0,0,0,0])

    def __init__(self, size, **kwargs):
        super(Attractor, self).__init__(**kwargs)
        self.size = size, size
        self.mass = size * 2
        self.color = [0, 0, 0, 1] # Make them invisible


class Ball(Widget):

    G = 0.5  # Gravitational Constant
    color = ListProperty([0,0,0,0])

    def __init__(self, size, objs, **kwargs):
        super(Ball, self).__init__(**kwargs)
        self.size = size, size
        self.mass = size / 2
        self.vel = PVector(0, 0)
        self.acc = PVector(0, 0)
        self.objs = objs
        self.color = [1,1,1,.7] # Make them invisible

        with self.canvas:
            self.path = Point(points=self.pos)

    def update(self, dt):
        for obj in self.objs:
            GraviForce = self.computeAttraction(obj)
            self.applyForce(GraviForce)
        self.move()
        # Update the current position to its own path
        self.path.add_point(self.pos[0], self.pos[1])

    def computeAttraction(self, obj):
        dist = (PVector(obj.pos) - self.pos).length()
        dist = self.constrain(dist, 5, 25)
        attractMag = self.G * self.mass * obj.mass / (dist * dist)
        dir = (PVector(obj.pos) - self.pos).normalize()
        GraviForce = dir * attractMag
        return GraviForce

    def constrain(self, value, min, max):
        if value < min:
            value = min
        elif value > max:
            value = max
        return value

    def applyForce(self, force):
        acc = force / self.mass
        self.acc += acc

    def move(self):
        self.vel += self.acc
        self.vel.limit(10)
        self.pos = PVector(self.pos) + self.vel
        self.acc *= 0


class Universe(FloatLayout):

    def __init__(self, **kwargs):
        super(Universe, self).__init__(**kwargs)
        # Add attractor
        attractors = self.add_attractor(4)
        # Add balls
        self.add_child(10, attractors)

    def add_attractor(self, val):
        attractors = []
        for _ in range(val):
            pos_x, pos_y = self.randomPos(cond="f")

            a = Attractor(pos=(pos_x, pos_y), size=50)
            self.add_widget(a)
            attractors.append(a)
        return attractors

    def add_child(self, val, objs):
        for _ in range(val):
            pos_x, pos_y = self.randomPos()

            b = Ball(pos=(pos_x, pos_y), size=randint(10, 50), objs=objs)
            self.add_widget(b)
            Clock.schedule_interval(b.update, .01)

    def randomPos(self, cond="f"):
        w, h = Window.width, Window.height
        if cond == "r": # restricted window
            return randint(w/5, 4*w/5), randint(h/5, 4*h/5)
        else:           # full window
            return randint(0, w), randint(0, h)


class NatureApp(App):

    def build(self):
        return Universe()



if __name__ == "__main__":
    NatureApp().run()
