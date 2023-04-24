"""
Create a simulation of a vehicle that you can drive around the screen using the
arrow keys: left arrow accelerates the car to the left, right to the right.
The car should point in the direction in which it is currently moving.


TODO: Fix the weird behavior when the vehicle's velocity is close to zero
(Find a way to update the heading vector)
"""

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.properties import ListProperty, NumericProperty, ObjectProperty
from kivy.graphics import *

from lib.pvector import PVector
from random import randint

class Car(Widget):

    angle = NumericProperty()

    def __init__(self, **kwargs):
        super(Car, self).__init__(**kwargs)
        self.pos = Window.center
        self.size = (30, 50)
        self.heading = PVector(0, 1)
        self.mass = 1
        self.vel = PVector(0, 0)
        self.acc = PVector(0, 0)

    def update(self, dt):
        friction = self.vel.normalize() * -0.1
        self.applyForce(friction)

        self.checkEdge()
        self.move()

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

    def move(self):
        self.vel += self.acc
        self.vel.limit(30)

        # Calculate the angle rotated from initial heading
        self.angle = self.vel.angle(PVector(0, 1))

        # Update the current heading according to the velocity vector
        if self.vel.length() > 0.1:
            self.heading = self.vel.normalize()

        self.pos = PVector(self.pos) + self.vel
        self.acc *= 0


class Universe(Widget):


    def __init__(self, **kwargs):
        super(Universe, self).__init__(**kwargs)
        Window.bind(on_key_down=self._keydown)
        self.car = Car()
        self.add_widget(self.car)
        Clock.schedule_interval(self.car.update, .05)

    def _keydown(self, instance, key, *args):
        '''Keycode ref
        https://github.com/kivy/kivy/blob/master/kivy/core/window/__init__.py
        '''
        # Key Up
        if key == 273:
            self.car.applyForce(self.car.heading)
        # Key Down
        elif key == 274:
            self.car.applyForce(-self.car.heading)
        # Key Left
        elif key == 276:
            self.car.applyForce(self.car.heading.rotate(90) * 0.2)
        # Key Right
        elif key == 275:
            self.car.applyForce(self.car.heading.rotate(-90) * 0.2)

class NatureApp(App):

    def build(self):
        return Universe()



if __name__ == "__main__":
    NatureApp().run()
