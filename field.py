from general import *
import general
class Field():
    """ Methods and properties related to rendering the field, goals, goals and scores. """
    def __init__(self):
        self.__grass_field, rect = load_image(filepath="grass.jpg");
        self.__grass_field = self.__grass_field.convert()
        self.__grass_size = self.__grass_field.get_size()

        self.__goal1 = Goal("down")
        self.__goal2 = Goal("up")
        self.__goal1.rect.move_ip(width/2.0 - self.__goal1.image.get_size()[0]/2.0, 0 + 50)
        self.__goal2.rect.move_ip(width/2.0 - self.__goal2.image.get_size()[0]/2.0, height - self.__goal2.image.get_size()[1] - 50)

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

        goal1_pos = [self.__goal1.rect.left - cameraPos[0], self.__goal1.rect.top - cameraPos[1]]
        goal2_pos = [self.__goal2.rect.left - cameraPos[0], self.__goal2.rect.top - cameraPos[1]]
        global_zoom = general.global_zoom
        image1 = self.__goal1.image
        image2 = self.__goal2.image
        if global_zoom != 1:
            goal1_pos = [goal1_pos[0] * global_zoom, goal1_pos[1] * global_zoom]
            goal2_pos = [goal2_pos[0] * global_zoom, goal2_pos[1] * global_zoom]
            goal1_size = self.__goal1.image.get_size()
            goal2_size = self.__goal2.image.get_size()
            image1 = pygame.transform.scale(image1, (int(goal1_size[0]*global_zoom), int(goal1_size[1]*global_zoom)))
            image2 = pygame.transform.scale(image2, (int(goal2_size[0]*global_zoom), int(goal2_size[1]*global_zoom)))

        surface.blit(image1, goal1_pos)
        surface.blit(image2, goal2_pos)

    def blitBackground(self, surface):
        """ Blit the background field. """
        self.__grass_field = pygame.transform.smoothscale(self.__grass_field,
                (int(self.__grass_size[0] * general.global_zoom), int(self.__grass_size[1] * general.global_zoom)) )

        nbrHor = int (math.ceil(width * general.global_zoom / self.getField().get_size()[0]))
        nbrVer = int (math.ceil(height* general.global_zoom / self.getField().get_size()[1]))
        for i in range(0,nbrHor):
            for j in range(0,nbrVer):
                surface.blit(self.getField(), (
                    i * self.getField().get_size()[0]-cameraPos[0]*general.global_zoom,
                    j * self.getField().get_size()[1]-cameraPos[1]*general.global_zoom))

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
        l = self.rect.left
        t = self.rect.top
        sizey = self.image.get_size()[1]
        return pygame.Rect(l, t, 5, sizey)

    def get_right_rect(self):
        r = self.rect.right
        t = self.rect.top
        sizey = self.image.get_size()[1]
        return pygame.Rect(r - 5, t, 5, sizey)

    def get_back_rect(self):
        l = self.rect.left
        t = self.rect.top
        b = self.rect.bottom
        sizex = self.image.get_size()[0]

        if self.direction == 'up':
            return pygame.Rect(l, b - 5, sizex, 5)
        else:
            return pygame.Rect(l, t, sizex, 5)
