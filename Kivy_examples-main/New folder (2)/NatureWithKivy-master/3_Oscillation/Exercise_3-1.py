"""
Rotate a baton-like object (see below) around its center using translate() and
rotate().
"""

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.properties import ListProperty, NumericProperty
from kivy.graphics import *


class Baton(Widget):

    rot = NumericProperty()

    def __init__(self, **kwargs):
        super(Baton, self).__init__(**kwargs)

    def update(self, dt):
        self.rot -= 2


class Universe(Widget):

    def __init__(self, **kwargs):
        super(Universe, self).__init__(**kwargs)

        b = Baton(center=Window.center)
        self.add_widget(b)

        Clock.schedule_interval(b.update, 1/60)


class NatureApp(App):

    def build(self):
        return Universe()



if __name__ == "__main__":
    NatureApp().run()
