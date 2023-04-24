"""
Redo Example 6.8 so that the behavior weights are not constants. What happens if they change over time
(according to a sine wave or Perlin noise)? Or if some vehicles are more concerned with seeking and others more
concerned with separating? Can you introduce other steering behaviors as well?

ANS:
Implemented perlin noise for separating and seeking behavior individually.
TODO: Other steering behavior is not yet introduced.
"""

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.properties import NumericProperty, ListProperty
from lib.pvector import PVector
from random import randint
from noise import pnoise1
import numpy as np


class Boid(Widget):

    angle = NumericProperty()
    target = ListProperty([0, 0])
    maxForce = 0.2
    maxSpeed = 4
    desiredSeparation = 30

    def __init__(self, neighbors=None, *args, **kwargs):
        super(Boid, self).__init__(*args, **kwargs)
        self.size = 20, 20
        self.heading = PVector(0, 1)
        self.mass = 1
        self.vel = PVector(randint(-2, 2), randint(-2, 2))
        self.acc = PVector(0, 0)
        self.neighbors = neighbors
        self.tx = randint(0, 10000)  # Input for perlin noise
        self.ty = randint(0, 10000)  # Input for perlin noise


    def update(self, dt):
        self.applyBehavior()
        self.applyRotation()
        self.checkEdge()
        self.move()


    def applyBehavior(self):
        separateF = self.separate()
        seekF = self.seek(Window.mouse_pos)
        # scale separation force according to Perlin noise
        self.applyForce(separateF * np.interp(pnoise1(self.tx), [-1,1], [1,10]).item())
        self.applyForce(seekF * np.interp(pnoise1(self.ty), [-1,1], [1,3]).item())

        self.tx += .01
        self.ty += .01

    def separate(self):
        sum = PVector(0,0)
        count = 0

        for neighbor in self.neighbors:
            if neighbor != self:
                diff = PVector(self.pos)- neighbor.pos
                dist = diff.length()
                if dist < self.desiredSeparation:
                    diff.normalize()
                    diff /= dist
                    sum += diff
                    count += 1

        if count > 0:
            sum /= count
            sum.normalize()
            sum *= self.maxSpeed

            steeringForce = sum - self.vel
            steeringForce.limit(self.maxForce)

            return steeringForce

        return PVector(0,0)


    def seek(self, target):
        desired_vel = PVector(target) - self.pos
        desired_vel.limit(self.maxSpeed)

        steeringForce = desired_vel - self.vel
        steeringForce.limit(self.maxForce)

        return steeringForce


    def checkEdge(self):
        # check horizontal border
        if self.center_x > Window.width:
            self.center_x = 0
        elif self.center_x <= 0:
            self.center_x = Window.width

        # check vertical border
        if self.center_y > Window.height:
            self.center_y = 0
        elif self.center_y <= 0:
            self.center_y = Window.height


    def applyForce(self, force):
        acc = force / self.mass
        self.acc += acc


    def applyRotation(self):
        self.angle = self.vel.angle(self.heading)


    def move(self):
        self.vel += self.acc
        self.vel.limit(self.maxSpeed)
        self.pos = self.vel + self.pos
        self.acc *= 0


def randomPos(width=Window.width, height=Window.height):
    w, h = width, height
    return randint(0, w), randint(0, h)


class Universe(Widget):

    def __init__(self, *args, **kwargs):
        super(Universe, self).__init__(*args, **kwargs)
        self.add_child(30)

    def add_child(self, val):
        self.boids = list()

        for _ in range(val):
            pos_x, pos_y = randomPos()

            b = Boid(pos=(pos_x, pos_y))
            self.boids.append(b)
            self.add_widget(b)

        for child in self.boids:
            child.neighbors = self.boids
            Clock.schedule_interval(child.update, 1/60)


class NatureApp(App):
    def build(self):
        return Universe()


if __name__ == "__main__":
    NatureApp().run()
