"""
Header: 

Name of File: p1_statespace.py
Other Files: p1_weather.py
Author: Tejvir Mann
Class: CS 540 
Description of Program: This program contains methods that are responsible for 
filling, emptying, transfering, and predicting all next possible moves(succ) for 
buckets filled with water. 
"""

# max = [5,7] #the capcities of the buckets  caps = capacities 
#  state = [0,0]  #how filled the buckets are at the start
# which = 0 #which jug, 0 or 1. 
# source = 0 #which jug is pouring
# dest = 0 #which jug is getting poured on. 

	#this function returns a copy of the state after one is filled. 
def fill(state, max, which):
	copy = state
	if which == 1: 
		copy = [state[0], max[1]]
	else: 
		copy = [max[0], state[1]]
	return copy

	#this function returns a copy of the state after on is emptied
def empty(state, max, which):
	copy = state
	if which == 1: 
		copy = [state[0], 0]
	else: 
		copy = [0, state[1]]
	return copy
	
	#this function transfers water from one bucket to another
def xfer(state, max, source, dest):
	copy = state 
	if source == 1: 
		maximum = max[0]
		current = copy[0]
		diff = maximum - current 
		if diff > copy[1]:
			copy[0] = copy[0] + copy[1]
			copy[1] = 0
		else:
			amount = copy[1] - diff
			copy[0] = max[0]
			copy[1] = copy[1] - amount
	else: 
		maximum = max[1]
		current = copy[1]
		diff = maximum - current 
		if diff > copy[0]:
			copy[1] = copy[1] + copy[0]
			copy[0] = 0
		else:
			amount = copy[0] - diff
			copy[1] = max[1]
			copy[0] = copy[0] - amount
	return copy 

	#this function 
def succ(state, max):
	
	e = fill(state, max, 1)
	f = empty(state, max, 1)
	g = xfer(state, max, 0, 1)
	h = fill(state, max, 0)
	i = empty(state, max, 0)
	j = xfer(state, max, 1, 0)
	final = [e, f, g, h, i, j]
	morefinal = []
	[morefinal.append(x) for x in final if x not in morefinal] 

	return morefinal

def main(): 
	print(succ(state, max))
main()
