from kivy.vector import Vector

class PVector(Vector):


    def __init__(self, *args, **kwargs):
        super(PVector, self).__init__(*args, **kwargs)

    def __add__(self, val):
        return PVector(list(map(lambda x, y: x + y, self, val)))

    def __neg__(self):
        return PVector([-x for x in self])

    def __sub__(self, val):
        return PVector(list(map(lambda x, y: x - y, self, val)))

    def __mul__(self, val):
        try:
            return PVector(list(map(lambda x, y: x * y, self, val)))
        except Exception:
            return PVector([x * val for x in self])

    def __truediv__(self, val):
        try:
            return PVector(list(map(lambda x, y: x / y, self, val)))
        except Exception:
            return PVector([x / val for x in self])

    def __rtruediv__(self, val):
        try:
            return PVector(*val) / self
        except Exception:
            return PVector(val, val) / self

    def get(self):
        return PVector(self.x, self.y)

    def normalize(self):
        '''Normalize the value in-place to has length 1
        return: self
        '''
        if self[0] == 0. and self[1] == 0.:
            return self
        # Compute the length once instead of twice (for x and y)
        # Otherwise the length changes as well after the x get changed
        length = self.length()
        self[0], self[1] = self[0]/length, self[1]/length

        return self

    def limit(self, val):
        if self.length() > val:
            #TODO: Limited value tends to drift over time
            #Possible solution: Decimal module

            self[0], self[1] = self.normalize() * val

    def abs(self):
        return PVector(abs(self[0]), abs(self[1]))

    def rotate(self, angle):
        '''Rotate the vector with an angle in degrees.

        >>> v = Vector(100, 0)
        >>> v.rotate(45)
        [70.71067811865476, 70.71067811865474]

        '''
        angle = math.radians(angle)
        return PVector(
            (self[0] * math.cos(angle)) - (self[1] * math.sin(angle)),
            (self[1] * math.cos(angle)) + (self[0] * math.sin(angle)))
