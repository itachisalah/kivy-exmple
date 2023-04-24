"""
Exercise 1.1
Find something you’ve previously made in Processing using separate x and y
variables and use PVectors instead.
"""

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.vector import Vector
from kivy.clock import Clock
from kivy.properties import ObjectProperty, NumericProperty, ReferenceListProperty
from kivy.core.window import Window


class Ball(Widget):

    vel_x = NumericProperty(3)
    vel_y = NumericProperty(3)
    vel = ReferenceListProperty(vel_x, vel_y)

    def move(self):
        self.pos = Vector(self.vel) + self.pos


class BouncingWorld(Widget):

    myBall = ObjectProperty()

    def update(self, dt):

        # Define behavior at the borders (size: 50, 50)
        if self.myBall.x < 0 or self.myBall.x + 50 > Window.width:
            self.myBall.vel_x *= -1

        if self.myBall.y < 0 or self.myBall.y + 50 > Window.height:
            self.myBall.vel_y *= -1

        self.myBall.move()


class BallApp(App):

    def build(self):
        world = BouncingWorld()
        Clock.schedule_interval(world.update, 1/60)
        return world


if __name__ == "__main__":
    BallApp().run()
