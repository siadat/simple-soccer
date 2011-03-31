import pygame, sys, os
from pygame.locals import *
import math
import copy

""" Public variables: """
surface = None
width  = 200.0 * 3
height = 200.0 * 4
visible_width  = width - 100
visible_height = height - 100
cameraPos = [0, 0]
global_zoom = 1
debug = not not False
PI = 3.1415
PLAYER_VEL_LIMIT = 2.2

def getVisibleSize():
    vis_x = visible_width  / global_zoom
    vis_y = visible_height / global_zoom
    if vis_x > width:  vis_x = width
    if vis_y > height: vis_y = height
    return [vis_x, vis_y]

class Array(list):
    ## cool class: maintains chainability
    def __add__(self, other):
        if isinstance(other, list):
            if len(other) != len(self): print "arrays must be the same size"; exit
            for i in xrange(len(self)):
                self[i] += other[i]
            return self
        else:
            return Array([other + x for x in self])

    def __sub__(self, other):
        if isinstance(other, list):
            if len(other) != len(self): print "arrays must be the same size"; exit
            for i in xrange(len(self)):
                self[i] -= other[i]
            return self
        else:
            return Array([other - x for x in self])

    def __mul__(self, other):
        if isinstance(other, list):
            if len(other) != len(self): print "arrays must be the same size"; exit
            for i in xrange(len(self)):
                self[i] *= other[i]
            return self
        else:
            return Array([other * x for x in self])

    def __div__(self, other):
        if isinstance(other, list):
            if len(other) != len(self): print "arrays must be the same size"; exit
            for i in xrange(len(self)):
                self[i] /= other[i]
            return self
        else:
            return Array([other / x for x in self])

    def int(self):
        return Array([int(x) for x in self])

def hardlimit(value, uplimit, downlimit):
    if downlimit > uplimit:
        tmp = uplimit
        uplimit = downlimit
        downlimit = tmp
    if value > uplimit:
        return uplimit
    elif value < downlimit:
        return downlimit
    else:
        return value

def load_image(filepath, scale=None, colorkey=None):
    """ Load an image. """
    fullname = os.path.join(os.path.dirname(sys.argv[0]), 'images', filepath)
    try:
        image = pygame.image.load(fullname)
        if scale is not None:
            image = pygame.transform.scale(image, scale)
    except pygame.error, message:
        print 'Cannot load image:', filepath
        raise SystemExit, message
    """ convert per pixel """
    image = image.convert_alpha()
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0,0))
        image.set_colorkey(colorkey, RLEACCEL)
    return image, image.get_rect()

def distance(pos1, pos2):
    """ Calculate the scalar distance between two points. """
    return math.sqrt( sum ( ( (pos1[0]-pos2[0])**2 , (pos1[1]-pos2[1])**2 ) ) )

def diff(value1, value2):
    """ Calculate the absolute difference between two numbers. """
    return abs(value1 - value2);

def drawLine(surface, color, startPos, endPos):
    """ Draw a line given the end points, a color and a surface. """
    startPos = copy.copy(startPos)
    endPos = copy.copy(endPos)
    startPos[0] = (startPos[0] - cameraPos[0]) * global_zoom
    startPos[1] = (startPos[1] - cameraPos[1]) * global_zoom
    endPos[0] = (endPos[0] - cameraPos[0]) * global_zoom
    endPos[1] = (endPos[1] - cameraPos[1]) * global_zoom
    pygame.draw.line( surface, color, startPos, endPos)

def drawCircle(surface, color, centrePos, radius, width=1):
    """ Draw a line given the end points, a color and a surface. """
    centrePos = copy.copy(centrePos)
    centrePos[0] = int((centrePos[0] - cameraPos[0]) * global_zoom)
    centrePos[1] = int((centrePos[1] - cameraPos[1]) * global_zoom)
    radius = int(radius * global_zoom)
    pygame.draw.circle( surface, color, centrePos, radius, width)

def drawRect(surface, color, startPos, endPos):
    """ Draw a line given the end points, a color and a surface. """
    startPos = copy.copy(startPos)
    endPos = copy.copy(endPos)
    startPos[0] = (startPos[0] - cameraPos[0]) * global_zoom
    startPos[1] = (startPos[1] - cameraPos[1]) * global_zoom
    endPos[0] = (endPos[0] - cameraPos[0]) * global_zoom
    endPos[1] = (endPos[1] - cameraPos[1]) * global_zoom
    pygame.draw.rect( surface, color, pygame.Rect(startPos[0], startPos[1], endPos[0]-startPos[0], endPos[1]-startPos[1]))

def moveCamera(ball):
    """ Move the camera relative to the ball's position and vel and acc. """
    pos = ball.getCentre()
    vis = getVisibleSize()
    cameraPos[0] = pos[0] - vis[0]/2.0
    cameraPos[1] = pos[1] - vis[1]/2.0
    #global global_zoom
    #global_zoom = 1 + abs(cameraPos[1]/3000.0)
    
    if cameraPos[0] < 0: cameraPos[0] = 0
    if cameraPos[0] > width-vis[0]: cameraPos[0] = width-vis[0]

    if cameraPos[1] < 0: cameraPos[1] = 0
    if cameraPos[1] > height-vis[1]: cameraPos[1] = height-vis[1]
