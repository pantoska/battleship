from Table.Field import Field
import pygame
import math

class Ship:

    def __init__(self, length):
        self.x = 0
        self.y = 0
        self.length = length
        self.color = (218,165,32)
        self.setHorizontal = True
        self.xcoordinate = 0
        self.ycoordinate = 0

    def setPosition(self,mx,my,screen):
        self.x = mx
        self.y = my
        if self.setHorizontal == True:
            self.drawShipHorizontal(screen)
        else:
            self.drawShipVertical(screen)

    def getPositionInField(self):
        coordinates = []
        self.xcoordinate = math.floor(self.x / Field.size)
        self.ycoordinate = math.floor(self.y / Field.size)
        coordinates.append(self.xcoordinate)
        coordinates.append(self.ycoordinate)

        if (self.setHorizontal == True):
            coordinates.append(self.length)
            coordinates.append(1)
        else:
            coordinates.append(1)
            coordinates.append(self.length)
        coordinates.append(self.setHorizontal)
        return coordinates

    def drawShipHorizontal(self,screen):
        self.setHorizontal = True
        pygame.draw.rect(screen, self.color, pygame.Rect(self.x, self.y, Field.size*self.length, Field.size))

    def drawShipVertical(self, screen):
        self.setHorizontal = False
        pygame.draw.rect(screen, self.color, pygame.Rect(self.x, self.y, Field.size, Field.size* self.length))

