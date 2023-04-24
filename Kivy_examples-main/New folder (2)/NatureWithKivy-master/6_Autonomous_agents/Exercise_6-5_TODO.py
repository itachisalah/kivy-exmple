"""
Come up with your own arbitrary scheme for calculating a desired velocity.
"""

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.graphics import *
from kivy.properties import NumericProperty
from lib.pvector import PVector
from random import uniform, random
import numpy as np



class Car(Widget):

    angle = NumericProperty()

    def __init__(self, **kwargs):
        super(Car, self).__init__(**kwargs)
        self.size = (30, 50)
        self.pos = PVector(Window.center) - PVector(self.size)/2
        self.heading = PVector(0, 1)
        self.mass = 1
        self.vel = PVector(0, 1)
        self.acc = PVector(0, 0)


    def update(self, dt):
        self.seek()
        self.applyRotation()
        self.checkEdge()
        self.move()


    def seek(self):
        goal = self.setGoal()
        desired_vel = goal - PVector(self.pos)
        desired_vel.limit(10)

        steeringForce = desired_vel - self.vel
        steeringForce.limit(.7)

        self.applyForce(steeringForce)


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
        self.vel.limit(30)
        self.pos = PVector(self.pos) + self.vel
        self.acc *= 0

    def setGoal(self):
        # Pick a point at distance apart from current location
        targetPos = self.vel.normalize() * 10 + self.pos
        # Randomly pick an angle between 0 and 180
        # and calculate the position on the circumference (radius = 5)
        angle = random() * 360
        dir = self.vel.normalize().rotate(angle)
        goal = targetPos + dir

        return goal

class Universe(Widget):

    def __init__(self, **kwargs):
        super(Universe, self).__init__(**kwargs)
        self.car = Car()
        self.add_widget(self.car)
        Clock.schedule_interval(self.car.update, .05)


class NatureApp(App):

    def build(self):
        return Universe()



if __name__ == "__main__":
    NatureApp().run()
