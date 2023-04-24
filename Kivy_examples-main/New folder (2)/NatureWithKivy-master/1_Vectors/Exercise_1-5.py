'''
Exercise 1-5
Create a simulation of a car (or runner) that accelerates when you press the
up key and brakes when you press the down key.
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
        self.vel += self.acc
        self.vel.limit(100)
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

    def __init__(self, **kwargs):
        super(BouncingWorld, self).__init__(**kwargs)
        Window.bind(on_key_down=self._keydown)

    def update(self, dt):
        self.myBall.checkEdge()
        self.myBall.move()

    def _keydown(self, instance, key, *args):
        '''Keycode ref
        https://github.com/kivy/kivy/blob/master/kivy/core/window/__init__.py
        '''
        # Key Up
        if key == 273:
            self.myBall.acc -= PVector(.01,0)
            print("Vel", self.myBall.vel, "Acc", self.myBall.acc)
        # Key Down
        if key == 274:
            self.myBall.acc += PVector(.01,0)
            print("Vel", self.myBall.vel, "Acc", self.myBall.acc)


class BallApp(App):

    def build(self):
        w = BouncingWorld()
        Clock.schedule_interval(w.update, .01)
        return w


if __name__ == "__main__":
    BallApp().run()
