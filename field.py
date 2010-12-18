from general import *
class Field():
    """ Methods and properties related to rendering the field, goals, goals and scores. """
    def __init__(self):
        self.__grass_field, rect = load_image(filepath="grass.jpg");# grass1000x1000.bmp");
        self.__grass_field = self.__grass_field.convert()

        self.__goal1 = Goal("down")
        self.__goal2 = Goal("up")
        self.__goal1.rect.move_ip(width/2.0 - self.__goal1.image.get_size()[0]/2.0, 0)
        self.__goal2.rect.move_ip(width/2.0 - self.__goal2.image.get_size()[0]/2.0, height - self.__goal2.image.get_size()[1])

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

        surface.blit(self.__goal1.image, (self.__goal1.rect.left - cameraPos[0], self.__goal1.rect.top - cameraPos[1]) )
        surface.blit(self.__goal2.image, (self.__goal2.rect.left - cameraPos[0], self.__goal2.rect.top - cameraPos[1]) )

    def blitBackground(self, surface):
        """ Blit the background field. """
        nbrHor = int (math.ceil(width  / self.getField().get_size()[0]))
        nbrVer = int (math.ceil(height / self.getField().get_size()[1]))
        for i in range(0,nbrHor):
            for j in range(0,nbrVer):
                surface.blit(self.getField(), (
                    i * self.getField().get_size()[0]-cameraPos[0],
                    j * self.getField().get_size()[1]-cameraPos[1]))

class Goal(pygame.sprite.Sprite):
    """ The class for the goal."""
    def __init__(self, direction):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image(filepath="goal2.bmp")
        self.image = self.image.convert_alpha()
        self.direction = direction

        if direction == 'up':
            self.image = pygame.transform.flip(self.image, False, True)

    def get_left_rect(self):
        return pygame.Rect(self.rect.topleft,     (5, self.image.get_size()[1]))
    def get_right_rect(self):
        return pygame.Rect((self.rect.right - 5, self.rect.top), (5, self.image.get_size()[1]))
    def get_back_rect(self):
        return pygame.Rect(self.rect.topleft, (self.image.get_size()[0]), 5)
