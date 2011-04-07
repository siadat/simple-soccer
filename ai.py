import pygame
import random
import math
import general
import creature
class Ai:
    def __init__(self, player, goal1=None, goal2=None):
        if not isinstance(player, creature.Player):
            print("AI says: You should give me a Player object!")
            return

        self.player = player
        self.astar_size = [30,40]

        self.gate_freq = 1
        self.time = 0
        self.goal1 = goal1
        self.goal2 = goal2

    def do(self, state):
        if not isinstance(state, State):
            print("AI says: You should give me a State object!")
            return

        self.time += 1
        self.state = state

        blocked_rects = [self.goal1.rect, self.goal2.rect, self.state.player1.rect]
        self.astar = AStar(self.player.get_centre_pos(), self.state.ball.get_centre_pos(), self.astar_size, blocked_rects)

        path = self.astar.get_shortest_path()
        #for pos in path:
        #    general.drawCircle(general.surface, pygame.Color(0,0,0), pos, 20,0)

        #p = self.go_to(path[0])
        
        self.player.relax = 1 - 2 * abs(1.0 * self.player.get_centre_pos()[1] / general.height - 0.5)

        if len(path) >= 2:
            self.go_to(general.Array(path[1]) - [0,0])
            #general.drawCircle(general.surface, pygame.Color(0,0,0), path[1], 4,0)


        #self.astar.draw_grid()
        #self.astar.draw_blocks()
        #self.go_to(general.Array(state.ball.get_centre_pos()) - [0,20])

        ## SHOOT:
        if self.state.ball.get_centre_pos()[1] < general.height - 30:
            if self.state.ball.get_centre_pos()[1] - self.player.get_centre_pos()[1] > 5 :
                self.state.ball.getShooted(self.player, 1)

        #mouse_pos = pygame.mouse.get_centre_pos()
        #self.go_to(general.Array(mouse_pos) + general.cameraPos )
        #print astar.to_node_pos(player.get_centre_pos()) 
        ## Assumption: player = player2
        #if state.what_area_player2 == [True,False]:
        #    self.player.acc = [0,0.02]
        #elif state.what_area_player2 == [True,True]:
        #    self.player.acc = [0,0]
        #elif state.what_area_player2 == [False,True]:
        #    self.player.acc = [0,-0.01]

    def run_to_back_of_the_ball():
        pass

    def go_to(self, pos):
        player_pos = self.player.get_centre_pos()
        dist = general.distance(player_pos, pos)

        if dist < 10:
            ## We're there!
            self.player.vel = [0,0]
            self.player.acc = [0,0]
            self.gate_freq  = 0
            return True

        max_dist = math.sqrt(general.width**2 + general.height**2)
        gate_freq = (1.0*dist/max_dist) * 1 + 1
        
        sin_old = math.sin((self.time)/180.0 * general.PI)
        self.time = self.time + 100 * gate_freq
        sin_new = math.sin((self.time)/180.0 * general.PI)

        if sin_old * sin_new <= 0:
            diff_x = pos[0] - player_pos[0]
            diff_y = pos[1] - player_pos[1]
            #self.player.vel[0] = diff_x / 20.0
            #self.player.vel[1] = diff_y / 20.0
            #return

            new_acc = [0,0]
            fire_acc = self.player.fire_acc
        
            if diff_x < 0:
                new_acc[0] = - fire_acc
            elif diff_x > 0:
                new_acc[0] =   fire_acc

            if diff_y < 0:
                new_acc[1] = - fire_acc
            elif diff_y > 0:
                new_acc[1] =   fire_acc

            self.player.acc[0] = new_acc[0]
            self.player.acc[1] = new_acc[1]

        #if dist < 20:
        #    self.player.vel_threshold = general.PLAYER_VEL_LIMIT * dist / 100.0
        #elif dist < 50:
        #    self.player.vel_threshold = general.PLAYER_VEL_LIMIT * dist / 80.0
        #elif dist < 100:
        #    self.player.vel_threshold = general.PLAYER_VEL_LIMIT * dist / 30.0
        #else:
        #    self.player.vel_threshold = general.PLAYER_VEL_LIMIT
        if self.player.relax > 0.5:
            if dist < 100:
                self.player.vel_threshold = general.PLAYER_VEL_LIMIT * dist / 25.0
        else:
            if dist < 100:
                self.player.vel_threshold = general.PLAYER_VEL_LIMIT * dist / 20.0

class AStar:
    def __init__(self, start_pixel_pos, target_pixel_pos, size, blocked_rects=[]):
        ## Number of nodes horizontally and vertically:
        self.sizex, self.sizey = size[0], size[1]
        self.unit_cost = 10
        self.unit_diagonal_cost = 14
        self.blocked_poses = []

        ## Create start and target nodes:
        start_node_pos  = self.to_node_pos(start_pixel_pos)
        target_node_pos = self.to_node_pos(target_pixel_pos)
        self.target_node = Node(pos=target_node_pos)
        self.start_node  = Node(pos=start_node_pos, g=0, h=self.calc_h(start_node_pos))

        #self.create_all_nodes() #[None] * (self.sizex * self.sizey)
        self.openlist   = []
        self.all_nodes = {}

        self.rects_to_poses(blocked_rects)
        if not (self.start_node.pos in self.blocked_poses):
            self.openlist.append(self.start_node)
        self.closedlist = []

    def rects_to_poses(self, rects):
        for rect in rects:
            topleft     = self.to_node_pos(rect.topleft)
            bottomright = self.to_node_pos(rect.bottomright)
            width  = int(abs(topleft[0] - bottomright[0]))
            height = int(abs(topleft[1] - bottomright[1]))
            for y in xrange(0, height+1):
                for x in xrange(0, width+1):
                    self.blocked_poses.append([topleft[0]+x,topleft[1]+y])

    def to_node_pos(self, pixel_pos):
        return [math.floor(self.sizex * (pixel_pos[0] / general.width )),
                math.floor(self.sizey * (pixel_pos[1] / general.height))]

    def to_pixel_pos(self, node_pos):
        return [1.0 * general.width  * node_pos[0] / self.sizex + 1.0 * (general.width/self.sizex)/2.0,
                1.0 * general.height * node_pos[1] / self.sizey + 1.0 * (general.height/self.sizey)/2.0]

    def draw_blocks(self):
        for node in self.blocked_poses:
            x = (1.0 * node[0]/self.sizex) * general.width  + 1.0 * general.width /self.sizex/2.0
            y = (1.0 * node[1]/self.sizey) * general.height + 1.0 * general.height/self.sizey/2.0
            general.drawCircle(general.surface, pygame.Color(0,0,0), [x,y], 5,0)

    def draw_grid(self):
        for i in xrange(0, self.sizex):
            x = (1.0 * i/self.sizex) * general.width
            general.drawLine(general.surface, pygame.Color(0,0,0), [x,0], [x,general.height])
        for i in xrange(0, self.sizey):
            y = (1.0 * i/self.sizey) * general.height
            general.drawLine(general.surface, pygame.Color(0,0,0), [0,y], [general.width,y])

    #def create_all_nodes(self):
    #    all_poses = [[x,y] for y in xrange(0,self.sizey) for x in xrange(0,self.sizex) ]
    #    self.all_nodes = [Node(pos=pos, g=0, h=self.calc_h(pos)) for pos in all_poses]

    def get_node(self, pos):
        pos_tuple = tuple(pos)
        pos_list  = list(pos)
        if not self.all_nodes.has_key(pos_tuple):
            self.all_nodes[pos_tuple] = Node(pos=pos_list, g=0, h=self.calc_h(pos_list))
        return self.all_nodes[pos_tuple]

    def get_adjacents(self, node):
        ret = []
        for y in xrange(int(node.pos[1]-1), int(node.pos[1]+1+1)):
            for x in xrange(int(node.pos[0]-1), int(node.pos[0]+1+1)):
                if not (x == node.pos[0] and y == node.pos[1]) and (x >= 0 and y >= 0) and (x < self.sizex and y < self.sizey) and not ([x,y] in self.blocked_poses):
                    adj_node = self.get_node([x,y])
                    if not (x == node.pos[0] or y == node.pos[1]):
                        adj_node.diagonal = True
                    ret.append(adj_node)
        return ret

    def get_astar_paths(self):
        path = []

        if self.target_node.pos in self.blocked_poses:
            return path
        while len(self.openlist) > 0:
            min_f = -1
            next_node = None
            for node in self.openlist:
                if node.f < min_f or min_f == -1:
                    next_node = node
                    min_f = node.f

            if next_node is None:
                print("node is None")
                return path

            self.openlist.remove(next_node)
            self.closedlist.append(next_node)

            for node in self.get_adjacents(next_node):
                if node in self.closedlist:
                    continue
                if not (node in self.openlist):
                    node.parent = next_node
                    node.g = node.parent.g
                    if node.diagonal: node.g += self.unit_diagonal_cost
                    else: node.g += self.unit_cost
                    node.f = node.g + node.h
                    self.openlist.append(node)
                else:
                    new_cost = next_node.g
                    if node.diagonal: new_cost += self.unit_diagonal_cost
                    else: new_cost += self.unit_cost
                    if node.g > new_cost:
                        node.parent = next_node
                        node.g = new_cost
                        node.f = node.g + node.h

            path.append(next_node)
            if next_node.pos == self.target_node.pos:
                return path
        return path

    def get_shortest_path(self):
        paths = self.get_astar_paths()
        if paths == []:
            return []
        node = paths.pop()
        shortest_path = []
        while node != None:
            shortest_path.append(self.to_pixel_pos(node.pos))
            node = node.parent
        shortest_path.reverse()
        return shortest_path

    def draw_path(self, path, node):
        if node == None:
            return path
        else:
            path.append(node)
            #general.drawCircle(general.surface, pygame.Color(255,0,0), self.to_pixel_pos(node.pos), 5,0)
            #self.draw_path(node.parent)

    def calc_f(self, node):
        node.f = node.g + node.h
        return node.f

    def calc_h(self, node_pos):
        h = self.unit_cost * (general.diff(node_pos[0], self.target_node.pos[0]) +\
                              general.diff(node_pos[1], self.target_node.pos[1]) )

        #xDistance = abs(node_pos[0]-self.target_node.pos[0])
        #yDistance = abs(node_pos[1]-self.target_node.pos[1])
        #if xDistance > yDistance:
        #     h = 14*yDistance + 10*(xDistance-yDistance)
        #else:
        #     h = 14*xDistance + 10*(yDistance-xDistance)

        #print node_pos, self.target_node.pos, ret
        return h

class Node(object):
    def __init__(self, pos, g=0, h=0 ):
        self.pos = pos
        self.parent = None
        self.diagonal = False
        self.h = h
        self.g = g
        self.f = self.h + self.g

# {{{

class State:
    def __init__(self, player1, player2, ball):
        self.player1 = player1
        self.player2 = player2
        self.ball = ball
        self.update()

    def update(self):
        ## distances:
        self.players_dist      = self.distance(self.player1, self.player2)
        self.player1_ball_dist = self.distance(self.player1, self.ball)
        self.player2_ball_dist = self.distance(self.player2, self.ball)

        ## relative velocities:
        self.players_relvel = self.distance(self.player1, self.player2)
        self.player1_ball_relvel = self.distance(self.player1, self.ball)
        self.player2_ball_relvel = self.distance(self.player2, self.ball)

        ## check in what area of the field each creature is:
        area_size = general.Array([general.width, general.height/2.0]) * general.global_zoom
        self.areas = [0,0]
        self.areas[0] = pygame.Rect([0,0], area_size)
        self.areas[1] = pygame.Rect(general.Array([0, general.height/2.0]) * general.global_zoom, area_size)

        self.what_area_player1 = self.is_in_area(self.player1, self.areas)
        self.what_area_player2 = self.is_in_area(self.player2, self.areas)
        self.what_area_ball    = self.is_in_area(self.ball, self.areas)

    def distance(self, creature1, creature2):
        return general.distance(creature1.get_centre_pos(), creature2.get_centre_pos())
    
    def relative_velocity(self, creature1, creature2):
        rel_vel[0] = creature1.vel[0] - creature2.vel[0]
        rel_vel[1] = creature1.vel[1] - creature2.vel[1]
        return sqrt(rel_vel[0]**2 + rel_vel[1]**2)

    def is_in_area(self, creature, rects_array):
        ## Problem: creature might overlap with more than one rect
        return [rect.colliderect(creature.rect)==True for rect in rects_array]
# }}}
