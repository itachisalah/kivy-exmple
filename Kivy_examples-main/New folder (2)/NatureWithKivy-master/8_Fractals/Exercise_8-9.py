"""
Once you have the tree built with an ArrayList of Branch objects, animate the tree’s growth.
Can you draw leaves at the end of the branches?
"""

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.graphics import Line, Ellipse, Color
from kivy.core.window import Window
from lib.pvector import PVector
from numpy.random import normal, random


class Branch(Widget):

    def __init__(self, start, end, thickness, **kwargs):
        super(Branch, self).__init__(**kwargs)
        self.start = start
        self.end = end
        self.thickness = thickness
        self.display()
        self.growLeaves()

    def getStart(self):
        return self.start.get()

    def getEnd(self):
        return self.end.get()

    def getGrowV(self):
        return self.end - self.start

    def display(self):
        with self.canvas:
            Color(1, 1, 1)
            Line(points=(self.start.x, self.start.y,
                         self.end.x, self.end.y),
                 width=self.thickness)

    def growLeaves(self):
        growV = self.getGrowV()
        growPorb = 70 / growV.length()
        numLeaves = abs(int(normal(growPorb, scale=2)))
        with self.canvas:
            Color(0, random(), 0, .7)
            for _ in range(numLeaves):
                Ellipse(size=(5, 10),
                        pos=self.start + normal(growV, 2) * random(),
                        scale=2)


class Universe(Widget):

    def __init__(self, **kwargs):
        super(Universe, self).__init__(**kwargs)
        self.theta = 20
        self.branches = list()
        self.plantTree()

    def plantTree(self):
        trunk = Branch(start=PVector(Window.width / 2, 0),
                       end=PVector(Window.width / 2, 100),
                       thickness=6)
        self.branches.append(trunk)
        self.add_widget(trunk)

    def grow(self):
        newBranches = list()
        for branch in self.branches:

            start = branch.getStart()
            end = branch.getEnd()
            growV = (end - start) * .8
            thickness = branch.thickness

            thickness *= .75
            # Left branch
            lB = Branch(start=end, end=end+growV.rotate(30), thickness=thickness)
            # Right branch
            rB = Branch(start=end, end=end+growV.rotate(-30), thickness=thickness)

            newBranches.extend([lB, rB])

        # Fill the list with the newest branches only
        self.branches = newBranches

        for nb in newBranches:
            self.add_widget(nb)

    def on_touch_down(self, touch):
        self.grow()


class NatureApp(App):
    def build(self):
        return Universe()


if __name__ == "__main__":
    NatureApp().run()