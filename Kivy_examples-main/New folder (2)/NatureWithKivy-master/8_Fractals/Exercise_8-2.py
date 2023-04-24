"""
Draw the Koch snowflake (or some other variation of the Koch curve).
"""

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.graphics import Line
from kivy.core.window import Window
from lib.pvector import PVector


class KochLine(Widget):

    def __init__(self, start, end, **kwargs):
        super(KochLine, self).__init__(**kwargs)
        self.a = start
        self.e = end
        self.display()

    def display(self):
        with self.canvas:
            Line(points=(self.a.x, self.a.y, self.e.x, self.e.y))

    def getA(self):
        return self.a.get()

    def getB(self):
        v = self.e - self.a
        v /= 3
        return self.a + v

    def getC(self):
        b = self.getB()
        d = self.getD()
        v = d - b
        return b + v.rotate(60)

    def getD(self):
        v = self.e - self.a
        v = v * 2 / 3
        return self.a + v

    def getE(self):
        return self.e.get()

    def rotateStart(self, angle):
        v = self.e - self.a
        v = self.a + v.rotate(angle)
        return KochLine(v, self.a)

    def rotateEnd(self, angle):
        v = self.a - self.e
        v = self.e + v.rotate(angle)
        return KochLine(self.e, v)


class Universe(Widget):

    def __init__(self, **kwargs):
        super(Universe, self).__init__(**kwargs)
        self.makeShape()

        # Make sure you don't generate too many widget!
        for _ in range(5):
            self.generate()

        print(len(self.children))  # 3072 widgets with 5 generation!

    def makeShape(self):
        bottomLine = KochLine(start=PVector(Window.width-200, 200), end=PVector(200, 200))
        leftLine = bottomLine.rotateStart(-60)
        rightLine = bottomLine.rotateEnd( 60)
        self.lines= [bottomLine, leftLine, rightLine]

        for line in self.lines:
            self.add_widget(line)

    def generate(self):
        nextGen = list()

        for line in self.lines:
            a = line.getA()
            b = line.getB()
            c = line.getC()
            d = line.getD()
            e = line.getE()

            nextGen.append(KochLine(a, b))
            nextGen.append(KochLine(b, c))
            nextGen.append(KochLine(c, d))
            nextGen.append(KochLine(d, e))

        for line in self.lines:
            self.remove_widget(line)

        for newLine in nextGen:
            self.add_widget(newLine)

        self.lines = nextGen


class NatureApp(App):
    def build(self):
        return Universe()


if __name__ == "__main__":
    NatureApp().run()