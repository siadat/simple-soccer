# {{{ Imports
import pygame, os
import random
import math
from pygame.locals import *
from general import *
import general #import *
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
    def isEquals(self): return self.__pygame_event.key == pygame.K_EQUALS;
    def isMinus(self): return self.__pygame_event.key == pygame.K_MINUS;
    def isPeriod(self): return self.__pygame_event.key == pygame.K_PERIOD;
    def isSlash(self): return self.__pygame_event.key == pygame.K_SLASH;
    def isComma(self): return self.__pygame_event.key == pygame.K_COMMA;
    def isBackquote(self): return self.__pygame_event.key == pygame.K_BACKQUOTE;
    def isOne(self): return self.__pygame_event.key == pygame.K_1;
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
        ## There's no self.pos. See set_pos() and get_pos()
        self._float_pos = [0, 0]

        self.initial_centre_pos = [width/2.0, height/2.0]
        self.showing = showing

        self.stoppingx = False
        self.stoppingy = False

        self.color     = pygame.Color(0,0,1)
        self.happiness = 0.0
        self.wealth = 0.0
        self.health = 0.0
        self.age    = 0.0
        self.angle  = 0.0
        self.fire_acc = 0.01
        self.mass = 1.0

    def set_pos(self, pos):
        self._float_pos = pos
        self.rect.move_ip(pos[0] - self.rect.left, pos[1] - self.rect.top)

    def get_pos(self):
        return [self._float_pos[0], self._float_pos[1]]

    def reset(self):
        self.set_pos([self.initial_centre_pos[0] - self.sizex/2.0, self.initial_centre_pos[1] - self.sizey/2.0])
        self.vel = [0,0]
        self.acc = [0,0]

    def renderImage(self, image, cameraPos):
        pos = self.get_pos()
        pos = [pos[0] - cameraPos[0], pos[1] - cameraPos[1]]
        global_zoom = general.global_zoom
        if global_zoom != 1: 
            size = image.get_size()
            image = pygame.transform.scale(image, (Array(size) * global_zoom).int())
            pos = Array(pos) * global_zoom
        self.surface.blit(image, pos)
        self.drawCoordinates()

    def getCentre(self):
        """ Get the position of the centre of the body, given the position of topleft. """
        pos = self.get_pos()
        return [pos[0] + self.sizex/2.0, pos[1] + self.sizey/2.0]

    def collidingGoal(self, goal):
        goal_size = goal.image.get_size()
        ## the goal's shape can be deconstructed into 3 rects.
        """ """
        pos = self.get_pos()
        self_right = pos[0] + self.sizex
        self_left  = pos[0]
        self_top    = pos[1]
        self_bottom = pos[1] + self.sizey

        goal_left  = goal.get_left_rect()
        goal_right = goal.get_right_rect()
        goal_back = goal.get_back_rect()

        if self.rect.colliderect(goal_back):
            line_top    = goal_back.top
            line_bottom = goal_back.bottom
            safety_dist = abs(self.vel[1]) + self.sizey * 0.3
            self.vel[1] = - self.vel[1]
            if diff(self_top, line_bottom) < diff(self_bottom, line_top):
                pos[1] = line_top + (safety_dist)
            else:
                pos[1] = line_bottom - (self.sizey + safety_dist)
            self.set_pos(pos)
            return

        safety_dist = abs(self.vel[0] * 2)
        if self.rect.colliderect(goal_left):
            line_left  = goal_left.left
            line_right = goal_left.right
            self.vel[0] = - self.vel[0]
            if diff(self_right, line_left) < diff(self_left, line_right):
                pos[0] = line_left  - (self.sizex + safety_dist)
            else:
                pos[0] = line_right + (safety_dist)
            self.set_pos(pos)
            return

        if self.rect.colliderect(goal_right):
            line_left  = goal_right.left
            line_right = goal_right.right
            self.vel[0] = - self.vel[0]
            if diff(self_right, line_left) < diff(self_left, line_right):
                pos[0] = line_left -  (self.sizex + safety_dist)
            else:
                pos[0] = line_right + (safety_dist)
            self.set_pos(pos)
            return



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

    def getShooted(self, kicker, power=1):
        """ Ball is shooted by kicker. """
        pos = self.get_pos()

        kicker_pos = kicker.get_pos()
        kicker_centre = kicker.getCentre()
        kicker_centre = Array(kicker_pos) + [kicker.sizex/2.0, kicker.sizey/2.0]
        dist = distance ( kicker_centre, Array(pos) + [self.sizex/2.0, self.sizey/2.0] )
        user_touch_dist = kicker.sizex/2 + self.sizex/2
        shoot_dist = user_touch_dist + 40
        if dist < shoot_dist:
            new_vel_0 = 2 * (self.vel[0] * (self.mass - kicker.mass) + 2 * kicker.mass * (pos[0]+self.sizex/2 - kicker_centre[0]) ) / (self.mass + kicker.mass)
            new_vel_1 = 2 * (self.vel[1] * (self.mass - kicker.mass) + 2 * kicker.mass * (pos[1]+self.sizey/2 - kicker_centre[1]) ) / (self.mass + kicker.mass)
            new_vel_size = math.sqrt( new_vel_0 ** 2 + new_vel_1 ** 2 )
            new_vel_0 = power * 300 * (new_vel_0 / new_vel_size) / dist
            new_vel_1 = power * 300 * (new_vel_1 / new_vel_size) / dist
            self.vel[0] = new_vel_0
            self.vel[1] = new_vel_1
            self.clockwise_spin = not self.clockwise_spin 

            ball_centre = self.getCentre()
            player_centre = kicker.getCentre()
            drawLine(self.surface, self.color, ball_centre, player_centre)


    def getKicked(self, kicker):
        """ Ball is kicked by the kicker. """
        pos = self.get_pos()
        kicker_pos = kicker.get_pos()
        dist = distance ( Array(kicker_pos) + [kicker.sizex/2.0, kicker.sizey/2.0], \
                          Array(pos) + [self.sizex/2, self.sizey/2] )
        user_touch_dist = kicker.sizex/2 + self.sizex/2
        if dist < user_touch_dist:
            self.is_under_player = True
            self.vel[0] = 2 * (self.vel[0] * (self.mass - kicker.mass) + 2 * kicker.mass * kicker.vel[0]) / (self.mass + kicker.mass)
            self.vel[1] = 2 * (self.vel[1] * (self.mass - kicker.mass) + 2 * kicker.mass * kicker.vel[1]) / (self.mass + kicker.mass)
            
            if self.vel == [0,0] and self.acc == [0,0]:
                scale = 1
                if self.clockwise_spin == True:
                    scale = -1
                self.vel = [random.random()*scale, random.random()*scale]
            else:
                self.clockwise_spin = not self.clockwise_spin 


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
        
        self.move_turn = math.floor(random.random()*100)
        self.is_contact = False
        self.clockwise_spin = False
        self.radius = radius
        
        rand = 0
        self.initial_centre_pos = [
                width/2.0   + random.random()*rand*2 - rand,
                height/2.0  + random.random()*rand*2 - rand
                ]
        self.reset()
        self.vel = [0,0]

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
        pos = self.get_pos()
        for i in range(0,2):
            if self.vel[i] <= 0.001 and self.vel[i] >= -0.001:
                self.vel[i] = 0
            if self.vel[i] > 0.1 or self.vel[i] < -0.1:
                self.rot_center(abs(self.vel[i])*4);

            if self.vel[i] > 0: ff = -0.01
            elif self.vel[i] < 0: ff =  0.01
            else: ff = 0

            self.vel[i] += - self.vel[i]/100.0 + ff
            if self.vel[i] <= 0.001 and self.vel[i] >= -0.001:
                self.vel[i] = 0

            if pos[i] > limit[i]:
                pos[i] = limit[i]
                self.vel[i] = -self.vel[i] * 4.0/5.0
            elif pos[i] < 0:
                pos[i] = 0
                self.vel[i] = -self.vel[i] * 4.0/5.0

            pos[i] = pos[i] + self.vel[i]
        self.set_pos(pos)



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

        self.initial_centre_pos = [width/2.0, height/3.0 * type]
        self.reset()

        self.move_turn = math.floor(random.random()*100)
        self.is_contact = False
        self.standing_direction = 'front'

    def move(self, surface, field, time, cameraPos, goal_size):
        """ stopping the player, if keyup """
        if self.stoppingx:
            self.vel[0] += - self.vel[0]/15.0
            self.acc[0] = 0
        if self.stoppingy:
            self.vel[1] += - self.vel[1]/15.0
            self.acc[1] = 0
        self.__newpos()
        if self.showing: self.__walk(time, cameraPos)
        """ draw indicators if player is outside visible area """
        pos = self.get_pos()
        vis = general.getVisibleSize()
        if pos[1] + self.sizey < cameraPos[1]:
            # marker will always be visible (limited to visible area from camera)
            pos[0] = general.hardlimit(pos[0], cameraPos[0], cameraPos[0] + vis[0] - self.sizex)
            topleft = [pos[0]+self.sizex/2.0 - field.getBarWidth()/2.0 - cameraPos[0], 0]
            topleft = Array(topleft) * general.global_zoom

            size    = [field.getBarWidth(), 10]
            rect = pygame.Rect(topleft, size)
            pygame.draw.rect(surface, self.color, rect)
        elif pos[1] > cameraPos[1] + vis[1]:
            pos[0] = general.hardlimit(pos[0], cameraPos[0], cameraPos[0] + vis[0] - self.sizex)
            topleft = [pos[0]+self.sizex/2.0 - field.getBarWidth()/2.0 - cameraPos[0], vis[1]]
            topleft = Array(topleft) * general.global_zoom
            size    = [field.getBarWidth(),-10]
            rect = pygame.Rect(topleft, size)
            pygame.draw.rect(surface, self.color, rect)
        # because pos was overwritten, get it again:
        pos = self.get_pos()
        if pos[0] + self.sizex < cameraPos[0]:
            pos[1] = general.hardlimit(pos[1], cameraPos[1], cameraPos[1] + vis[1] - self.sizey)
            topleft = [0, pos[1]+self.sizey/2.0 - field.getBarWidth()/2.0 -cameraPos[1]]
            topleft = Array(topleft) * general.global_zoom
            size = [10, field.getBarWidth()]
            rect = pygame.Rect(topleft, size)
            pygame.draw.rect(surface, self.color, rect)
        elif pos[0] > cameraPos[0] + vis[0]:
            pos[1] = general.hardlimit(pos[1], cameraPos[1], cameraPos[1] + vis[1] - self.sizey)
            topleft = [vis[0], pos[1]+self.sizey/2.0 - field.getBarWidth()/2.0 -cameraPos[1]]
            topleft = Array(topleft) * general.global_zoom
            size = [-10, field.getBarWidth()]
            rect = pygame.Rect(topleft, size)
            pygame.draw.rect(surface, self.color, rect)

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
        pos = self.get_pos()
        for i in range(0,2):
            self.vel[i] = self.vel[i] + self.acc[i]
            if self.vel[i] <= 0.001 and self.vel[i] >= -0.001:
                self.vel[i] = 0
            self.vel_threshold = 1.2
            if   self.vel[i] >  self.vel_threshold: self.vel[i] =  self.vel_threshold
            elif self.vel[i] < -self.vel_threshold: self.vel[i] = -self.vel_threshold


            if pos[i] > limit[i]:
                pos[i] = limit[i]
                self.vel[i] = -self.vel[i] * 3.0/5.0
            elif pos[i] < 0:
                pos[i] = 0
                self.vel[i] = -self.vel[i] * 3.0/5.0
            pos[i] = pos[i] + self.vel[i]
        self.set_pos(pos)

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


        self.initial_centre_pos = [width/2.0, height/3.0 * self.type]
        self.reset()

        self.move_turn = math.floor(random.random()*100)
        self.is_contact = False
        self.standing_direction = 'front'
# }}}
