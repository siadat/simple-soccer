# {{{ Imports
import pygame, os
import random
import math
from pygame.locals import *
from general import *
# }}}
# {{{ Keyboard 
class Keyboard():
    """ Determining the name of a key code. """
    def __init__(self, pygame_event): self.__pygame_event = pygame_event
    def isKEYUP(self): return self.__pygame_event.type == pygame.KEYUP;
    def isKEYDOWN(self): return self.__pygame_event.type == pygame.KEYDOWN;
    def isLeft(self): return self.__pygame_event.key == pygame.K_LEFT;
    def isRight(self): return self.__pygame_event.key == pygame.K_RIGHT;
    def isUp(self): return self.__pygame_event.key == pygame.K_UP;
    def isDown(self): return self.__pygame_event.key == pygame.K_DOWN;
    def isA(self): return self.__pygame_event.key == pygame.K_a;
    def isD(self): return self.__pygame_event.key == pygame.K_d;
    def isW(self): return self.__pygame_event.key == pygame.K_w;
    def isS(self): return self.__pygame_event.key == pygame.K_s;
    def isPeriod(self): return self.__pygame_event.key == pygame.K_PERIOD;
    def isComma(self): return self.__pygame_event.key == pygame.K_COMMA;
    def isBackquote(self): return self.__pygame_event.key == pygame.K_BACKQUOTE;
    def isEscape(self): return self.__pygame_event.key == pygame.K_ESCAPE;
# }}}
# {{{ GeneralMovingBody 
class GeneralMovingBody(pygame.sprite.Sprite):
    """ The base class for all movig bodies (e.g. ball, player and computer creature)."""
    def __init__(self, surface, size, showing=True):
        pygame.sprite.Sprite.__init__(self)

        self.sizex = size[0]
        self.sizey = size[1]
        self.scale = (self.sizex, self.sizey)
        self.surface = surface

        self.limitx = width  - self.sizex
        self.limity = height - self.sizey

        self.vel = [0, 0]
        self.acc = [0, 0]
        self.initial_pos = [width/2.0, height/2.0]
        self.showing = showing

        self.stoppingx = False
        self.stoppingy = False

        self.color     = pygame.Color(0,0,1)
        self.happiness = 0.0
        self.wealth = 0.0
        self.health = 0.0
        self.age    = 0.0
        self.angle  = 0.0
        self.fire_acc = 0.05
        self.mass = 1.0

    def reset(self):
        self.pos = [self.initial_pos[0], self.initial_pos[1]]
        self.vel = [0,0]
        self.acc = [0,0]

    def renderImage(self, image, cameraPos):
        self.surface.blit(image, (self.pos[0]-cameraPos[0],self.pos[1]-cameraPos[1]))
        self.drawCoordinates()

    def getCentre(self):
        """ Get the position of the centre of the body, given the position of topleft. """
        return [self.pos[0] + self.sizex/2.0, self.pos[1] + self.sizey/2.0]

    # TODO take into consideration the velocity of the ball when colliding
    def collidingHorizontallyLeft(self, line_top, line_bottom, line_x):
        threshold = 20
        self_top    = self.pos[1]
        self_bottom = self.pos[1] + self.sizey
        self_left   = self.pos[0]
        self_right  = self.pos[0] + self.sizex
        return (self_top < line_bottom and self_bottom > line_top ) and ( (diff(self_right, line_x) < threshold) and (self_right > line_x) )

    def collidingHorizontallyRight(self, line_top, line_bottom, line_x):
        threshold = 20
        self_top    = self.pos[1]
        self_bottom = self.pos[1] + self.sizey
        self_left   = self.pos[0]
        self_right  = self.pos[0] + self.sizex
        return (self_top < line_bottom and self_bottom > line_top ) and ( (diff(self_right, line_x) < threshold) and (self_left < line_x) )

    def collidingVerticallyBottom(self, line_left, line_right, line_y):
        threshold = 2
        self_top    = self.pos[1]
        self_bottom = self.pos[1] + self.sizey
        self_left   = self.pos[0]
        self_right  = self.pos[0] + self.sizex
        return (self_left < line_right and self_right > line_left ) and ( (diff(self_bottom, line_y) < threshold) and (self_top < line_y) )

    def collidingVerticallyTop(self, line_left, line_right, line_y):
        threshold = 2
        self_top    = self.pos[1]
        self_bottom = self.pos[1] + self.sizey
        self_left   = self.pos[0]
        self_right  = self.pos[0] + self.sizex
        return (self_left < line_right and self_right > line_left ) and ( (diff(self_bottom, line_y) < threshold) and (self_top > line_y) )

    def collidingGoal(self, goal_size):
        """ """
        if self.collidingHorizontallyLeft (line_top=0,                   line_bottom=goal_size[1], line_x=width/2.0 - goal_size[0]/2.0) \
        or self.collidingHorizontallyRight(line_top=0,                   line_bottom=goal_size[1], line_x=width/2.0 + goal_size[0]/2.0) \
        or self.collidingHorizontallyLeft (line_top=height-goal_size[1], line_bottom=height,       line_x=width/2.0 - goal_size[0]/2.0) \
        or self.collidingHorizontallyRight(line_top=height-goal_size[1], line_bottom=height,       line_x=width/2.0 + goal_size[0]/2.0):
            self.vel[0] = - self.vel[0]

    def fireLeft(self):
        """ Accelerate to the left. """
        self.acc[0] = - self.fire_acc
        self.stoppingx = False

    def fireRight(self):
        """ Accelerate to the right. """
        self.acc[0] = self.fire_acc
        self.stoppingx = False

    def fireUp(self):
        """ Accelerate upwards. """
        self.acc[1] = - self.fire_acc
        self.stoppingy = False

    def fireDown(self):
        """ Accelerate downwards. """
        self.acc[1] = self.fire_acc
        self.stoppingy = False

    def stopLeftAndRight(self):
        """ Stop accelerating horizontally. """
        self.stoppingx = True

    def stopUpAndDown(self):
        """ Stop accelerating vertically. """
        self.stoppingy = True

    def getShooted(self, kicker):
        """ Ball is shooted by kicker. """
        kicker_centre = kicker.getCentre()
        kicker_centre[0] = kicker.pos[0] + kicker.sizex/2.0
        kicker_centre[1] = kicker.pos[1] + kicker.sizey/2.0
        dist = distance ( [kicker_centre[0], kicker_centre[1]] , [self.pos[0]+self.sizex/2, self.pos[1]+self.sizey/2] )
        user_touch_dist = kicker.sizex/2 + self.sizex/2
        shoot_dist = user_touch_dist + 70
        if dist < shoot_dist:
            new_vel_0 = 2 * (self.vel[0] * (self.mass - kicker.mass) + 2 * kicker.mass * (self.pos[0]+self.sizex/2 - kicker_centre[0]) ) / (self.mass + kicker.mass)
            new_vel_1 = 2 * (self.vel[1] * (self.mass - kicker.mass) + 2 * kicker.mass * (self.pos[1]+self.sizey/2 - kicker_centre[1]) ) / (self.mass + kicker.mass)
            new_vel_size = math.sqrt( new_vel_0 ** 2 + new_vel_1 ** 2 )
            new_vel_0 = 500 * (new_vel_0 / new_vel_size) / dist
            new_vel_1 = 500 * (new_vel_1 / new_vel_size) / dist
            self.vel[0] = new_vel_0
            self.vel[1] = new_vel_1
            self.clockwise_spin = not self.clockwise_spin 

            ball_centre = self.getCentre()
            player_centre = kicker.getCentre()
            drawLine(self.surface, self.color, ball_centre, player_centre)


    def getKicked(self, kicker):
        """ Ball is kicker by kicker. """
        dist = distance ( [kicker.pos[0]+ kicker.sizex/2, kicker.pos[1]+kicker.sizey/2] , [self.pos[0]+self.sizex/2, self.pos[1]+self.sizey/2] )
        user_touch_dist = kicker.sizex/2 + self.sizex/2
        #if self.collidingHorizontallyLeft  (line_top=kicker.pos[1],  line_bottom=kicker.pos[1]+kicker.sizey, line_x=kicker.pos[0]) \
        #or self.collidingHorizontallyRight (line_top=kicker.pos[1],  line_bottom=kicker.pos[1]+kicker.sizey, line_x=kicker.pos[0]+kicker_size[1]) \
        #or self.collidingVerticallyTop     (line_left=kicker.pos[0], line_right=kicker.pos[0]+kicker.sizex,  line_y=kicker.pos[0]) \
        #or self.collidingVerticallyBottom  (line_left=kicker.pos[0], line_right=kicker.pos[0]+kicker.sizex,  line_y=kicker.pos[0]+kicker_size[0]):
        if dist < user_touch_dist:
            self.is_under_player = True
            self.vel[0] = 2 * (self.vel[0] * (self.mass - kicker.mass) + 2 * kicker.mass * kicker.vel[0]) / (self.mass + kicker.mass)
            self.vel[1] = 2 * (self.vel[1] * (self.mass - kicker.mass) + 2 * kicker.mass * kicker.vel[1]) / (self.mass + kicker.mass)
            self.clockwise_spin = not self.clockwise_spin 
        else:
            self.is_under_player = False


    def drawCoordinates(self):
        if debug:
            centre_pos = self.getCentre()
            drawLine(self.surface, self.color, [centre_pos[0], 0], [centre_pos[0],height])
            drawLine(self.surface, self.color, [0, centre_pos[1]], [width, centre_pos[1]])

# }}}

# {{{ BallBody
class BallBody(GeneralMovingBody):
    """ Everything a ball needs to know. """
    def __init__(self, surface, radius, showing=True):
        GeneralMovingBody.__init__(self,surface=surface,size=[radius*2,radius*2],showing=True)
        self.image, self.rect = load_image('ball.bmp', self.scale, -1)
        self.original = self.image
        self.initial_pos = [width/2.0,height/2.0]
        self.reset()
        self.move_turn = math.floor(random.random()*100)
        self.is_contact = False
        self.clockwise_spin = False
        self.radius = radius
        #self.mass = 1

    def move(self, time, cameraPos, target=None):
        self.__time = time
        self.__newpos()
        if self.showing: self.renderImage(self.image, cameraPos)

    def drawAimLine(self, player):
        ball_centre = self.getCentre()
        player_centre = player.getCentre()
        drawLine(self.surface, self.color, ball_centre, player_centre)

    def rot_center(self, rate):
        " Spin the body. "
        center = self.rect.center

        if self.clockwise_spin:
            self.angle += rate
        else:
            self.angle -= rate

        self.angle = self.angle % 360
        if self.angle == 0:
            self.image = self.original
        else:
            rotate = pygame.transform.rotate
            self.image = rotate(self.original, self.angle)
        self.rect = self.image.get_rect(center=center)

    def __newpos(self):
        limit = [self.limitx, self.limity]
        for i in range(0,2):
            if self.vel[i] <= 0.001 and self.vel[i] >= -0.001:
                self.vel[i] = 0
            if self.vel[i] > 0.1 or self.vel[i] < -0.1:
                self.rot_center(abs(self.vel[i])*3);

            if self.vel[i] > 0: ff = -0.01
            elif self.vel[i] < 0: ff =  0.01
            else: ff = 0

            self.vel[i] += - self.vel[i]/100.0 + ff
            if self.vel[i] <= 0.001 and self.vel[i] >= -0.001:
                self.vel[i] = 0

            if self.pos[i] > limit[i]:
                self.pos[i] = limit[i]
                self.vel[i] = -self.vel[i] * 2.0/5.0
            elif self.pos[i] < 0:
                self.pos[i] = 0
                self.vel[i] = -self.vel[i] * 2.0/5.0
            self.pos[i] = self.pos[i] + self.vel[i]



# }}}
# {{{ CreatureBody
class CreatureBody(GeneralMovingBody):
    """ Everything a player needs to know."""
    def __init__(self, surface, size, type=1, showing=True):
        GeneralMovingBody.__init__(self,surface=surface,size=size,showing=True)

        if type==1:
            name = 'guy_'
            self.color = pygame.Color(0,100,230)
        elif type==2:
            name = 'guy2_'
            self.color = pygame.Color(255,0,0)
        elif type==3:
            name = 'computer'
            self.color = pygame.Color(0,255,0)

        self.guy_front_standing ,self.rect = load_image( name + "front_standing.bmp", self.scale)
        self.guy_back_standing  ,self.rect = load_image( name + "back_standing.bmp", self.scale)
        self.guy_right_standing ,self.rect = load_image( name + "right_standing.bmp", self.scale)
        self.guy_front_running1,self.rect  = load_image( name + "front_running1.bmp", self.scale)
        self.guy_front_running2,self.rect  = load_image( name + "front_running2.bmp", self.scale)
        self.guy_back_running1,self.rect   = load_image( name + "back_running1.bmp", self.scale)
        self.guy_back_running2,self.rect   = load_image( name + "back_running2.bmp", self.scale)
        self.guy_right_running1,self.rect  = load_image( name + "right_running1.bmp", self.scale)
        self.guy_right_running2,self.rect  = load_image( name + "right_running2.bmp", self.scale)

        self.guy_left_standing = pygame.transform.flip(self.guy_right_standing, True, False)
        self.guy_left_running1 = pygame.transform.flip(self.guy_right_running1, True, False)
        self.guy_left_running2 = pygame.transform.flip(self.guy_right_running2, True, False)

        self.initial_pos = [width/2.0, height/3.0 * type]
        self.reset()

        self.move_turn = math.floor(random.random()*100)
        self.is_contact = False
        self.standing_direction = 'front'

    def move(self, surface, field, time, cameraPos, goal_size):
        """ players colliding with the goals """
        self.collidingGoal(goal_size)
        """ stopping the player, if keyup """
        if self.stoppingx:
            self.vel[0] += - self.vel[0]/2.0
            self.acc[0] = 0
        if self.stoppingy:
            self.vel[1] += - self.vel[1]/2.0
            self.acc[1] = 0
        self.__newpos()
        if self.showing: self.__walk(time, cameraPos)
        """ draw indicators if player is outside visible area """
        if self.pos[1] + self.sizey < cameraPos[1]:
            pygame.draw.rect(surface, self.color, (self.pos[0]+self.sizex/2.0 - field.getBarWidth()/2.0, 0, field.getBarWidth(), 10))
        if self.pos[1] > cameraPos[1] + visible_height:
            pygame.draw.rect(surface, self.color, (self.pos[0]+self.sizex/2.0 - field.getBarWidth()/2.0, visible_height, field.getBarWidth(),-10))


    def __walk(self, time, cameraPos):
        """ Render (blit) approprate image depending on direction the player is facing. """
        gate_frequency = 50
        if abs(self.vel[1]) > abs(self.vel[0]):
            """ Vertical vel is higher: """
            if self.vel[1] > 0:
                self.standing_direction = 'front'
                if time % gate_frequency > gate_frequency/2.0:
                    self.renderImage(self.guy_front_running2, cameraPos)
                else:
                    self.renderImage(self.guy_front_running1, cameraPos)
            else:
                self.standing_direction = 'back'
                if time % gate_frequency > gate_frequency/2.0:
                    self.renderImage(self.guy_back_running2, cameraPos)
                else:
                    self.renderImage(self.guy_back_running1, cameraPos)
        elif self.vel[1] != 0 or self.vel[0] != 0:
            """ Horizontal vel is higher: """
            if self.vel[0] > 0:
                self.standing_direction = 'right'
                if time % gate_frequency > gate_frequency/2.0:
                    self.renderImage(self.guy_right_running2, cameraPos)
                else:
                    self.renderImage(self.guy_right_running1, cameraPos)
            else:
                self.standing_direction = 'left'
                if time % gate_frequency > gate_frequency/2.0:
                    self.renderImage(self.guy_left_running2, cameraPos)
                else:
                    self.renderImage(self.guy_left_running1, cameraPos)
        else:
            """ Standing: """
            if self.standing_direction == 'back':
                self.renderImage(self.guy_back_standing, cameraPos)
            elif self.standing_direction == 'right':
                self.renderImage(self.guy_right_standing, cameraPos)
            elif self.standing_direction == 'left':
                self.renderImage(self.guy_left_standing, cameraPos)
            else:
                self.renderImage(self.guy_front_standing, cameraPos)

    def __newpos(self):
        """ Update player's position """
        limit = [self.limitx, self.limity]
        for i in range(0,2):
            self.vel[i] = self.vel[i] + self.acc[i]
            if self.vel[i] <= 0.001 and self.vel[i] >= -0.001:
                self.vel[i] = 0
            self.vel_threshold = 6
            if   self.vel[i] >  self.vel_threshold: self.vel[i] =  self.vel_threshold
            elif self.vel[i] < -self.vel_threshold: self.vel[i] = -self.vel_threshold


            if self.pos[i] > limit[i]:
                self.pos[i] = limit[i]
                self.vel[i] = -self.vel[i] * 3.0/5.0
            elif self.pos[i] < 0:
                self.pos[i] = 0
                self.vel[i] = -self.vel[i] * 3.0/5.0
            self.pos[i] = self.pos[i] + self.vel[i]

# }}}
#{{{ CreatureBodyComputer 
class CreatureBodyComputer(CreatureBody):
    """ Everything about a computer creature."""
    def __init__(self, surface):
        GeneralMovingBody.__init__(self,surface=surface,size=[random.random()*30+20,random.random()*30+20],showing=True)
        self.type=3

        name = 'computer'

        self.guy_front_standing , self.rect = load_image( "computer.bmp", self.scale)
        self.guy_back_standing  , self.rect = load_image( "computer.bmp", self.scale)
        self.guy_right_standing , self.rect = load_image( "computer.bmp", self.scale)
        self.guy_front_running1 , self.rect = load_image( "computer.bmp", self.scale)
        self.guy_front_running2 , self.rect = load_image( "computer.bmp", self.scale)
        self.guy_back_running1  , self.rect = load_image( "computer.bmp", self.scale)
        self.guy_back_running2  , self.rect = load_image( "computer.bmp", self.scale)
        self.guy_right_running1 , self.rect = load_image( "computer.bmp", self.scale)
        self.guy_right_running2 , self.rect = load_image( "computer.bmp", self.scale)

        self.guy_left_standing = pygame.transform.flip(self.guy_right_standing, True, False)
        self.guy_left_running1 = pygame.transform.flip(self.guy_right_running1, True, False)
        self.guy_left_running2 = pygame.transform.flip(self.guy_right_running2, True, False)


        self.initial_pos = [width/2.0, height/3.0 * self.type]
        self.reset()

        self.move_turn = math.floor(random.random()*100)
        self.is_contact = False
        self.standing_direction = 'front'
# }}}
