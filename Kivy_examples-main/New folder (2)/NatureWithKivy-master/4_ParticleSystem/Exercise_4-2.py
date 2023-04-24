"""
1. Rewrite the example so that the particle can respond to force vectors via an applyForce() function.
2. Add angular velocity (rotation) to the particle. Create your own non-circle particle design.

TODO: Particle can fall straight down, but with rotation to the left or right
"""

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.properties import ListProperty, NumericProperty

from lib.pvector import PVector
from random import randint, random
import numpy as np

class Particle(Widget):

    # Gravity
    g = PVector(0, -0.1)
    # Opacity of the particle
    alpha = NumericProperty(1)
    rot = NumericProperty(random()*2 - 1)

    def __init__(self, **kwargs):
        super(Particle, self).__init__(**kwargs)
        self.size = 20, 20
        self.pos = Window.center
        self.mass = 1
        self.vel = PVector(0, 0)
        self.acc = PVector(randint(-1, 1), 1)
        self.alive = True

    def update(self, *args):

        # Gravity
        gravity = self.g * self.mass
        self.applyForce(gravity)
        # Friction
        friction = -.01 * self.vel.normalize()
        self.applyForce(friction)

        self.checkEdge()
        self.move()
        self.alpha -= .01

        if self.alpha <= 0:
            self.alive = False
            print("Particle is dead!")
            # Stop animation
            return False

    def applyForce(self, force):
        self.acc += force / self.mass


    def checkEdge(self):
        if self.y < 0:
            self.vel.y *= -1
            self.y = 0


    def move(self):
        self.vel += self.acc
        self.vel.limit(10)
        self.pos = PVector(self.pos) + self.vel
        self.acc *= 0
        self.rot += float(np.sign(self.rot))


class Universe(Widget):

    def __init__(self, **kwargs):
        super(Universe, self).__init__(**kwargs)
        self.ps = {}

        self.add_particle(1)

    def add_particle(self, val):

        for _ in range(val):
            p = Particle()
            self.add_widget(p)
            self.ps[p] = Clock.schedule_interval(p.update, .05)



class NatureApp(App):

    def build(self):
        return Universe()



if __name__ == "__main__":
    NatureApp().run()
