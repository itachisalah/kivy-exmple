"""
Use an L-system as a set of instructions for creating objects stored in an ArrayList.
Use trigonometry and vector math to perform the rotations instead of matrix transformations
(much like we did in the Koch curve example).
"""

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.graphics import Line, Ellipse, Color
from kivy.core.window import Window

from lib.pvector import PVector


class Branch(Widget):

    def __init__(self, start, length, angle, **kwargs):
        super(Branch, self).__init__(**kwargs)
        self.start = start
        self.end = start + PVector(0, length).rotate(angle)
        with self.canvas:
            Line(points=(self.start.x, self.start.y,
                         self.end.x, self.end.y))


class Universe(Widget):

    def __init__(self, **kwargs):
        super(Universe, self).__init__(**kwargs)
        self.sentence = "F"
        self.length = 6
        self.theta = 0
        self.endpoint = PVector(Window.width / 2, 0)
        self.tempPos = []
        self.tempDeg = []
        self.draw()

    def makeSentence(self):
        self.sentence = self.sentence.replace("F", "FF+[+F-F-F]-[-F+F+F]")

    def draw(self):
        for command in self.sentence:
            if command == "F":
                branch = Branch(self.endpoint, self.length, self.theta)
                self.add_widget(branch)
                self.endpoint = branch.end.get()

            elif command == "+":
                self.theta += 20

            elif command == "-":
                self.theta -= 20

            elif command == "[":
                self.tempPos.append(self.endpoint)
                self.tempDeg.append(self.theta)

            elif command == "]":
                self.endpoint = self.tempPos.pop()
                self.theta = self.tempDeg.pop()

    def on_touch_down(self, touch):
        self.makeSentence()
        self.draw()


class NatureApp(App):
    def build(self):
        return Universe()


if __name__ == "__main__":
    NatureApp().run()