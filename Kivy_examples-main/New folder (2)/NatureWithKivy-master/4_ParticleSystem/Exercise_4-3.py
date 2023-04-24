"""
Make the origin point move dynamically. Have the particles emit from the mouse location or use the concepts of velocity
and acceleration to make the system move autonomously.
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
    g = PVector(0, -0.4)
    # Opacity of the particle
    alpha = NumericProperty(1)
    rot = NumericProperty(random()*2 - 1)

    def __init__(self, **kwargs):
        super(Particle, self).__init__(**kwargs)
        self.size = 20, 20
        self.mass = 1
        self.vel = PVector(0, 0)
        self.acc = PVector(randint(-3, 3), randint(-3, 3))

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
            return False # Unschedule Clock

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
        # Rotate two degrees further in the initial direction
        self.rot += float(np.sign(self.rot)*3)


class ParticleSystem(Widget):

    def __init__(self, **kwargs):
        super(ParticleSystem, self).__init__(**kwargs)
        Clock.schedule_interval(self.run, .05)


    def run(self, *args):
        particle = Particle(pos=self.pos)
        self.add_widget(particle)
        Clock.schedule_interval(particle.update, .05)

        # The cleanUp func will be called every time the property "alpha" changes
        particle.bind(alpha=self.cleanUp)

    def cleanUp(self, instance, alpha):
        if alpha <= 0:
            # Remove widget when the color is completely faded out
            self.remove_widget(instance)


class Universe(Widget):

    def __init__(self, **kwargs):
        super(Universe, self).__init__(**kwargs)

    def on_touch_down(self, touch):
        ps = ParticleSystem(pos=touch.pos)
        self.add_widget(ps)


class NatureApp(App):

    def build(self):
        return Universe()



if __name__ == "__main__":
    NatureApp().run()
