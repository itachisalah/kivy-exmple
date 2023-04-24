"""
Create a sketch that displays the angle between two PVector objects.
"""

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.graphics import *
from kivy.properties import NumericProperty
from lib.pvector import PVector
from random import uniform, random
import numpy as np


class Arrow(Widget):

    angle = NumericProperty()

    def __init__(self, *args, **kwargs):
        super(Arrow, self).__init__(*args, **kwargs)
        self.pos = Window.center

    def update(self, dt):
        to_mouse = PVector(Window.mouse_pos) - self.pos
        self.angle = to_mouse.angle((0, 1))


class Universe(Widget):

    def __init__(self, *args, **kwargs):
        super(Universe, self).__init__(*args, **kwargs)
        a = Arrow()
        self.add_widget(a)
        Clock.schedule_interval(a.update, .05)

        with self.canvas:
            x, y = Window.center
            Color(1,1,1,.7)
            Line(points=(x, y, x, y+100), width = 2)



class NatureApp(App):
    def build(self):
        return Universe()


if __name__ == "__main__":
    NatureApp().run()
