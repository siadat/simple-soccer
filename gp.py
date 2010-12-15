import math
import random
import time
from general import *

functions      = 'sum', 'sub', 'mult', 'div', 'sqrt', 'pow', 'lt', 'mt', 'eq', 'rand', 'neg', 'sin', 'cos' #, 'floor', 'ceiling', 'log'
functions_args = 2,     2,     2,      2,     1,      2,     2,    2,    2,    0,      1,     1,     1

nbr_functions  = len(functions_args)
terminals      ='time',\
		'ball_posx', 'ball_posy', 'ball_velx', 'ball_vely',\
		'p1_posx', 'p1_posy', 'p1_velx', 'p1_vely', 'p1_energy',\
		'p2_posx', 'p2_posy', 'p2_velx', 'p2_vely', 'p2_energy',\
		'p1p2_dist', 'p1ball_dist', 'p2ball_dist'

nbr_terminals = len(terminals)


class Terminals:
	def __init__(self,
			time,
			ball_pos, ball_vel,
			p1_pos, p1_vel, p1_energy,
			p2_pos, p2_vel, p2_energy):
		self.time = time
		self.ball_posx = ball_pos[0]
		self.ball_posy = ball_pos[1]
		self.ball_velx = ball_vel[0]
		self.ball_vely = ball_vel[1]
		
		self.p1_posx   = p1_pos[0]
		self.p1_posy   = p1_pos[1]
		self.p1_velx   = p1_vel[0]
		self.p1_vely   = p1_vel[1]
		self.p1_energy = p1_energy

		self.p2_posx   = p2_pos[0]
		self.p2_posy   = p2_pos[1]
		self.p2_velx   = p2_vel[0]
		self.p2_vely   = p2_vel[1]
		self.p2_energy = p2_energy

		self.p1ball_dist = distance(ball_pos,p1_pos)
		self.p2ball_dist = distance(ball_pos,p2_pos)
		self.p1p2_dist   = distance(p1_pos,p2_pos)

#--------------------------------------------------------------------

class TerminalNode:
	def __init__(self, parent, terminal_str):
		self.id           = 0
		self.is_terminal  = True
		self.parent       = parent
		self.terminal_str = terminal_str
		self.child        = None
		#if self.terminal_str == 'cont':

class FunctionNode:
	def __init__(self, parent, func_str):
		self.id          = 0
		self.is_terminal = False
		self.parent      = parent
		self.func_str    = func_str
		self.child       = []

#--------------------------------------------------------------------

def do_func(func_str, x=None):
	threshold = 10


	if x is not None:
		for i in range(len(x)):
			if x[i] > 10: x[i] = 10
			if x[i] <-10: x[i] =-10


		if func_str=='pow':
			if abs(x[0])<0.0001 or abs(x[1])<0.0001:
				return 0
			if x[0]<0 and x[1] != int(x[1]):
				return 0
		elif func_str=='div':
			if abs(x[1]) < .0001:
				if   x[0]>0: return  threshold
				elif x[0]<0: return -threshold
				else: return 0
		#if func_str=='pow' or func_str=='sqrt':
		#	print x
	
	result = {
		'sum'  : lambda x : x[0] + x[1],
		'sub'  : lambda x : x[0] - x[1],
		'mult' : lambda x : x[0] * x[1],
		'div'  : lambda x : x[0] / x[1],
		'sqrt' : lambda x : math.sqrt(abs(x[0])),
		'pow'  : lambda x : x[0] **x[1],
		'lt'   : lambda x : int (x[0] < x[1]),
		'mt'   : lambda x : int (x[0] > x[1]),
		'eq'   : lambda x : int (x[0] ==x[1]),
		'rand' : lambda x : random.random(),
		'neg'  : lambda x : -x[0],
		'sin'  : lambda x : math.sin(2*math.pi * x[0]),
		'cos'  : lambda x : math.cos(2*math.pi * x[0])
	}[func_str](x)


	

	result = result * threshold
	
	#if   result > threshold: result = threshold
	#elif result <-threshold: result =-threshold
	return result


#def do_func2(func_str, x=None, y=None):
#	result = [0,0]	
#	if x is None:	result = [ do_func( func_str ) , do_func( func_str ) ]
#	elif y is None:	result = [ do_func( func_str, [x[0],None] ) , do_func( func_str, [x[1],None] ) ]
#	return result

def get_terminal(terminal_str, terminal_values):
	terminal = {
		'time'      : lambda : terminal_values.time,
		'ball_posx' : lambda : terminal_values.ball_posx,
		'ball_posy' : lambda : terminal_values.ball_posy,
		'ball_velx' : lambda : terminal_values.ball_velx,
		'ball_vely' : lambda : terminal_values.ball_vely,

		'p1_posx'   : lambda : terminal_values.p1_posx,
		'p1_posy'   : lambda : terminal_values.p1_posy,
		'p1_velx'   : lambda : terminal_values.p1_velx,
		'p1_vely'   : lambda : terminal_values.p1_vely,
		'p1_energy' : lambda : terminal_values.p1_energy,

		'p2_posx'   : lambda : terminal_values.p2_posx,
		'p2_posy'   : lambda : terminal_values.p2_posy,
		'p2_velx'   : lambda : terminal_values.p2_velx,
		'p2_vely'   : lambda : terminal_values.p2_vely,
		'p2_energy' : lambda : terminal_values.p2_energy,
		'p1p2_dist' : lambda : terminal_values.p1p2_dist,
		'p1ball_dist': lambda : terminal_values.p1ball_dist,
		'p2ball_dist': lambda : terminal_values.p2ball_dist
	}[terminal_str]()
	return terminal

#--------------------------------------------------------------------




class Individual:
	def __init__(self):
		self.node_counter  = 0
		self.nbr_of_nodes1 = 0
		self.nbr_of_nodes2 = 0
		self.fitness = 0
		
		self.rootNode_accx = self.create_a_gp(None,0)
		self.nbr_of_nodes1 = self.node_counter
		self.node_counter = 0
		#print ',,,,'

		self.rootNode_accy = self.create_a_gp(None,0)
		self.nbr_of_nodes2 = self.node_counter
		self.node_counter = 0

	def __cmp__ (self, other):
		return cmp(self.fitness, other.fitness)
	
	def create_a_gp(self, parent, depth=0, to_print=False):
		self.node_counter += 1
		intent = ""
		if (random.random() > 0.9 or depth > 8) and depth>=2:
			is_func = False
			chosen = int (random.random() * nbr_terminals)
			terminal_node = TerminalNode(parent, terminals[chosen])
			terminal_node.id = self.node_counter
			
			if to_print:
				for i in range(depth):
					intent += " "
				print intent + "T: " + str(terminal_node.id) + " " + terminals[chosen]
			depth -= 1
			
			return terminal_node
		else:
			is_func = True
			chosen = int (random.random() * nbr_functions)
			function_node = FunctionNode(parent, functions[chosen])
			function_node.id = self.node_counter

			nbr_args = functions_args[chosen]
			
			
			if to_print:
				for i in range(depth):
					intent += " "
				print intent + "F: " + str(function_node.id) + " " + functions[chosen]
			
			depth += 1
			
			for i in range(nbr_args):
				(function_node.child).append(self.create_a_gp(function_node, depth, to_print))
			
			return function_node


	def mutate(self):
		self.mutate_x()
		self.mutate_y()

	def mutate_x (self):
		current_node = self.rootNode_accx
		i = int ( random.random() * self.nbr_of_nodes1 ) + 1
		#print 'to be mutated===' + str(i)
		
		old_node = self.get_node(current_node, i)
		node = old_node
		
		#if node.parent is not None: node.parent.child.remove(node) # i.e. don't do anything if root node
		#print '--------------new-subtree..'
		#if node is None: print i
		parent = node.parent
		node = self.create_a_gp(parent)

		if old_node.parent is not None:
			old_node.parent.child.append(node)
			old_node.parent.child.remove(old_node) 
		else:
			#the root node is changed, ie all of the tree
			self.rootNode_accx = node
		
		#print '--------------NEW TREE:'
		self.node_counter = 0
		self.renumber_id(self.rootNode_accx)
		self.nbr_of_nodes1 = self.node_counter
		#self.print_tree(self.rootNode_accx)

		#---debug-only:
		#print 'number of nodes = ' + str(self.nbr_of_nodes1)
		#for i in range(1,self.nbr_of_nodes1+1):
		#	node = self.get_node(current_node, i)
		#	if node.is_terminal: print str(i) + '\tterminal'
		#	else: print str(i) + '\tfnuction'

	def mutate_y (self):
		current_node = self.rootNode_accy
		i = int ( random.random() * self.nbr_of_nodes2 ) + 1
		old_node = self.get_node(current_node, i)
		node = old_node

		#if node is None: print i
		parent = node.parent
		node = self.create_a_gp(parent)

		if old_node.parent is not None:
			old_node.parent.child.append(node)
			old_node.parent.child.remove(old_node) 
		else:
			self.rootNode_accy = node
		
		self.node_counter = 0
		self.renumber_id(self.rootNode_accy)
		self.nbr_of_nodes2 = self.node_counter


	def get_node(self, node, id):
		if node.id == id:
			return node
		if node.child is not None and len(node.child) > 0:
			for child in node.child:
				node = self.get_node(child, id)
				if node is not None: return node
		else:
			return None
	
	def renumber_id(self, node):
		self.node_counter += 1
		node.id = self.node_counter
		if node.child is not None and len(node.child) > 0:
			for child in node.child:
				self.renumber_id(child)

	def print_tree(self, node, depth=0):
		intent = ""
		if node.is_terminal:
			for i in range(depth):
				intent += " "
			print intent + "T: " + str(node.id) + ' ' + node.terminal_str
			depth -= 1
		else:
			for i in range(depth):
				intent += " "
			print intent + "F: " +str(node.id) + ' ' + node.func_str

			if node.child is not None and len(node.child) > 0:
				depth += 1
				for child in node.child:
					self.print_tree(child, depth)


class running_tree:
	def __init__(self, terminals):
		self.terminals = terminals

	def run_tree(self, node):
		if node.is_terminal:
			return get_terminal(node.terminal_str, self.terminals)
		else:
			x = None
			if len(node.child) > 0:
				x = list()
				for ch in node.child:
					x.append(self.run_tree(ch))
			return do_func(node.func_str, x)
#---------------------------------------------------------------------------------

