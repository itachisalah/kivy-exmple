from kivy.vector import Vector

class PVector(Vector):

    def __init__(self, *args, **kwargs):
        super(PVector, self).__init__(*args, **kwargs)

    def limit(self, val):
        if self.length() > val:
            #TODO: Limited value tends to drift over time
            #Possible solution: Decimal module
            self[0], self[1] = self.normalize() * val

    def abs(self):
        return PVector(abs(self[0]), abs(self[1]))
