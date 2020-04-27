import copy

'''
Author: Tejvir Mann
Name of Program: Torus_Puzzle.py
Function: Solve a 9 bit square puzzle so the 8 numbers are in order at the end. 

'''

''' author: hobbes
    source: cs540 canvas
    TODO: complete the enqueue method
'''
class PriorityQueue(object):
    def __init__(self):
        self.queue = []
        self.max_len = 0

    def __str__(self):
        return ' '.join([str(i) for i in self.queue])

    def is_empty(self):
        return len(self.queue) == 0

    def enqueue(self, state_dict):
        """ Items in the priority queue are dictionaries:
             -  'state': the current state of the puzzle
             -      'h': the heuristic value for this state
             - 'parent': a reference to the item containing the parent state
             -      'g': the number of moves to get from the initial state to
                         this state, the "cost" of this state
             -      'f': the total estimated cost of this state, g(n)+h(n)

            For example, an item in the queue might look like this:
             {'state':[1,2,3,4,5,6,7,8,0], 'parent':[1,2,3,4,5,6,7,0,8],
              'h':0, 'g':14, 'f':14}

            Please be careful to use these keys exactly so we can test your
            queue, and so that the pop() method will work correctly.

            TODO: complete this method to handle the case where a state is
                  already present in the priority queue
        """
        in_open = False

        #run through the states in the queue. if == then set to true.
        #run through all of the dictionaries, if the state equals any of the parents
        #then in open is true
        y = state_dict['state']
        state_dict2 = copy.deepcopy(state_dict)
        x = state_dict2 #assigning x and g. x: iterates and runs to next parent. g: runs to next state
        g = state_dict2

        while x != None: 
            x = state_dict2['parent']
            if x == None: #if no parent 
                break
            g = x['state']
            if y == g: #if the state = parent state, don't add
                in_open = True
            state_dict2 = x

        if not in_open:
            self.queue.append(state_dict)

        # track the maximum queue length
        if len(self.queue) > self.max_len:
            self.max_len = len(self.queue)

    def requeue(self, from_closed):
        """ Re-queue a dictionary from the closed list (see lecture slide 21)
        """
        self.queue.append(from_closed)

        # track the maximum queue length
        if len(self.queue) > self.max_len:
            self.max_len = len(self.queue)

    def pop(self):
        """ Remove and return the dictionary with the smallest f(n)=g(n)+h(n)
        """
        minf = 0
        for i in range(1, len(self.queue)):
            if self.queue[i]['f'] < self.queue[minf]['f']:
                minf = i
        state = self.queue[minf]
        del self.queue[minf]
        return state

#this method is meant to take it the state, and return the h value
def get_h(state):
    j= 0
    goal = [ 1,2,3,4,5,6,7,8,0]
    for i in state: 
        if state[i] != goal[i]: #checks matches
            j += 1
            if state[i] == 0:
                j -= 1

    return j   


#this method returns an array of the new combo
def get_options(one, two, optionX):
    option = optionX
    temp = option[one]
    option[one] = option[two]
    option[two] = temp 
    return option

#this method is to print all possible successors 
def print_succ(state):
    state1 = copy.deepcopy(state)
    state2 = copy.deepcopy(state)
    state3 = copy.deepcopy(state)
    state4 = copy.deepcopy(state)
    options = [state1, state2, state3, state4]
    goal = [1,2,3,4,5,6,7,8,0]

    empty = 0

    for i in state: #this finds the index of the blank 0
    	if state[i] == 0:
    		empty = i

    #prints all 4 combos for each empty position
    if empty == 0: 
        options[0] = get_options(1,empty, options[0]) #0 is the blank, 1 is to switch with
        options[1] = get_options(2,empty, options[1]) 
        options[2] = get_options(3,empty, options[2])
        options[3] = get_options(6,empty, options[3])
    		

    if empty == 1: 
        options[0] = get_options(0,empty, options[0])
        options[1] = get_options(2,empty, options[1]) 
        options[2] = get_options(4,empty, options[2])
        options[3] = get_options(7,empty, options[3])

    if empty == 2:
        options[0] = get_options(0,empty, options[0])
        options[1] = get_options(1,empty, options[1])
        options[2] = get_options(5,empty, options[2])
        options[3] = get_options(8,empty, options[3])

    if empty == 3: 
        options[0] = get_options(0,empty, options[0])
        options[1] = get_options(4,empty, options[1])
        options[2] = get_options(5,empty, options[2])
        options[3] = get_options(6,empty, options[3])

    if empty == 4: 
        options[0] = get_options(1,empty, options[0])
        options[1] = get_options(3,empty, options[1])
        options[2] = get_options(5,empty, options[2])
        options[3] = get_options(7,empty, options[3])

    if empty == 5:
        options[0] = get_options(2,empty, options[0])
        options[1] = get_options(3,empty, options[1])
        options[2] = get_options(4,empty, options[2])
        options[3] = get_options(8,empty, options[3])

    if empty == 6: 
        options[0] = get_options(0,empty, options[0])
        options[1] = get_options(3,empty, options[1])
        options[2] = get_options(7,empty, options[2])
        options[3] = get_options(8,empty, options[3])

    if empty == 7: 
        options[0] = get_options(1,empty, options[0])
        options[1] = get_options(4,empty, options[1])
        options[2] = get_options(6,empty, options[2])
        options[3] = get_options(8,empty, options[3])

    if empty == 8: 
        options[0]= get_options(2,empty, options[0])
        options[1] = get_options(5,empty, options[1])
        options[2] = get_options(6,empty, options[2])
        options[3]= get_options(7,empty, options[3])

    options = sorted(options) # sorts the combos
    
    h = []
    j = 0
    k = 0 

    # this loop gets all of the h values, and adds them to h. 
    for i in range(len(options)): 
        for k in range(len(options[i])): 
            if options[i][k] != goal[k]:
                j += 1
                if options[i][k] == 0:
                    j-=1  # because we dont count the blank 0

        h.append(j)
        j = 0

    # this method prints the values 
    for i in range(len(options)): 
        print( str(options[i]) + " h=" + str(h[i]))

    return options

# this method is exactly like print succ, but doesn't print succ. 
def dont_print_succ(state):
    state1 = copy.deepcopy(state) 
    state2 = copy.deepcopy(state)
    state3 = copy.deepcopy(state)
    state4 = copy.deepcopy(state)
    options = [state1, state2, state3, state4]
    goal = [1,2,3,4,5,6,7,8,0]

    empty = 0

    for i in state: #this finds the index of the blank 0
        if state[i] == 0:
            empty = i

    if empty == 0: 
        options[0] = get_options(1,empty, options[0]) #0 is the blank, 1 is to switch with
        options[1] = get_options(2,empty, options[1]) 
        options[2] = get_options(3,empty, options[2])
        options[3] = get_options(6,empty, options[3])
            

    if empty == 1: 
        options[0] = get_options(0,empty, options[0])
        options[1] = get_options(2,empty, options[1]) 
        options[2] = get_options(4,empty, options[2])
        options[3] = get_options(7,empty, options[3])

    if empty == 2:
        options[0] = get_options(0,empty, options[0])
        options[1] = get_options(1,empty, options[1])
        options[2] = get_options(5,empty, options[2])
        options[3] = get_options(8,empty, options[3])

    if empty == 3: 
        options[0] = get_options(0,empty, options[0])
        options[1] = get_options(4,empty, options[1])
        options[2] = get_options(5,empty, options[2])
        options[3] = get_options(6,empty, options[3])

    if empty == 4: 
        options[0] = get_options(1,empty, options[0])
        options[1] = get_options(3,empty, options[1])
        options[2] = get_options(5,empty, options[2])
        options[3] = get_options(7,empty, options[3])

    if empty == 5:
        options[0] = get_options(2,empty, options[0])
        options[1] = get_options(3,empty, options[1])
        options[2] = get_options(4,empty, options[2])
        options[3] = get_options(8,empty, options[3])

    if empty == 6: 
        options[0] = get_options(0,empty, options[0])
        options[1] = get_options(3,empty, options[1])
        options[2] = get_options(7,empty, options[2])
        options[3] = get_options(8,empty, options[3])

    if empty == 7: 
        options[0] = get_options(1,empty, options[0])
        options[1] = get_options(4,empty, options[1])
        options[2] = get_options(6,empty, options[2])
        options[3] = get_options(8,empty, options[3])

    if empty == 8: 
        options[0]= get_options(2,empty, options[0])
        options[1] = get_options(5,empty, options[1])
        options[2] = get_options(6,empty, options[2])
        options[3]= get_options(7,empty, options[3])

    options = sorted(options)
    
    h = []
    j = 0
    k = 0

    for i in range(len(options)): 
        for k in range(len(options[i])): 
            if options[i][k] != goal[k]:
                j += 1
                if options[i][k] == 0:
                    j-=1  # because we dont count the blank 0

        h.append(j)
        j = 0

    return options


#this method is supposed to use A* Search to solve hte puzzle from
#start to finish
def solve(state):

    #if the state is already perfect
    goal = [1, 2, 3, 4, 5, 6, 7, 8, 0]
    if state == goal:
        print("[1, 2, 3, 4, 5, 6, 7, 8, 0]  h=0  moves: 0")
        print("Max queue length: 0")
        return

    g = 0
    s = state # the current state 
    open = PriorityQueue() #queue to add the options 
    d = {'state': state, 'h': get_h(s), 'g': g, 'parent': None, 'f': (get_h(s) + g)} 
    y = d
    open.enqueue(d)
    if open.is_empty == True:
        return

    closed = PriorityQueue()
    closed.enqueue(open.pop()) #pop pops off the one with the lowest f. 
    z = 0
    while(get_h(s) != 0):
        
        z += 1
        y = closed.pop()
        g += 1
        #g += y['g'] + 1

        s = y['state'] 
        if get_h(s) == 0:
            break

        options = dont_print_succ(s) # gets successors 
        for i in range(len(options)): 
            x = get_h(options[i])
            open.enqueue({'state': options[i], 'h': x, 'g': g, 'parent': y, 'f': (x + g)})

        smallest = open.pop() #keep smallest
        closed.enqueue(smallest)
        open = PriorityQueue()

    m = copy.deepcopy(y)
    final = {}
    x = y 
    
    #add all the steps to a dictionary
    while x != None: 
        g -= 1
        x = m['parent']
        final[g] = {'state': m['state'], 'h': m['h'], 'g': m['g']}
        if x == None:
            break
        m = x

        #print the steps 
    for i in range(len(final)):
        print(str(final[i]['state']) + "  h=" + str(final[i]['h']) + "  moves: " + str(final[i]['g']))

    print("Max queue length: " + str(open.max_len))



# def main(): 


#     solve([1,2,3,4,5,6,7,8,0])
    

# main()



