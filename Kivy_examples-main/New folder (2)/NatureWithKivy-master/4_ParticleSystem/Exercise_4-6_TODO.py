"""
Create a simulation of an object shattering into many pieces. How can you turn one large shape into many small particles?
What if there are several large shapes on the screen and they shatter when you click on them?
"""

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.properties import ListProperty, NumericProperty, ObjectProperty
from kivy.graphics import *

from lib.pvector import PVector
from random import randint, random
from collections import deque
import numpy as np


class Particle(Widget):

    # Gravity
    g = PVector(0, -0.4)
    # Opacity of the particle
    alpha = NumericProperty(1)
    rot = NumericProperty(random()*2 - 1)

    def __init__(self, vel, **kwargs):
        super(Particle, self).__init__(**kwargs)
        self.size = 20, 20
        self.mass = 1
        self.vel = PVector(vel)
        self.acc = PVector(randint(-1, 1), randint(-1, 1))
        self.alive = True

    def update(self, *args):
        # Gravity
        gravity = self.g * self.mass
        self.applyForce(gravity)
        # Friction
        friction = -.01 * self.vel.normalize()
        self.applyForce(friction)

        self.move()
        self.alpha -= .01

        if self.alpha <= 0:
            self.alive = False
            # Stop animation
            return False


    def applyForce(self, force):
        self.acc += force / self.mass


    def move(self):
        self.vel += self.acc
        self.vel.limit(10)
        self.pos = PVector(self.pos) + self.vel
        self.acc *= 0
        # Rotate two degrees further in the initial direction
        self.rot += float(np.sign(self.rot)*3)


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
        self.ps = deque()
        Clock.schedule_interval(self.cleanUp, 5)

    def update(self, dt):
        friction = self.vel.normalize() * -0.2
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

    def applyRotation(self, lateralForce):
        newHeading = self.heading + lateralForce
        self.angle += newHeading.angle(self.heading)
        self.heading = newHeading.normalize()

    def move(self):
        self.vel += self.acc
        self.vel.limit(30)
        self.pos = PVector(self.pos) + self.vel
        self.acc *= 0

    def particlePropulsion(self):
        particle = Particle(pos=self.center, vel=-self.vel)
        self.add_widget(particle)
        self.ps.append(particle)
        Clock.schedule_interval(particle.update, .05)


    def cleanUp(self, *args):

        if not self.ps:
            print("No more particles to clean!")
            return

        dead_p = []
        for p in self.ps:
            if not p.alive:
                self.remove_widget(p)
                dead_p.append(p)

        # remove any died particle
        if dead_p:
            for p in dead_p:
                self.ps.remove(p)
            print(len(dead_p), "dead particles removed!")


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
        # Key z
        if key == 122:
            self.car.applyForce(-self.car.heading)
            self.car.particlePropulsion()
        # Key Down
        elif key == 274:
            pass #self.car.applyForce(-self.car.heading)
        # Key Left
        elif key == 276:
            lateralForce = self.car.heading.rotate(90) * 0.1
            self.car.applyForce(lateralForce)
            self.car.applyRotation(lateralForce)
        # Key Right
        elif key == 275:
            lateralForce = self.car.heading.rotate(-90) * 0.1
            self.car.applyForce(lateralForce)
            self.car.applyRotation(lateralForce)


class NatureApp(App):

    def build(self):
        return Universe()



if __name__ == "__main__":
    NatureApp().run()
