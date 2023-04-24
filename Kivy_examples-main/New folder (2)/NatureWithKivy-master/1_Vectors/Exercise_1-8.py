'''
Exercise 1-8
Try implementing the above example with a variable magnitude of acceleration,
stronger when it is either closer or farther away.
'''
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.vector import Vector
from kivy.clock import Clock
from kivy.properties import ObjectProperty
from lib.pvector import PVector


class Ball(Widget):

    vel = PVector(2, 0)
    acc = PVector(0, 0)

    def move(self):
        # Calculate the direction from mouse to ball
        dir = PVector(Window.mouse_pos) - self.pos
        # Acceleration gets stronger when it's close
        self.acc = dir.normalize() / dir.length() * 2

        self.vel += self.acc
        self.vel.limit(10)
        self.pos = PVector(self.pos) + self.vel

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
