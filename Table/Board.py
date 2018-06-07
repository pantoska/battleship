from Table.Field import Field
from Ships.Ship import Ship
from Ships.AlienShip import AlienShip
from Game.MyException import MyException

class Board:
    maxSize = 10
    def __init__(self, dx, dy):
        self.dx = dx
        self.dy = dy
        self.field = []
        self.statusOfshootedField = False
        self.counterOfshootFields = 0
        self.saveColor = (255,255,255)
        self.rememberPositionOfShip =[]
        #list comprehension
        self.field = [[Field(i,j) for j in range(self.maxSize)] for i in range(self.maxSize)]

    checkSizes = lambda mx, my: True if 0 <= mx <= 9 and 0 <= my <= 9 else False

    def drawBoard(self, screen):
        for i in range(self.maxSize):
            for j in range(self.maxSize):
                self.field[i][j].drawField(screen, self.dx, self.dy, i, j)#zmiana

    def changeColorField(self,mx,my):

        positionmx = (mx - self.dx) // Field.size
        positionmy = (my - self.dy) // Field.size

        if (Board.checkSizes(positionmx,positionmy) == True):
            if(self.field[positionmx][positionmy].shootAgain == False):
                if(self.field[positionmx][positionmy].shootAlienShip == True):
                    self.field[positionmx][positionmy].changeColor((255,0,0))
                    self.counterOfshootFields += 1
                    self.saveColor = (255,0,0)
                    self.field[positionmx][positionmy].shootAgain = True
                else:
                    self.field[positionmx][positionmy].changeColor((0, 0, 255))
                    self.saveColor = (0, 0, 255)
                    self.field[positionmx][positionmy].shootAgain = True
            else:
                return False
        else:
            return False
        return True

    def changeColorFieldbyAlien(self,mx,my):
        if (Board.checkSizes(mx, my) == True):
            if (self.field[mx][my].shootShip == True):
                self.field[mx][my].changeColor((255, 0, 0))
                self.counterOfshootFields += 1
                return True
            else:
                self.field[mx][my].changeColor((0, 0, 255))
        return False

    #rysuje statki na swojej planszy
    def drawShip(self, myShip):
        if not isinstance(myShip, Ship):
            raise MyException("Valid instance of Ship")

        positionmx = myShip.x // Field.size
        positionmy = myShip.y // Field.size

        if (self.checkBoundaries(myShip, False) == True):
            if (myShip.setHorizontal == True):
                for i in range(0, myShip.length):
                    self.field[positionmx + i][positionmy].changeColor((218,165,32))
                    self.field[positionmx + i][positionmy].shootShip= True
                    self.field[positionmx + i][positionmy].howLongShip = myShip.length #ustawiam dlugosc statku dla informacji czy zatopiony
                #self.rememberPosOfOne = []
                #self.rememberPositionOfShip.append
            else:
                for i in range(0, myShip.length):
                    self.field[positionmx][positionmy + i].changeColor((218,165,32))
                    self.field[positionmx][positionmy + i].shootShip = True
                    self.field[positionmx][positionmy + i].howLongShip = myShip.length #ustawiam dlugosc statku dla informacji czy zatopiony
            return True
        else:
            print("Nie możesz tu umieścić statku!")
            return False

    def checkBoundaries(self,myShip,alien):
        if not isinstance(myShip, Ship):
            raise MyException("Valid instance of Ship")
        if (alien == False):
            information = myShip.getPositionInField()
            x = information[0]
            y = information [1]
            width = information [2]
            height = information [3]
        else:
            information = myShip.getPositionInField()
            x = information[0]
            y = information[1]
            width = information[2]
            height = information[3]

        if x < 0 or x + width > 10 or y < 0 or y + height > 10:
            return False

        for i in range(x, width + x):
            for j in range(y, height + y):
                if self.field[i][j].blocked == True:
                    return False

        width = width + 1
        height = height + 1
        if x - 1 >= 0:
            if x != self.maxSize - 1 and x + width <= self.maxSize:
                width += 1
            x -= 1

        if y - 1 >= 0:
            if y != self.maxSize - 1 and y + height <= self.maxSize:
                height += 1
            y -= 1

        for i in range(x, width + x):
            for j in range(y, height + y):
                self.field[i][j].blocked = True

        return True

    def drawShipsAlien(self, currentAlienShip):
        if not isinstance(currentAlienShip, AlienShip):
            raise MyException("Valid instance of AlienShip")
        if (self.checkBoundaries(currentAlienShip, True) == True):
            if (currentAlienShip.setHorizontal == True):
                for i in range(currentAlienShip.length):
                    self.field[currentAlienShip.x + i][currentAlienShip.y].changeColor((176,196,222))
                    self.field[currentAlienShip.x + i][currentAlienShip.y].shootAlienShip = True
                    self.field[currentAlienShip.x + i][currentAlienShip.y].howLongShip = currentAlienShip.length
                self.appendToArray(currentAlienShip, True)
            else:
                for i in range(0, currentAlienShip.length):
                    self.field[currentAlienShip.x][currentAlienShip.y + i].changeColor((176,196,222))
                    self.field[currentAlienShip.x][currentAlienShip.y + i].shootAlienShip = True
                    self.field[currentAlienShip.x][currentAlienShip.y + i].howLongShip = currentAlienShip.length
                self.appendToArray(currentAlienShip, False)
            return True
        else:
            return False

    def getShiplength(self,x,y):
        return self.field[x][y].howLongShip

    def changeColorFieldonGrey(self,mx,my):
        self.field[mx][my].changeColor((47,79,79))

    def checkPosition(self,x,y, list):
        xx, yy, height, width = list
        for i in range (0, width):
            for j in range(0, height):
                if (xx + i == x and yy + j == y):
                    return True
        return False

    def changeColorShipOnGrey(self, list):
        xx, yy, height, width = list
        for i in range (0, width):
            for j in range(0, height):
                self.changeColorFieldonGrey(xx + i, yy + j)

    def appendToArray(self, currentAlienShip, horizontal):
        self.rememberPosOfOne = []
        self.rememberPosOfOne.append(currentAlienShip.x)
        self.rememberPosOfOne.append(currentAlienShip.y)

        if (horizontal == True):
            self.rememberPosOfOne.append(1)
            self.rememberPosOfOne.append(currentAlienShip.length)
        else:
            self.rememberPosOfOne.append(currentAlienShip.length)
            self.rememberPosOfOne.append(1)

        self.rememberPositionOfShip.append(self.rememberPosOfOne)

    def showAllShips(self):
        for i in range(self.maxSize):
            for j in range(self.maxSize):
                if(self.field[i][j].shootAlienShip == True and self.field[i][j].shootAgain == False):
                    self.field[i][j].changeColor((130, 180, 0))



































