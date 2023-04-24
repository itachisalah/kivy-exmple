"""
Using drawCircle() and the Cantor set as models, generate your own pattern with recursion.
Here is a screenshot of one that uses lines.
"""

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.graphics import Line
from kivy.core.window import Window
from lib.pvector import PVector


class Universe(Widget):

    def __init__(self, **kwargs):
        super(Universe, self).__init__(**kwargs)
        self.cantor(pos=PVector(Window.width/2, 50), dir=PVector(0, 20), thickness=10)

    def cantor(self, pos, dir, thickness):
        if dir.length() < 150:
            with self.canvas:
                Line(circle=(pos.x, pos.y, dir.length()))
                Line(points=(pos.x, pos.y, (pos+dir).x, (pos+dir).y), width=thickness)

            self.cantor(pos+dir, dir.rotate(-20) * 1.3, thickness*.6)
            self.cantor(pos+dir, dir.rotate( 20) * 1.3, thickness*.6)


class NatureApp(App):
    def build(self):
        return Universe()


if __name__ == "__main__":
    NatureApp().run()