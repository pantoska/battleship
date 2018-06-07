import pygame
from Game.Battle import Battle

class Menu:
    def __init__(self, width,height,screen):
        self.width = width
        self.height = height
        self.screen = screen
        #self.mainBoard = Board
        self.activeLoop = False

    def gameIntro(self):
        intro = True

        while intro:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

            self.screen.fill((255,255,255))
            largeText = pygame.font.Font('Font.ttf',115)
            TextSurf, TextRect = self.textObjects("Battleship", largeText)
            TextRect.center = ((self.width/2, (self.height-150)/4))
            self.screen.blit(TextSurf, TextRect)

            self.button((0,255,0),"Start",300,250,150,100, "play")
            self.button((255, 0, 0), "Koniec", 600,250,150,100, "exit")

            pygame.display.update()

    def button(self, color, text, x, y, width, height, action = None):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        if( x <= mouse[0] <= x+width and y <= mouse[1] <= y+ height):
            pygame.draw.rect(self.screen, color, (x,y, width, height))
            if(click[0] == 1 and action != None):
                if(action == "play"):
                    Battle.loop()
                    self.activeLoop = True
                elif(action == "exit"):
                    pygame.quit()
                    quit()

        smallText = pygame.font.Font("Font.ttf", 40)
        textSurf, textRect = self.textObjects(text, smallText)
        textRect.center = (x+75, y+45)
        self.screen.blit(textSurf, textRect)


    def textObjects(self, text, font):
        textSurface = font.render(text, True, (0,0,0))
        return textSurface, textSurface.get_rect()