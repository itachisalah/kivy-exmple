"""
Change the attraction force in Example 2.8 to a repulsion force. Can you create
an example in which all of the Mover objects are attracted to the mouse, but
repel each other? Think about how you need to balance the relative strength of
the forces and how to most effectively use distance in your force calculations.
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


class Ball(Widget):

    G = 0.5  # Gravitational Constant
    color = ListProperty([0,0,0,0])

    def __init__(self, size, index, neighbors=None, **kwargs):
        super(Ball, self).__init__(**kwargs)
        self.size = size, size
        self.mass = size / 2
        self.index = index
        self.vel = PVector(0, 0)
        self.acc = PVector(0, 0)
        self.neighbors = neighbors
        self.color = [1,1,1,.7] 

        #with self.canvas:
        #    self.path = Point(points=self.center)

    def update(self, dt):
        # Attract by mouse
        toMouse = (PVector(Window.mouse_pos) - self.pos) * .01
        self.applyForce(toMouse)
        # Repel by neighbors
        for neighbor in self.neighbors:
            if self.index != neighbor.index:
                RepelForce = self.computeRepulsion(neighbor)
                self.applyForce(RepelForce)

        self.move()
        # Update the current position to its own path
        #self.path.add_point(self.center_x, self.center_y)

    def computeRepulsion(self, obj):
        vec = PVector(self.pos) - obj.pos
        dist = vec.length()
        dist = self.constrain(dist, 5, 25)
        dir = vec.normalize()
        mag = self.G * self.mass * obj.mass / (dist * dist)
        RepelForce = dir * mag
        return RepelForce

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
        # Add balls
        self.balls = self.add_child(10)

    def add_child(self, val):
        children = {}
        for i in range(val):
            pos_x, pos_y = self.randomPos()

            b = Ball(pos=(pos_x, pos_y), size=randint(10, 50), index=i)
            children[b] = i
            self.add_widget(b)
            Clock.schedule_interval(b.update, .01)
        return children

    def randomPos(self, cond="f"):
        w, h = Window.width, Window.height
        if cond == "r": # restricted window
            return randint(w/5, 4*w/5), randint(h/5, 4*h/5)
        else:           # full window
            return randint(0, w), randint(0, h)


class NatureApp(App):

    def build(self):
        u = Universe()
        # Update the list of neighbors in the universe,
        # so that they can attract to each other
        for ball in u.balls:
            ball.neighbors = u.balls
        return u



if __name__ == "__main__":
    NatureApp().run()
