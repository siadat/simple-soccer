from general import *
import general
class Field(pygame.sprite.Sprite):
    """ Methods and properties related to rendering the field, goals, goals and scores. """
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        #self.image, self.rect = load_image(filepath= os.path.dirname(sys.argv[0]) + "grass.jpg");
        self.image, self.rect = load_image(filepath= "grass.jpg");
        self.image = self.image.convert()
        self.__grass_size = self.image.get_size()

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
        return self.image

    def setField(self, field):
        """ Get field. """
        self.image = field

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

        goal1_pos = Array(self.__goal1.rect.topleft) - cameraPos
        goal2_pos = Array(self.__goal2.rect.topleft) - cameraPos

        global_zoom = general.global_zoom
        image1 = self.__goal1.image
        image2 = self.__goal2.image

        if global_zoom != 1:
            goal1_pos = Array(goal1_pos) * global_zoom
            goal2_pos = Array(goal2_pos) * global_zoom

            goal1_size = self.__goal1.image.get_size()
            goal2_size = self.__goal2.image.get_size()
            image1 = pygame.transform.scale(image1, (Array(goal1_size) * global_zoom).int())
            image2 = pygame.transform.scale(image2, (Array(goal2_size) * global_zoom).int())

        surface.blit(image1, goal1_pos)
        surface.blit(image2, goal2_pos)

    def blitBackground(self, surface):
        """ Blit the background field. """
        self.setField(pygame.transform.smoothscale(self.getField(),
                (int(self.__grass_size[0] * general.global_zoom), int(self.__grass_size[1] * general.global_zoom)) ))

        nbrHor = int (math.ceil(width * general.global_zoom / self.getField().get_size()[0]))
        nbrVer = int (math.ceil(height* general.global_zoom / self.getField().get_size()[1]))
        for i in range(0,nbrHor):
            for j in range(0,nbrVer):
                surface.blit(self.getField(), (
                    i * self.getField().get_size()[0]-cameraPos[0]*general.global_zoom,
                    j * self.getField().get_size()[1]-cameraPos[1]*general.global_zoom))

        line_color = pygame.Color(240,250,220)
        ## centre line
        drawRect  (surface, line_color, [0, height/2.0-1], [width, height/2.0+1])
        ## big circle in the middle
        drawCircle(surface, line_color, [width/2.0, height/2.0], 80)
        ## small circle where ball is
        drawCircle(surface, line_color, [width/2.0, height/2.0], 4,0)
        ## line behind goal 1
        goal1_pos = [self.getGoal1().rect.left, self.getGoal1().rect.top]
        drawRect  (surface, line_color, [0, goal1_pos[1]], [width, goal1_pos[1]])
        ## line behind goal 2
        goal2_pos = [self.getGoal2().rect.left, self.getGoal2().rect.bottom]
        drawRect  (surface, line_color, [0, goal2_pos[1]], [width, goal2_pos[1]])

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
            return pygame.Rect(l+5, b - 5, sizex-5*2, 5)
        else:
            return pygame.Rect(l+5, t, sizex-5*2, 5)
