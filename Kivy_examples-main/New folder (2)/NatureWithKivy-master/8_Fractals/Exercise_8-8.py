"""
The tree structure can also be generated using the ArrayList technique demonstrated with the Koch curve.
Recreate the tree using a Branch object and an ArrayList to keep track of the branches.
Hint: you’ll want to keep track of the branch directions and lengths using vector math instead of Processing transformations.
"""

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.graphics import Line
from kivy.graphics.context_instructions \
    import PushMatrix, PopMatrix, Rotate, Translate
from kivy.core.window import Window
from lib.pvector import PVector


class Branch(Widget):

    def __init__(self, start, end, thickness, **kwargs):
        super(Branch, self).__init__(**kwargs)
        self.start = start
        self.end = end
        self.thickness = thickness
        with self.canvas:
            self.line = Line(points=(self.start.x, self.start.y,
                                     self.end.x, self.end.y),
                             width=self.thickness)

    def getStart(self):
        return self.start.get()

    def getEnd(self):
        return self.end.get()

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