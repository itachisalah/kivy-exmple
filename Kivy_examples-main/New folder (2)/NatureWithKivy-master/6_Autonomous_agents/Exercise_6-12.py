"""
Rewrite separate() to work in the opposite fashion (“cohesion”). If a vehicle is beyond a certain distance, steer
towards that vehicle. This will keep the group together. (Note that in a moment, we’re going to look at what happens
when we have both cohesion and separation in the same simulation.)
"""

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.graphics import *
from kivy.properties import NumericProperty, ListProperty
from lib.pvector import PVector
from random import randint
import numpy as np


class Boid(Widget):

    angle = NumericProperty()
    target = ListProperty([0,0])
    maxForce = 0.5
    maxSpeed = 4
    desiredSeparation = 30

    def __init__(self, neighbors=None, path=None, *args, **kwargs):
        super(Boid, self).__init__(*args, **kwargs)
        self.size = 20, 20
        self.heading = PVector(0, 1)
        self.mass = 1
        self.vel = PVector(randint(-2, 2), randint(-2, 2))
        self.acc = PVector(0, 0)
        self.path = path
        self.neighbors = neighbors


    def update(self, dt):
        self.separate()
        self.applyRotation()
        self.checkEdge()
        self.move()

    def separate(self):
        sum = PVector(0,0)
        count = 0

        for neighbor in self.neighbors:
            if neighbor != self:
                diff = PVector(neighbor.pos)- self.pos
                dist = diff.length()
                if dist > self.desiredSeparation:
                    diff.normalize()
                    diff /= dist
                    sum += diff
                    count += 1

        if count > 0:
            sum /= count
            sum.normalize()
            sum *= self.maxSpeed

            steeringForce = sum - self.vel
            steeringForce.limit(self.maxForce)

            self.applyForce(steeringForce)

    def follow(self):
        # Predict future location
        predict = self.vel.get()
        predict = predict.normalize() * 25
        predictLoc = predict + self.pos

        # Screen through possible normal points
        worldRecord = 1000000
        currentPath = PVector(0,0)
        for i in range(0, len(self.path.pList)-2, 2):
            begin = PVector(self.path.pList[i:i+2])
            end = PVector(self.path.pList[i+2:i+4])
            # Get normal point on the path
            normalPoint = self.getNormalPoint(predictLoc, begin, end)

            # Not sure about this...
            if (normalPoint.x < min(begin.x, begin.x)) or (normalPoint.x > max(end.x, end.x)):
                normalPoint = end.get()
            if (normalPoint.y < min(begin.y, begin.y)) or (normalPoint.y > max(end.y, end.y)):
                normalPoint = end.get()

            # Find the closest normal point
            distToLine = predictLoc.distance(normalPoint)
            if distToLine < worldRecord:
                worldRecord = distToLine
                self.target = normalPoint#.get()
                currentPath = end - begin

        # Find and define the target (10 px further on the path)
        direction = currentPath.normalize() * 10
        self.target = direction + self.target

        if (predictLoc.distance(self.target) > self.path.radius):
            self.seek()


    def getNormalPoint(self, predictLoc, begin, end):
        toPosition = predictLoc - begin # Vector
        lineVector = end - begin

        lineVector.normalize()
        # Find the normal points projected on the line vector
        lineVector *= toPosition.dot(lineVector)

        return begin + lineVector


    def seek(self):
        desired_vel = PVector(self.target) - self.pos
        desired_vel.limit(self.maxSpeed)

        steeringForce = desired_vel - self.vel
        steeringForce.limit(self.maxForce)

        self.applyForce(steeringForce)


    def checkEdge(self):
        # check horizontal border
        if self.center_x > Window.width:
            self.center_x = 0
        elif self.center_x <= 0:
            self.center_x = Window.width

        # check vertical border
        if self.center_y > Window.height:
            self.center_y = 0
        elif self.center_y <= 0:
            self.center_y = Window.height


    def applyForce(self, force):
        acc = force / self.mass
        self.acc += acc


    def applyRotation(self):
        self.angle = self.vel.angle(self.heading)


    def move(self):
        self.vel += self.acc
        self.vel.limit(self.maxSpeed)
        self.pos = self.vel + self.pos
        self.acc *= 0


class Path(Widget):

    def __init__(self, pointNum, *args, **kwargs):
        super(Path, self).__init__(*args, **kwargs)
        self.start = PVector(0, Window.height/3)
        self.end = PVector(Window.width, 2*Window.height/3)
        self.radius = 20
        self.pointNum = pointNum
        self.makePoints()

        with self.canvas.before:
            Color(1,1,1,.9)
            Line(points=self.pList, width=self.radius)
        with self.canvas.after:
            Color(0,0,0,1)
            Line(points=self.pList, width=2)


    def makePoints(self):
        # Leftmost point
        self.pList = [0, randint(0, Window.height)]

        for _ in range(self.pointNum):
            x, y = randomPos()
            self.pList.extend([x, y])

        # Rightmost point
        self.pList.extend([Window.width, randint(0, Window.height)])


def randomPos(width=Window.width, height=Window.height):
    w, h = width, height
    return randint(0, w), randint(0, h)


class Universe(Widget):

    def __init__(self, *args, **kwargs):
        super(Universe, self).__init__(*args, **kwargs)
        self.add_child(50)

    def add_child(self, val):
        for _ in range(val):
            pos_x, pos_y = randomPos()

            b = Boid(pos=(pos_x, pos_y))
            self.add_widget(b)

        for child in self.children:
            child.neighbors = self.children
            Clock.schedule_interval(child.update, 1/60)




class NatureApp(App):
    def build(self):
        return Universe()


if __name__ == "__main__":
    NatureApp().run()
