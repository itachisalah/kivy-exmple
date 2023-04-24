"""
Step 1: Create a simulation where objects are shot out of a cannon. Each object
should experience a sudden force when shot (just once) as well as gravity
(always present).
Step 2: Add rotation to the object to model its spin as it is shot from the
cannon. How realistic can you make it look?
"""

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.properties import ListProperty, NumericProperty, ObjectProperty
from kivy.graphics import *

from lib.pvector import PVector
from random import randint

class Ball(Widget):

    # Gravity
    g = PVector(0, -0.1)

    rotation = NumericProperty()

    def __init__(self, **kwargs):
        super(Ball, self).__init__(**kwargs)
        self.pos = (25, 20)
        self.size = (30, 30)
        self.mass = 1
        self.vel = PVector(0, 0)
        self.acc = PVector(0, 0)
        self.aVel = 0
        self.aAcc = 0
        # whether ball is out of sight
        self.out = False

    def update(self, dt):
        gravity = self.g * self.mass
        airResistance = -self.vel.normalize() * 0.01

        self.applyForce(gravity)
        self.applyForce(airResistance)

        self.checkEdge()
        self.move()

        if self.out == True:
            # Cancel schedule
            return False

    def checkEdge(self):
        # check horizontal border
        if self.x > Window.width:
            self.out = True
        elif self.x < 0:
            self.vel.x *= -1
            self.x = 0

        # check vertical border
        if self.y > Window.height:
            # Nothing happen here
            pass
        elif self.y < 0:
            self.vel.y *= -1
            self.y = 0

    def applyForce(self, force):
        acc = force / self.mass
        self.acc += acc

    def applyRotation(self, rotation):
        self.aAcc += rotation

    def move(self):
        self.vel += self.acc
        self.vel.limit(10)
        self.pos = PVector(self.pos) + self.vel
        self.acc *= 0

        self.aVel += self.aAcc
        self.rotation += self.aVel
        self.aAcc *= 0

class Canon(Widget):

    rotation = NumericProperty()

    def __init__(self, **kwargs):
        super(Canon, self).__init__(**kwargs)
        self.rotation = 0
        self.loaded = []

    def lockAndLoad(self):
        ball = Ball()
        self.add_widget(ball)
        self.loaded.append(ball)

    def fire(self):
        # Force = direction * magnitude
        explosion = PVector(1,0).rotate(self.rotation) * 100
        rotation = randint(-10, -3)
        ball = self.loaded[0]
        ball.applyForce(explosion)
        ball.applyRotation(rotation)
        # Animation
        Clock.schedule_interval(ball.update, 1/60)
        Clock.schedule_interval(self.cleanUp, .5)
        self.loaded.pop(0)

    def cleanUp(self, dt):
        for child in self.children[:]:
            if child.out:
                print("The ball is out of sight!")
                self.remove_widget(child)
                return False
            else:
                print("The ball is still not out of sight!")
                return True

class BattleField(Widget):

    canon = ObjectProperty()

    def __init__(self, **kwargs):
        super(BattleField, self).__init__(**kwargs)
        Window.bind(on_key_down=self._keydown)
        self.add_widget(Canon())

    def _keydown(self, instance, key, *args):
        '''Keycode ref
        https://github.com/kivy/kivy/blob/master/kivy/core/window/__init__.py
        '''
        # Key Up
        if key == 273:
            self.canon.rotation += 3
        # Key Down
        elif key == 274:
            self.canon.rotation -= 3
        # "l" for load
        elif key == 108:
            self.canon.lockAndLoad()
        # Space Bar
        elif key == 32 and self.canon.loaded:
            self.canon.fire()


class NatureApp(App):

    def build(self):
        return BattleField()



if __name__ == "__main__":
    NatureApp().run()
