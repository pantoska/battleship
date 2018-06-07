import random
from Table.Board import Board
from Game.MyException import MyException

class Alien:
    def __init__(self):
        self.active = False
        self.temp = []
        self.counter = 0
        self.flag = False
        self.choosed = False
        self.temp1 = []
        self.previousFields = []
    def shoot(self, table, boardAlien):

        if not isinstance(boardAlien, Board):
            raise MyException("Valid instance of Board")

        if (len(table) != 0 ):

            # wybiera z tabeli tymczasowej gdzie ma boki do sprawdzenia
            if (len(self.temp) != 0):
                x,y = random.choice(self.temp)
                if (x, y) in table:
                    table.remove((x, y))
            # gdy tymczasowa jest pusta, ale trzeba sprawdzić drugi bok
            elif(len(self.temp) == 0 and self.choosed == True):
                self.checkOtherSide(self.rememberX, self.rememberY, table, self.temp1)
                #jest nie ma już drugiego boku to sprawdza z pierwszej tabeli
                if(len(self.temp1) != 0):
                    x, y = random.choice(self.temp1)
                    if(x,y) in table:
                        table.remove((x,y))
                else:
                    x, y = random.choice(table)
                    if (x, y) in table:
                        table.remove((x, y))
                    self.flag = False
                    self.choosed = False
                self.choosed = False
            else:
                x,y = random.choice(table)
                if (x, y) in table:
                    table.remove((x, y))
                self.flag = False
                self.choosed = False
            # jesli alien trafi w plansze
            if (boardAlien.changeColorFieldbyAlien(x, y) == True):
                self.counter += 1
                self.previousFields.append(tuple((x, y)))

                #jesli statek został zatopiony, to ustawia jego kolor na szary
                if(self.counter == boardAlien.getShiplength(x, y)):
                    for x,y in self.previousFields:
                        boardAlien.changeColorFieldonGrey(x, y)
                        self.removeCorners(x, y, table, True)
                    del self.previousFields[:]
                    self.counter = 0


                    #jesli jest to pojedynczy statek to usuwa wszystkie boki wokol niego
                    if(boardAlien.getShiplength(x, y) == 1):
                        self.removeCorners(x, y, table,True)

                    #usuwa z generalnej tabeli to co bylo w tymczasowych tablicach
                    #list comprehension
                    if (self.temp != 0):
                        table = [(x, y) for x, y in table if (x, y) not in self.temp]
                    if (self.temp1 != 0):
                        table = [(x, y) for x, y in table if (x, y) not in self.temp1]

                    del self.temp[:]
                    del self.temp1[:]

                    self.choosed = False

                else:
                    # zapisuje pierwsze wspolrzedne,aby miec odniesienie do kolejnego boku
                    if (self.choosed == False):
                        self.choosed = True
                        self.rememberX = x
                        self.rememberY = y
                    #usuwa poprzednie wspolrzedne
                    if(self.temp1 != 0):
                        if (x, y) in self.temp1:
                            self.temp1.remove((x, y))

                    #usuwa pola, ktore stykaja sie krawedzia
                    self.removeCorners(x,y,table,False)

                    #sprawdza czy lista dla kolejnych pol jest pusta, jesli nie to usuwa ja z tej listy oraz generalnej listy
                    if(len(self.temp) != 0):
                        del self.temp[:]

                        if(x == self.rememberX):
                            if (((self.rememberX-1,self.rememberY)) in table):
                                table.remove((self.rememberX-1,self.rememberY))
                            if (((self.rememberX+1,self.rememberY)) in table):
                                table.remove((self.rememberX+1,self.rememberY))

                        if(y == self.rememberY):
                            if (((self.rememberX,self.rememberY-1)) in table):
                                table.remove((self.rememberX,self.rememberY-1))
                            if (((self.rememberX,self.rememberY+1)) in table):
                                table.remove((self.rememberX,self.rememberY+1))

                    #jesli lista jest pusta
                    if(len(self.temp) == 0):

                        if (x, y) in table:
                            table.remove((x, y))
                        self.checkOtherSide(x,y,table, self.temp)

            #jesli spudlowano,tez dodaje do tabeli
            else:
                if (x, y) in table:
                    table.remove((x, y))
                if (x, y) in self.temp:
                    self.temp.remove((x, y))
                if (x, y) in self.temp1:
                    self.temp1.remove((x, y))

    def checkOtherSide(self, x,y, table, list):
        append = lambda x,y : list.append(tuple((x, y))) if ((x, y) in table) else False

        append(x-1,y)
        append(x+1,y)
        append(x,y+1)
        append(x,y-1)

    #list comprehension
    def tableToShoot(self):
        self.positionToShoot = [tuple((i, j)) for i in range(10) for j in range(10)]
        return self.positionToShoot

    def removeCorners(self,x,y,table,allCorners):
        remove = lambda x, y: table.remove((x, y)) if (x, y) in table else False

        remove(x,y)
        remove(x - 1, y - 1)
        remove(x + 1, y + 1)
        remove(x - 1, y + 1)
        remove(x + 1, y - 1)

        if(allCorners == True):
            remove(x - 1, y)
            remove(x + 1, y)
            remove(x, y + 1)
            remove(x, y - 1)








