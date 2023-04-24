"""
Using forces, simulate a helium-filled balloon floating upward and bouncing off
the top of a window. Can you add a wind force that changes over time, perhaps
according to Perlin noise?
"""

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import ListProperty

from random import randint
from noise import pnoise1
from lib.pvector import PVector


class Ball(Widget):

    color = ListProperty([0,0,0,0])
    # Wind strength is the same for every ball
    tx = randint(0, 10000)

    def __init__(self, **kwargs):
        super(Ball, self).__init__(**kwargs)
        self.vel = PVector(0, 0)
        self.acc = PVector(0, 0)
        self.color = [1,1,1,.7]

    def update(self, dt):
        # Generate and apply force
        gravity = PVector(0, .1)
        wind = PVector(pnoise1(self.tx), 0) * .2
        self.applyForce(gravity)
        self.applyForce(wind)

        self.checkEdge()
        self.move()

        self.tx += .01

    def checkEdge(self):
        # check horizontal border
        if self.x + self.size[0] > Window.width:
            self.vel.x *= -1
            self.x = Window.width - self.size[0]
        elif self.x < 0:
            self.vel.x *= -1
            self.x = 0

        # check vertical border
        if self.y + self.size[1] > Window.height:
            self.vel.y *= -1
            self.y = Window.height - self.size[1]
        elif self.y < 0:
            self.vel.y *= -1
            self.y = 0

    def applyForce(self, force):
        self.acc += force

    def move(self):
        self.vel += self.acc
        self.vel.limit(10)
        self.pos = PVector(self.pos) + self.vel
        self.acc *= 0


class Universe(FloatLayout):

    def __init__(self, **kwargs):
        super(Universe, self).__init__(**kwargs)
        for _ in range(5):
            self.add_child()

    def add_child(self):
        pos_x = randint(0, Window.width)
        pos_y = randint(0, Window.height)
        b = Ball(pos = (pos_x, pos_y))

        self.add_widget(b)
        Clock.schedule_interval(b.update, .01)


class NatureApp(App):

    def build(self):
        return Universe()


if __name__ == "__main__":
    NatureApp().run()
