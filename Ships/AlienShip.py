from Ships.Ship import Ship
import random

class AlienShip(Ship):

    def __init__(self, length):
            super().__init__(length)
            self.x = random.randint(0, 9)
            self.y = random.randint(0, 9)
            self.randHorizontal = random.randint(0, 1)
            if (self.randHorizontal == 0):
                self.setHorizontal = True
            else:
                self.setHorizontal = False

    def getPositionInField(self):
        coordinates = []
        coordinates.append(self.x)
        coordinates.append(self.y)

        if (self.setHorizontal == True):
            coordinates.append(self.length)
            coordinates.append(1)
        else:
            coordinates.append(1)
            coordinates.append(self.length)
        coordinates.append(self.setHorizontal)

        return coordinates

