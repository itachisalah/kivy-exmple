"""
Implement seeking a moving target, often referred to as “pursuit.” In this case,
your desired vector won’t point towards the object’s current location, but rather
its “future” location as extrapolated from its current velocity. We’ll see this
ability for a vehicle to “predict the future” in later examples.
"""

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.graphics import *
from kivy.properties import NumericProperty
from lib.pvector import PVector
from random import randint, random
import numpy as np



class Car(Widget):

    angle = NumericProperty()

    def __init__(self, **kwargs):
        super(Car, self).__init__(**kwargs)
        self.size = (30, 50)
        self.pos = PVector(Window.center) - PVector(self.size)/2
        self.heading = PVector(0, 1)
        self.mass = 1
        self.vel = PVector(0, 0)
        self.acc = PVector(0, 0)


    def update(self, dt):
        self.seek()
        self.applyRotation()
        self.checkEdge()
        self.move()


    def seek(self):
        # Simply reversing the direction of desired velocity
        # and you get the fleeing behavior
        desired_vel = PVector(self.pos) - PVector(Window.mouse_pos)
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
