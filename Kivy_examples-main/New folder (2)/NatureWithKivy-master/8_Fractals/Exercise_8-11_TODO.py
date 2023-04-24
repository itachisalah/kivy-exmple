"""
Set the angles of the branches of the tree according to Perlin noise values.
Adjust the noise values over time to animate the tree. See if you can get it to appear as if it is blowing in the wind.
"""

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.graphics import Line, Ellipse, Color
from kivy.core.window import Window
from kivy.properties import ListProperty, ObjectProperty
from kivy.clock import Clock

from lib.pvector import PVector
from numpy.random import normal, random, randint
from noise import pnoise1


class Branch(Widget):

    def __init__(self, start, end, thickness, upperBranch, **kwargs):
        super(Branch, self).__init__(**kwargs)
        self.start = start
        self.end = end
        self.thickness = thickness
        self.display()
        self.upperBranch = upperBranch
        self.ty = randint(10000)
        self.growLeaves()
        Clock.schedule_interval(self.update, .05)


    def getStart(self):
        return self.start.get()

    def getEnd(self):
        return self.end.get()

    def getGrowV(self):
        return self.end - self.start

    def display(self):
        with self.canvas:
            Color(1, 1, 1)
            self.line = Line(points=(self.start.x, self.start.y,
                                     self.end.x, self.end.y),
                             width=self.thickness)

    def growLeaves(self):
        self.leaves = []
        growV = self.getGrowV()
        growPorb = 70 / growV.length()
        numLeaves = abs(int(normal(growPorb, scale=2)))
        with self.canvas:
            Color(0, random(), 0, .7)
            for _ in range(numLeaves):
                self.leaves.append(Ellipse(size=(5, 10),
                                           pos=self.start + normal(growV, 2) * random(),
                                           scale=2))

    def update(self, *args):
        angle = pnoise1(self.ty)
        growV = self.getGrowV().rotate(angle)
        old_loc = self.start
        if self.upperBranch is not None:
            self.start = self.upperBranch.getEnd()
        self.end = self.start + growV
        self.line.points = (self.start.x, self.start.y, self.end.x, self.end.y)

        for leaf in self.leaves:
            leaf.pos = PVector(leaf.pos) - old_loc + self.start

        self.ty += .04


class Universe(Widget):

    tx = randint(10000)

    def __init__(self, **kwargs):
        super(Universe, self).__init__(**kwargs)
        self.branches = list()
        self.plantTree()
        for _ in range(9):
            self.grow()

    def plantTree(self):
        trunk = Branch(start=PVector(Window.width / 2, 0),
                       end=PVector(Window.width / 2, 100),
                       thickness=6,
                       upperBranch=None)
        self.branches.append(trunk)
        self.add_widget(trunk)
        self.trunk = trunk

    def grow(self):
        newBranches = list()
        for branch in self.branches:

            start = branch.getStart()
            end = branch.getEnd()
            growV = (end - start) * .8
            thickness = branch.thickness * .75

            # Left branch
            lB = Branch(start=end, end=end+growV.rotate(20),
                        thickness=thickness, upperBranch=branch)
            # Right branch
            rB = Branch(start=end, end=end+growV.rotate(-20),
                        thickness=thickness, upperBranch=branch)

            newBranches.extend([lB, rB])

        # Fill the list with the newest branches only
        self.branches = newBranches

        for nb in newBranches:
            self.add_widget(nb)


class NatureApp(App):
    def build(self):
        return Universe()


if __name__ == "__main__":
    NatureApp().run()