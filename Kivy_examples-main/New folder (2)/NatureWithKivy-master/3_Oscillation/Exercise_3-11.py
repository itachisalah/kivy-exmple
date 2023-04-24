"""
More complex waves can be produced by the values of multiple waves together.
Create a sketch that implements this, as in the screenshot below.
"""

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.properties import ListProperty, NumericProperty, ObjectProperty
from kivy.graphics import *

from lib.pvector import PVector
from random import randint, uniform
from math import sin, cos, pi
from noise import pnoise1
import numpy as np
from functools import partial


class Oscillator(Widget):

    def __init__(self, loc, angle, **kwargs):
        super(Oscillator, self).__init__(**kwargs)
        self.size = (20, 20)
        self.pos = loc, 0
        self.angle = angle


class Wave(Widget):

    def __init__(self, step, amp=100, vel=.1, loc=0, num=20, **kwargs):
        super(Wave, self).__init__(**kwargs)
        self.amp = amp
        self.vel = vel
        self.loc = loc
        self.num = num
        self.oscillators = self.makeOscillators(step)

    def makeOscillators(self, step):
        # location of pos x
        xMin, xMax = self.loc-250, self.loc+250
        locs = np.linspace(xMin, xMax, self.num).tolist()
        angle = 0

        oscillators = []
        for loc in locs:
            osci = Oscillator(loc, angle)
            oscillators.append(osci)
            self.add_widget(osci)
            # phase between two oscillators
            angle += step

        return oscillators

    def update(self, *largs):
        for oscillator in self.oscillators:
            oscillator.y = self.amp * sin(oscillator.angle)
            oscillator.angle += self.vel

    @staticmethod
    def update_mixWave(newWave, instances, *largs):

        # Update the position of its own oscillators
        for i, oscilator in enumerate(newWave.oscillators):
            ys = 0
            # from the other oscillators
            for ins in instances:
                ys += ins.oscillators[i].y

            oscilator.y = ys

        # Update next frame
        for ins in instances:
            ins.update()


class Universe(Widget):

    def __init__(self, **kwargs):
        super(Universe, self).__init__(**kwargs)
        num_Balls = 100

        wave1 = Wave(step=.6, amp=50, num=num_Balls)
        wave2 = Wave(step=.3, amp=70, num=num_Balls)
        wave3 = Wave(step=.2, amp=10, num=num_Balls)
        wave4 = Wave(step=.1, amp=150, num=num_Balls)

        waveCollection = [wave1, wave2, wave3, wave4]

        newWave = Wave(step=0, num=num_Balls)
        self.add_widget(newWave)

        Clock.schedule_interval(partial(Wave.update_mixWave, newWave, waveCollection), .05)


class NatureApp(App):

    def build(self):
        return Universe()



if __name__ == "__main__":
    NatureApp().run()
