"""
Create an example that simulates a box sliding down the incline with friction.
Note that the magnitude of the friction force is equal to the normal force.
"""

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.properties import ListProperty, NumericProperty
from kivy.graphics import *

from lib.pvector import PVector
from math import sin, cos, radians


class Bob(Widget):

    def __init__(self, **kwargs):
        super(Bob, self).__init__(**kwargs)
        self.size = 30, 30
        self.pos = 100, 100
        self.mass = 1
        self.vel = PVector(0, 0)
        self.acc = PVector(0, 0)


class Spring(Widget):

    g = PVector(0, -0.4)

    anchor = ListProperty([0, 0])
    ball_x, ball_y = NumericProperty(), NumericProperty()

    def __init__(self, bob, **kwargs):
        super(Spring, self).__init__(**kwargs)
        self.connect(bob)
        self.anchor = 0, 300
        self.restLength = 200
        self.k = .05

    def update(self, *args):
        # Spring Force
        dir = self.constrainLength(20, 500)
        x = dir.length() - self.restLength
        springForce = dir.normalize() * self.k * x
        self.applyForce(springForce)

        # Gravity
        graviForce = self.bob.mass * self.g
        self.applyForce(graviForce)

        # Track the position of the bob
        self.ball_x, self.ball_y = self.ball_center()

    def constrainLength(self, min, max):
        dir = PVector(self.anchor) - [self.ball_x, self.ball_y]

        if dir.length() > max:
            dir = dir.normalize() * max
            self.bob.pos = PVector(self.anchor) + dir
            self.bob.vel *= 0
        elif dir.length() < min:
            dir = dir.normalize() * min
            self.bob.pos = PVector(self.anchor) + dir
            self.bob.vel *= 0

        return dir

    def applyForce(self, force):
        self.bob.acc += force / self.bob.mass
        self.bob.vel += self.bob.acc
        self.bob.vel *= .995   # Damping
        self.bob.pos = PVector(self.bob.pos) + self.bob.vel
        self.bob.acc *= 0

    def ball_center(self):
        ball_x = self.bob.x + self.bob.size[0]/2
        ball_y = self.bob.y + self.bob.size[1]/2
        return ball_x, ball_y

    def connect(self, bob):
        self.bob = bob
        self.add_widget(bob)


class Universe(Widget):

    def __init__(self, **kwargs):
        super(Universe, self).__init__(**kwargs)
        self.bob = Bob()
        self.spring = Spring(self.bob)

        self.add_widget(self.spring)

        Clock.schedule_interval(self.spring.update, .05)


class NatureApp(App):

    def build(self):
        return Universe()



if __name__ == "__main__":
    NatureApp().run()
