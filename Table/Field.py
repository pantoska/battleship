import pygame

class Field:

    size = 50
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.color = (176,196,222)
        self.blocked = False
        self.shootShip = False
        self.shootAlienShip = False
        self.shootAgain = False
        self.howLongShip = 0

    def drawField(self, screen, dx, dy,x,y):
        pygame.draw.rect(screen, self.color, pygame.Rect(x * Field.size + dx, y * Field.size + dy, Field.size - 1, Field.size - 1))

    def changeColor(self, color):
        self.color = color


