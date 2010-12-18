import pygame, sys, os
from pygame.locals import *
import math

""" Public variables: """
width  = 200.0 * 3
height = 200.0 * 4
visible_width = width
visible_height = height - 100
cameraPos = [0, 0]
debug = not not False

def load_image(filepath, scale=None, colorkey=None):
    """ Load an image. """
    fullname = os.path.join('images', filepath)
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
    pygame.draw.line( surface, color,
            [startPos[0] - cameraPos[0], startPos[1] - cameraPos[1]],
            [endPos[0] - cameraPos[0], endPos[1] - cameraPos[1]])

def moveCamera(ball):
    """ Move the camera relative to the ball's position and vel and acc. """
    pos = ball.get_pos()
    if diff(cameraPos[1], pos[1]-visible_height/2.0) > 5:
        if cameraPos[1] > pos[1] - visible_height/2.0:
            cameraPos[1] = cameraPos[1] - abs(ball.vel[1]) - 1
        elif cameraPos[1] < pos[1] - visible_height/2.0:
            cameraPos[1] = cameraPos[1] + abs(ball.vel[1]) + 1


    cameraPos[1] = pos[1] - visible_height/2.0
    if cameraPos[1] < 0: cameraPos[1] = 0
    if cameraPos[1] > height-visible_height: cameraPos[1] = height-visible_height
