"""
Add the separation force to path following to create a simulation of Reynolds’s “Crowd Path Following.”

TODO: The following behavior does not really work
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
    maxForce = 0.2
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
        self.follow()
        #self.separate()
        self.applyRotation()
        self.checkEdge()
        self.move()

    def separate(self):
        sum = PVector(0,0)
        count = 0

        for neighbor in self.neighbors:
            if neighbor != self:
                diff = PVector(self.pos)- neighbor.pos
                dist = diff.length()
                if dist < self.desiredSeparation:
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
        """TODO: Try break down and simply the behavior so that it's easier to debug"""
        # Predict future location
        predict = self.vel.get()
        predict = predict.normalize() * 25
        predictLoc = predict + self.pos

        # Screen through possible normal points
        worldRecord = 1000000
        for i in range(len(self.path.pList)-1):

            begin = PVector(self.path.pList[i])
            end = PVector(self.path.pList[i+1])
            # Get normal point on the path
            normalPoint = self.getNormalPoint(predictLoc, begin, end)
            dir = end - begin
            # If the normal point is not on the line itself
            if normalPoint.x < min(begin.x, begin.x) or normalPoint.x > max(end.x, end.x) \
                    or normalPoint.y < min(begin.y, begin.y) or normalPoint.y > max(end.y, end.y):
                normalPoint = end.get()
                listLength = len(self.path.pList)
                begin = PVector(self.path.pList[(i+1)%listLength])
                end = PVector(self.path.pList[(i+2)%listLength])
                dir = end - begin

            # Find the closest normal point
            distToLine = predictLoc.distance(normalPoint)
            if distToLine < worldRecord:
                worldRecord = distToLine
                self.target = normalPoint.get()
                # Find and define the target (25 px further on the path)
                direction = dir.normalize() * 25
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
            Line(points=self.pList, width=self.radius, close=True)
        with self.canvas.after:
            Color(0,0,0,1)
            Line(points=self.pList, width=2, close=True)


    def makePoints(self):

        # Need 3 or more points to close a line
        assert(self.pointNum >= 3)

        """ Make the points manually this time
        for _ in range(self.pointNum):
            x, y = randomPos()
            self.pList.extend([x, y])
        """
        self.pList = [PVector(100, 100), PVector(100, 500), PVector(700, 500), PVector(700, 100), PVector(400, 300)]

def randomPos(width=Window.width, height=Window.height):
    w, h = width, height
    return randint(0, w), randint(0, h)


class Universe(Widget):

    def __init__(self, *args, **kwargs):
        super(Universe, self).__init__(*args, **kwargs)
        self.path = Path(4)
        self.add_widget(self.path)
        self.add_child(1)

    def add_child(self, val):
        self.boids = list()
        for _ in range(val):
            pos_x, pos_y = randomPos()

            b = Boid(path=self.path, pos=(pos_x, pos_y))
            self.boids.append(b)
            self.add_widget(b)

        for child in self.boids:
            child.neighbors = self.boids
            Clock.schedule_interval(child.update, 1/60)




class NatureApp(App):
    def build(self):
        return Universe()


if __name__ == "__main__":
    NatureApp().run()
