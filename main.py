# {{{ Imports
import pygame, sys, os
from general import *
import random
from pygame.locals import *
from creature import *
#from gp import *
#from net import *
from field import *
# }}}

if not pygame.font:  print 'Warning, fonts disabled'
if not pygame.mixer: print 'Warning, sound disabled'

def creaturesTest(rootNode1_acc, rootNode2_acc, showing=False, time_length=None, playing=False, online=False):
    """ Run the simulation (e.g., game) with all the creatures (e.g., players and balls). """
    number_of_players = 2
    number_of_computer_creatures = 0
    number_of_balls = 1

    balls = list()
    players = list()
    computer_creature = list()

    if online: socket, isClient = tcp_connect(ip_address)

    if not playing:
        rootNode1_accx = rootNode1_acc[0]
        rootNode1_accy = rootNode1_acc[1]
        rootNode2_accx = rootNode2_acc[0]
        rootNode2_accy = rootNode2_acc[1]

    if showing: pygame.init()
    if showing: pygame.mouse.set_visible(False)
    
    if showing:
        window = pygame.display.set_mode( (int(visible_width), int(visible_height)), pygame.DOUBLEBUF)# , pygame.FULLSCREEN)
    else:
        window = pygame.display.set_mode((100,100))
    
    fitness1 = 0
    fitness2 = 0
    surface = None
    if showing:
        pygame.display.set_caption('Genetic Soccer')
        surface = pygame.display.get_surface()
        field = Field();

    for i in range(0,number_of_balls):
        balls.append(BallBody(surface=surface, radius=6, showing=showing))

    for i in range(0,number_of_players):
        players.append( CreatureBody(surface,(20,20),i+1, showing) )

    for i in range(0,number_of_computer_creatures):
        computer_creature.append( CreatureBodyComputer( surface=surface ) )

    if showing: clock = pygame.time.Clock()

    counter = 0

    while counter<time_length or time_length is None:
        """ Main loop of the simulation (e.g., game). """
        moveCamera(balls[0])
        stoppingx_event = False
        stoppingy_event = False
        new_key = False
        mouse_pos = pygame.mouse.get_pos()
        goal_size = field.getGoal1().get_size()

        if online:
            ball = balls[0]
            player1 = players[0]
            player2 = players[1]
            terminals0 = Terminals( counter, ball.pos, ball.vel, player1.pos, player1.vel, 1, [0,0],[0,0],1)
            terminals1 = Terminals( counter, ball.pos, ball.vel, [width - player2.pos[0], height - player2.pos[1]], [-player2.vel[0], -player2.vel[1]],   1, [0,0],[0,0],1) #width-players[1].pos[0],height-players[1].pos[1],    players[1].vel[0], players[1].vel[1],  1)

        if not playing:
            players[0].acc[0] = running_tree(terminals0).run_tree(rootNode1_accx)
            players[0].acc[1] = running_tree(terminals0).run_tree(rootNode1_accy)

            players[1].acc[0] = running_tree(terminals1).run_tree(rootNode2_accx)
            players[1].acc[1] = -running_tree(terminals1).run_tree(rootNode2_accy)
            
        if showing: clock.tick(120)

        counter += 1

        if showing:
            """ Background """
            if showing: field.blitBackground(surface)
            """ Keyboard events """
            input = pygame.event.get()
            for event in input:
                whatkey = Keyboard(event)
                if whatkey.isKEYDOWN():
                    if whatkey.isEscape():
                        sys.exit(0)
                    elif whatkey.isLeft():
                        players[0].fireLeft()
                    elif whatkey.isRight():
                        players[0].fireRight()
                    elif whatkey.isUp():
                        players[0].fireUp()
                    elif whatkey.isDown():
                        players[0].fireDown()
                    elif whatkey.isPeriod():
                        balls[0].getShooted(players[0])
                    elif whatkey.isA():
                        players[1].fireLeft()
                    elif whatkey.isD():
                        players[1].fireRight()
                    elif whatkey.isW():
                        players[1].fireUp()
                    elif whatkey.isS():
                        players[1].fireDown()
                    elif whatkey.isBackquote():
                        balls[0].getShooted(players[1])
                elif whatkey.isKEYUP():
                    if whatkey.isLeft() or whatkey.isRight():
                        players[0].stopLeftAndRight()
                    elif whatkey.isUp() or whatkey.isDown():
                        players[0].stopUpAndDown()
                    elif whatkey.isA() or whatkey.isD():
                        players[1].stopLeftAndRight()
                    elif whatkey.isW() or whatkey.isS():
                        players[1].stopUpAndDown()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    left, top = (x - 50 for x in event.pos)
                
                if whatkey.isKEYUP() or whatkey.isKEYDOWN():
                    new_key = True
            if online: net.updatePlayers(new_key, isClient, socket, players)

        
        for player in players:
            player.move(surface, field, counter, cameraPos=cameraPos, goal_size=goal_size)

        for ball in balls:
            """ All balls """
            ball_centre = ball.getCentre()
            
            fitness1 += 1000/distance(ball_centre, players[0].pos)
            fitness2 += 1000/distance(ball_centre, players[1].pos)

            ball.is_under_player = False
            # players colliding with the ball
            for player in players:
                ball.getKicked(player)
            # computer player colliding with the ball and the goal
            for cc in computer_creature:
                cc.collidingGoal(goal_size)
                ball.getKicked(cc)
                if debug:
                    print mouse_pos
                cc.acc = [ (random.random()-0.5)/5.0, (random.random()-0.5)/5.0]
                cc.move(surface, field, counter, cameraPos=cameraPos, goal_size=goal_size)

            # to the pipe (tirake darvaze):
            is_colliding_goal_pipe_top_right    = ( ball.vel[1] < 0 and (diff(ball_centre[1], goal_size[1]) < ball.radius)            and (diff(ball_centre[0], (width/2 + goal_size[0]/2)) < 3) )
            is_colliding_goal_pipe_top_left     = ( ball.vel[1] < 0 and (diff(ball_centre[1], goal_size[1]) < ball.radius)            and (diff(ball_centre[0], (width/2 - goal_size[0]/2)) < 3) )
            is_colliding_goal_pipe_bottom_right = ( ball.vel[1] > 0 and (diff(ball_centre[1], (height - goal_size[1])) < ball.radius) and (diff(ball_centre[0], (width/2 + goal_size[0]/2)) < 3) )
            is_colliding_goal_pipe_bottom_left  = ( ball.vel[1] > 0 and (diff(ball_centre[1], (height - goal_size[1])) < ball.radius) and (diff(ball_centre[0], (width/2 - goal_size[0]/2)) < 3) )

            if is_colliding_goal_pipe_top_right or is_colliding_goal_pipe_top_left or is_colliding_goal_pipe_bottom_right or is_colliding_goal_pipe_bottom_left:
                ball.vel[1] = - ball.vel[1]
            else:
                ball.collidingGoal(goal_size) 

            if (ball_centre[1] < goal_size[1] and abs(ball_centre[0] - width/2) < goal_size[0]/2 - 3) :
                fitness2 += 100
                field.score2+=1
                ball.reset()
                players[0].reset()
                players[1].reset()
                players[0].fire_acc += 0.01
                players[1].fire_acc += 0.01

                if showing: field.setMessage2()
            elif (ball_centre[1] > height - goal_size[1] and abs(ball_centre[0] - width/2) < goal_size[0]/2 - 3):
                fitness1 += 100
                field.score1+=1
                ball.reset()
                players[0].reset()
                players[1].reset()
                players[0].fire_acc += 0.01
                players[1].fire_acc += 0.01
                if showing: field.setMessage1()

            if showing:
                field.blitField(width=width, height=height, surface=surface, cameraPos=cameraPos)

            ball.move(counter,cameraPos=cameraPos)

        if debug: pygame.draw.rect(surface, pygame.Color(0,0,0), (0,0, visible_width,visible_height),1)
        if showing:pygame.display.flip()
    return (1.0 * fitness1/counter, 1.0 * fitness2/counter)
