'''
Exercise 1-6
Referring back to the Introduction, implement acceleration according to
Perlin noise.
'''
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.vector import Vector
from kivy.clock import Clock
from kivy.properties import ObjectProperty
from noise import pnoise1
from random import randint
from lib.pvector import PVector


class Ball(Widget):

    vel = PVector(2, 0)
    acc = PVector(0, 0)

    tx = randint(1, 10000)
    ty = randint(1, 10000)

    def move(self):
        self.acc = PVector(pnoise1(self.tx), pnoise1(self.ty))

        self.vel += self.acc
        self.vel.limit(10)
        self.pos = PVector(self.pos) + self.vel

        self.tx += 0.01
        self.ty += 0.01

    def checkEdge(self):
        # check horizontal border
        if self.x > Window.width:
            self.x = 0
        elif self.x < 0:
            self.x = Window.width

        # check vertical border
        if self.y > Window.height:
            self.y = 0
        elif self.y < 0:
            self.y = Window.height


class BouncingWorld(Widget):

    myBall = ObjectProperty()

    def update(self, dt):
        self.myBall.checkEdge()
        self.myBall.move()


class BallApp(App):

    def build(self):
        w = BouncingWorld()
        Clock.schedule_interval(w.update, .01)
        return w


if __name__ == "__main__":
    BallApp().run()
