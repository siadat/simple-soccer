from general import *
class Field():
    """ Methods and properties related to rendering the field, goals, goals and scores. """
    def __init__(self):
        self.__grass_field, rect = load_image(filepath="grass.jpg");# grass1000x1000.bmp");
        self.__grass_field = self.__grass_field.convert()
        self.__goal1, rect = load_image(filepath="goal2.bmp")
        self.__goal2 = pygame.transform.flip(self.__goal1, False, True)
        self.__goal1 = self.__goal1.convert_alpha()
        self.__goal2 = self.__goal2.convert_alpha()
        self.__font = pygame.font.Font(None, 76)
        self.__message1 = self.__font.render(str(0), True, (30, 40, 210))
        self.__message2 = self.__font.render(str(0), True, (210, 40, 30))
        self.score1 = 0
        self.score2 = 0
        self.__goal_bar_width = 5.0

    def getField(self):
        """ Get field. """
        return self.__grass_field

    def getGoal1(self):
        """ Get goal 1. """
        return self.__goal1

    def getGoal2(self):
        """ Get goal 2. """
        return self.__goal2

    def getBarWidth(self):
        """ Get goal bar width. """
        return self.__goal_bar_width

    def setMessage1(self):
        """ Render score1. """
        self.__message1 = pygame.Surface((150,50))
        self.__message1 = self.__font.render( str(self.score1), True, (30, 40, 210))

    def setMessage2(self):
        """ Render score2. """
        self.__message2 = pygame.Surface((150,50))
        self.__message2 = self.__font.render( str(self.score2), True, (210, 40, 30))

    def blitField(self, width, height, surface, cameraPos):
        """ Blit messages and the goals. """
        surface.blit(self.__message1,(0,0))
        surface.blit(self.__message2,(0,50))
        surface.blit(self.__goal1, (width/2.0 - self.__goal1.get_size()[0]/2.0 - cameraPos[0], 0 - cameraPos[1]))
        surface.blit(self.__goal2, (width/2.0 - self.__goal1.get_size()[0]/2.0 - cameraPos[0], height - self.__goal2.get_size()[1] - cameraPos[1]))

    def blitBackground(self, surface):
        """ Blit the background field. """
        nbrHor = int (math.ceil(width  / self.getField().get_size()[0]))
        nbrVer = int (math.ceil(height / self.getField().get_size()[1]))
        for i in range(0,nbrHor):
            for j in range(0,nbrVer):
                surface.blit(self.getField(), (
                    i * self.getField().get_size()[0]-cameraPos[0],
                    j * self.getField().get_size()[1]-cameraPos[1]))
