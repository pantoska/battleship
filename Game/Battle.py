from Table.Board import Board
from Table.Field import Field
from Ships.Ship import Ship
from Game.Alien import Alien
from Ships.AlienShip import AlienShip
from Game.MyException import MyException
import random
import pygame

class Battle:

    counter = 0
    pygame.init()
    pygame.display.set_caption('Battleship')

    def __init__(self):
        self.again = False
        self.resetAll()

    def resetAll(self):
        Battle.counter = 0
        self.alien = Alien()
        self.width = 2 * Field.size * Board.maxSize + Field.size
        self.height = Field.size * Board.maxSize + Field.size * 3
        self.widthAlienTable = Field.size * Board.maxSize + Field.size

        self.mainBoard = Board(0, 0)
        self.alienBoard = Board(self.widthAlienTable, 0)
        self.counterforme = 0

        self.ships = [Ship(4), Ship(3), Ship(3), Ship(2), Ship(2), Ship(2),
                      Ship(1), Ship(1), Ship(1), Ship(1)]
        self.shipsAlien = [AlienShip(4), AlienShip(3), AlienShip(3), AlienShip(2), AlienShip(2), AlienShip(2),
                           AlienShip(1), AlienShip(1), AlienShip(1), AlienShip(1)]
        self.finish = False
        self.setReset = False
        self.previousFields = []
        self.alocated = [True, False, False, False]
        self.endOfGame = False
        self.yourTurn = random.randint(0, 1)

        self.screen = pygame.display.set_mode((self.width, self.height))
        if(self.again == False):
            self.gameIntro()
        else:
            self.loop()

    def gameIntro(self):
        intro = True

        while intro:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

            self.screen.fill((180,180,255))
            largeText = pygame.font.Font('../Font/Font.ttf',115)
            TextSurf, TextRect = self.textObjects("Battleship", largeText)
            TextRect.center = ((self.width/2, (self.height-150)/4))
            self.screen.blit(TextSurf, TextRect)

            self.button((0,255,0),"Start",300,350,150,100, "play")
            self.button((255, 0, 0), "Exit", 600,350,150,100, "exit")

            pygame.display.update()

    def button(self, color, text, x, y, width, height, action = None):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        if( x <= mouse[0] <= x+width and y <= mouse[1] <= y+ height):
            pygame.draw.rect(self.screen, color, (x,y, width, height))
            if(click[0] == 1 and action != None):
                if(action == "play"):
                    self.loop()
                elif(action == "exit"):
                    pygame.quit()
                    quit()

        smallText = pygame.font.Font('../Font/Font.ttf', 40)
        textSurf, textRect = self.textObjects(text, smallText)
        textRect.center = (x+75, y+45)
        self.screen.blit(textSurf, textRect)


    def textObjects(self, text, font):
        textSurface = font.render(text, True, (0,0,0))
        return textSurface, textSurface.get_rect()

    def checkCounter(self, Board1, Board2):
        if not isinstance(Board1, Board):
            raise MyException("Valid instance of Board")
        if not isinstance(Board2, Board):
            raise MyException("Valid instance of Board")

        if(Board2.counterOfshootFields == 20):
            self.drawStartButton("You Win!!!", 650, 550, 300,80)
            return True
        elif(Board1.counterOfshootFields == 20):
            self.drawStartButton("Bot win!!!", 650, 550,300,80)
            return True
        else:
            return False

    def drawStartButton(self, status, x, y, width, heigth):
        pygame.draw.rect(self.screen, (192,192,192), (x, y, width, heigth))
        smallText = pygame.font.Font('../Font/Font.ttf', 40)
        textSurf, textRect = self.textObjects(status, smallText)
        if(x < 600):
            textRect.center = (x + 75, y + 35)
        else:
            textRect.center = (x + 155, y + 35)
        self.screen.blit(textSurf, textRect)

    def draw(self,screen):
        screen.fill((0, 0, 1))
        self.mainBoard.drawBoard(screen)
        self.alienBoard.drawBoard(screen)
        if(self.setReset == False):
            self.drawStartButton("Start",200, 550,150, 80)
        else:
            self.drawStartButton("Reset",200, 550,150, 80)

    def drawAlocatedShips(self):
        if (Battle.counter < 10):
            if (Battle.counter == 0):

                self.alocated[0] = False
                self.alocated[1] = True

                if(self.mainBoard.drawShip(self.ships[Battle.counter]) == False):
                    Battle.counter -= 1
            if (Battle.counter > 0 and Battle.counter < 3):
                self.alocated[1] = False
                self.alocated[2] = True
                if(self.mainBoard.drawShip(self.ships[Battle.counter]) == False):
                    Battle.counter -= 1
            if (Battle.counter >= 3 and Battle.counter <= 5):
                self.alocated[2] = False
                self.alocated[3] = True
                if(self.mainBoard.drawShip(self.ships[Battle.counter]) == False):
                    Battle.counter -= 1
            if (Battle.counter > 5 and Battle.counter <= 9):
                self.alocated[3] = True
                if(self.mainBoard.drawShip(self.ships[Battle.counter]) == False):
                    Battle.counter -= 1


    def drawAlienShips(self):
        for i in range(len(self.shipsAlien)):
            flag = True
            while (flag == True):
                if (self.alienBoard.drawShipsAlien(self.shipsAlien[i]) == False):
                    flag = True
                    self.shipsAlien[i].x = random.randint(0, 9)
                    self.shipsAlien[i].y = random.randint(0, 9)
                else:
                    flag = False

    def loop(self):
        if (self.yourTurn == 0):
            self.yourTurn = True
        else:
            self.yourTurn = False

        done = False

        while not done:
            mx, my = pygame.mouse.get_pos()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.again = False
                    self.resetAll()
                    done = True
                if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                    self.alienBoard.showAllShips()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and self.finish == False:
                    if (self.ships[Battle.counter].setHorizontal == True):
                        self.ships[Battle.counter].drawShipVertical(self.screen)
                    else:
                        self.ships[Battle.counter].drawShipHorizontal(self.screen)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if (self.alien.active == True and self.yourTurn == True and self.endOfGame == False):
                        if(self.alienBoard.changeColorField(mx,my) == True):
                            self.yourTurn = False
                            if(self.alienBoard.saveColor == (255,0,0)):

                                positionmx = (mx - self.widthAlienTable) // Field.size
                                positionmy = (my) // Field.size
                                self.previousFields.append(tuple((positionmx, positionmy)))

                                for i in range(0, len(self.helpArray)):
                                    if (self.alienBoard.checkPosition(positionmx, positionmy,self.helpArray[i]) == True):
                                        counter = 0
                                        #self.counterforme = 0
                                        xx, yy, width, height = self.helpArray[i]
                                        if width > height:
                                            maxcounter = width
                                        else:
                                            maxcounter = height
                                        for pos in self.previousFields:
                                            if self.alienBoard.checkPosition(pos[0], pos[1],self.helpArray[i]):
                                                counter += 1
                                                #self.counterforme += 1
                                        if counter == maxcounter:
                                            self.alienBoard.changeColorShipOnGrey(self.helpArray[i])
                                        break
                            

                    if (200 <= mx <= 200+150 and 550 <= my <= 550 + 70):
                        if(self.setReset == True):
                            self.again = True
                            self.resetAll()
                            self.setReset = True
                        elif (self.setReset == False and Battle.counter >= 10):
                            self.drawAlienShips()
                            self.helpArray = self.alienBoard.rememberPositionOfShip
                            self.table = self.alien.tableToShoot()
                            self.alien.active = True
                            self.setReset = True

                    self.drawAlocatedShips()
                    Battle.counter += 1
            if(Battle.counter < 10):
                self.setReset = True
            if(Battle.counter >= 10 and self.alien.active == False):
                self.setReset = False

            #rysowanie boardu
            self.draw(self.screen)

            if (self.yourTurn == False and self.alien.active == True and self.endOfGame == False):
                self.alien.shoot(self.table,self.mainBoard)
                self.yourTurn = True

            if(self.checkCounter(self.mainBoard,self.alienBoard) == True):
                self.endOfGame = True

            #typ statku ktory pojawi sie przy kursorze
            if (Battle.counter < 10):
                for i in range(len(self.alocated)):
                    if (self.alocated[i] == True):
                        self.ships[Battle.counter].setPosition(mx, my, self.screen)
            else:
                self.finish = True

            pygame.display.flip()
            pygame.display.update()

