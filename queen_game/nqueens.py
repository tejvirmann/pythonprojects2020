'''
Name: nqueens.py
Author: Tejvir Mann
Class: CS 540
Professors: Zhu and Hobbes 
Function: This program is designed to take in a array
symbolizing a chessboard with queens, then output the steps 
to ensure to minimize the amount of queens that attack each other 
'''

import copy # imports 
import random


#this method returns a list of possible states
def succ(state, boulderX, boulderY):
	
	size = len(state)  #size
	state_copy = copy.deepcopy(state) #copy of state to be used
	succs = [] #array to store options
	l = 0 #length and width to move through the table 
	w = 0

	for i in state: #for the moves through l
		w = 0
		for j in state: #moves through w
			state_copy[l] = w 
			value = copy.deepcopy(state_copy)
			if value != state: #adds all possible options removing the option of 
				succs.append(value)  # a queen being where the boulder is 
				if (l == boulderX) and (w == boulderY):
					succs.remove(value)
			w += 1
		state_copy = copy.deepcopy(state)
		l += 1


	return succs # returns options

#this assigns an f value for each state
def f(state, boulderX, boulderY):
	conflicts = [] # this at the end should contain all the in danger queens
	row = 0;

	for i in range(len(state)): #this loop runs through the rows, checks 
		curr = state[i] #if there is another queen or a boulder.
		k = i+1
		for j in (range(len(state) - i - 1)):
			if k == boulderX and state[i] == boulderY: 
				k = k+1
				break

			if state[k] == state[i]:
				conflicts.append([i,state[i]]) # the one that is being tested on
				conflicts.append([k,state[k]]) # the one that was caught to have 

			k = k+1


	# the above diagonal check
	for i in range(len(state)): #runs through each column
		curr = state[i]
		k = i+1
		l = 1

		for j in (range(len(state) - i - 1)): #checks the diagonals of each queen
			if k == boulderX and state[i] + l == boulderY: #if diagonal boulder, move
	
				k = k+1
				l = l +1 #increments to next diagonal square
				break

			if state[k] == state[i] + l: #if diag queen
				
				conflicts.append([i,state[i]]) # the one that is being tested on
				conflicts.append([k,state[k]]) # the one that was caught to have 
			
			k = k+1
			l = l +1
	
	# the below diagonal check
	for i in range(len(state)): #goes through each column
		curr = state[i]
		k = i+1
		l = 1
		for j in (range(len(state) - i - 1)): #checks each diagonal square for each queen 
			if k == boulderX and state[i] - l == boulderY:
				
				l = l + 1
				k = k + 1 
				break  #if boulder is hit move to next

			if state[k] == state[i] - l: #if a queen is diag

				conflicts.append([i,state[i]]) # the one that is being tested on
				conflicts.append([k,state[k]]) # the one that was caught to have 

			l = l+1
			k = k +1

	f_conflicts = []
	[f_conflicts.append(x) for x in conflicts if x not in f_conflicts] #removes duplicates

	f = len(f_conflicts) #length of this array is f's value

	return f


#this method gets all of the possibilites 
#based off the current state 
#then it finds the one with the unique lowest f. 
#if there are multiple, then 'sort' and choose the smallest
#if you end up picking the current state, return None. 
def choose_next(curr, boulderX, boulderY):
	#calls succ with curr
	#picks the best out of curr based on f
	new_curr = []
 	lowest_f = 100;
 	current_f = 0;
 	tempp = 0;
	succs = succ(curr, boulderX, boulderY) 
	num_f = 0
	top_x = [] 
	end = []
    
	    #finds the lowest f
	for i in range(len(succs)):
	    	current_f = f(succs[i], boulderX, boulderY)
	    	if current_f < lowest_f:
	    		temp = copy.deepcopy(current_f)
	    		lowest_f = copy.deepcopy(temp)

	#gets the total amount of lowest fs
	for i in range(len(succs)):
		if current_f == lowest_f:
			num_f += 1

	#if there is only one lowest f, then return that one.
	if num_f == 1:
	    #gets the array corresponding to the lowest f
	    for i in range(len(succs)):
	    	current_f = f(succs[i], boulderX, boulderY)
	    	if current_f == lowest_f:
	    		new_curr = copy.deepcopy(succs[i])

	#otherwise, just return the shortest one
	else:
		succs = sorted(succs)

		for i in range(len(succs)):
			if f(succs[i], boulderX, boulderY) == lowest_f:
				top_x.append(succs[i])

		top_x = sorted(top_x)
		new_curr = top_x[0] #new curr should be the option that is a smallest of the smallest fs
		

	#if the fs of the og and new curr are same, then add, 
	# #sort, return 0, if that is the og then return none
	
	#this checks if the initial has the same f as the new curr, if new curr < return that
	if f(new_curr, boulderX, boulderY) == f(curr, boulderX, boulderY): 
		end.append(new_curr)
		end.append(curr)
		end = sorted(end)

		if end[0] == curr:
			return None #if curr is the same as new_curr, return none

	return new_curr 

#this method in a loop gets new states, then once the
#minimum state is reached, it prints the options, and
#returns the minimum state.
def nqueens(initial_state, boulderX, boulderY):

	curr = copy.deepcopy(initial_state) # the current state
	conv_state = [] #the list of moves
	conv_state.append(initial_state)
	value = []
	temp_curr = [] #keeps track of the previous curr

	while(f(curr, boulderX, boulderY) != 0):
		curr = choose_next(curr, boulderX, boulderY)

		if curr == None:
			curr = initial_state
			break

		temp_curr = copy.deepcopy(curr) #this is always returned, it is the last step
		value = copy.deepcopy(curr)
		conv_state.append(value)

	for i in range(len(conv_state)): #this prints out the moves for this attempt
		print(str(conv_state[i]) + " - f=" + str(f(conv_state[i], boulderX, boulderY)))

	return temp_curr #returns the last step


#if the minimum state returned doesnt have a f of 0
#then random it, make sure queen not at boulder, start again
#stop if you rach k times.
def nqueens_restart(n, k, boulderX, boulderY):

	#first generate a random array that is n long and has largest number n-1
	curr = []
	cntr = 0 #keeps try of the attempts up to k
	empty = [] #used to clear curr sometimes
	path  = [] #stores the curr returned from nqueens
	starter = [] #keeps track of the new randomly generated boards
	ender = [] #keeps rack of the results of the newly randomly generated boards
	#attempts {} #keeps track of the curr, the final result and the f of it
	current_f = 0 
	lowest_f = 100 #both of these are used to find the smallest f
	temp = 0 
	best_starters = [] #used to store the starters that have the smallest f
	best_enders = [] #used to store the enders that have the smallest f
	trash = [] # this is some throwaway variable thats not important
	c = 0 #used to break the loop once done 


	while (cntr != k+1): #runs through k times to find solution
		x = True
		#this generates a random correct board
		while( x != False): #generates a random and correct board
			c = 0
			curr = copy.deepcopy(empty) #clears the board to try again to randomize
			x == False
			for i in range(0,n):
				curr.append(random.randint(0,n-1)) #makes the board

			for i in range(len(curr)): #checks the board

				if i == boulderX and curr[i] == boulderY: #1 0, so if 0 not in middle fine
					x == True
					c = 1
					break

			if c != 1: #if the board is correct, else repeats
				break

	#at this point you have random board
		print("Current Board: " + str(curr)) #prints the board

		path = nqueens(curr, boulderX, boulderY) #prints the moves of the board
		print(" ..") #to separate the next board
		
		starter.append(curr) # the starting board #changing extend to append
		ender.append(path) # the ending board to keep track for reference
		
		if f(path, boulderX, boulderY) == 0: #if solution found
			break

		cntr += 1 #increments to keep track
		

	#at this point, should have printed, the lists of stuff.
	#now you have to reprint the run/runs with the lowest f. 

	if f(ender[-1], boulderX, boulderY) == 0: #if solution reached
		
		print("Best Solution(s) : (from worst to best)")
		trash = nqueens(starter[-1], boulderX, boulderY) # changing ender to starter
		return

	else: #if no solution reached

		for i in range(len(ender)): #gets lowest f
			current_f = f(ender[i], boulderX, boulderY)
			if current_f < lowest_f:
				temp = copy.deepcopy(current_f)
				lowest_f = copy.deepcopy(temp)

		for i in range(len(ender)): #gets all the enders with that lowest f
			if f(ender[i], boulderX, boulderY) == lowest_f: 
				best_enders.append(ender[i])

		best_enders = sorted(best_enders) #sorts the best enders 

		for i in range(len(best_enders)): # gets all the starters 
			for j in range(len(ender)):
				if best_enders[i] == ender[j]:
					best_starters.append(starter[j])

		best_starters = best_starters[0:len(best_enders)] #makes sure list correct length
		
		
		print("Best Solutions: (from worst to best)") #prints the best solutions starting from 'largest'
		for i in range(len(best_starters)): 
			trash = nqueens(best_starters[(len(best_starters)-1)-i], boulderX, boulderY)
			print(" ..")

# def main():
#   	nqueens_restart(3,1, 2, 2)
  	

# main()