import random
import copy
import time

'''
Name: teeko_player.py
Author: Tejvir Mann
Project: P5, this is a game where you face a AI machine. to get 4 in
 a row or a square.

'''

class TeekoPlayer:
    """ An object representation for an AI game player for the game Teeko.
    """
    board = [[' ' for j in range(5)] for i in range(5)]
    pieces = ['b', 'r']
    full_depth = 1

    def __init__(self):
        """ Initializes a TeekoPlayer object by randomly selecting red or black as its
        piece color.
        """
        self.my_piece = random.choice(self.pieces)
        self.opp = self.pieces[0] if self.my_piece == self.pieces[1] else self.pieces[1]
        self.depth = self.full_depth

    def succ(self, state):
        drop_phase = True
        total_space = 17
        space = 0
        m = 0 #to keep track of the index when finding the right successor

        for row in state:
            for i in range(5):
                if row[i] == ' ':
                    space += 1

        if total_space == space: 
            drop_phase == False

        if space <= 17: #THEN MOVE PHASE 
            player = self.my_piece
            curr_state = copy.deepcopy(state)
            succs_move = []
            locations = []

            for row in range(len(state)):
                for i in range(len(state)): 
                    if state[row][i] == player:
                        locations.append([row,i]) #get the location of the 4 pieces

            for num in range(4):
                for i in range(len(state)):
                    for j in range(len(state)): 
                        if curr_state[i][j] == ' ':
                            curr_state[i][j] = player
                            curr_state[locations[num][0]][locations[num][1]] = ' ' 
                            #sets the old location of the piece to ' '
                            temp = copy.deepcopy(curr_state)
                            succs_move.append(temp)
                            curr_state = copy.deepcopy(state) 

            return succs_move

        #DROP PHASE
        player = self.my_piece
        curr_state = copy.deepcopy(state)
        succs_drop = []

        for i in range(len(state)):
            for j in range(len(state)): 
                if curr_state[i][j] == ' ':
                    curr_state[i][j] = player
                    temp = copy.deepcopy(curr_state)
                    succs_drop.append(temp)
                    curr_state = copy.deepcopy(state)
  
        return succs_drop


    def Max_Value(self, state, depth):
        the_scores = []

        value = self.game_value(state)
        if value == 1 or value == -1:
            return value

        if depth >= self.depth:
            a = self.get_scores(state) 
            #way to grade the unterminated states
            return a

        else: 
            a = -1000
            for s in self.succ(state):
                a = self.Min_Value(state, depth+1)
                the_scores.append(a)

        return max(the_scores)

    def Min_Value(self, state, depth):
        the_scores = []

        value = self.game_value(state)
        if value == 1 or value == -1:
            return value

        if depth >= self.depth:
            b = self.get_scores(state)
            return b 

        else: 
            b = 1000
            for s in self.succ(state):
                #minimum of all of the states returned. 
                b = self.Max_Value(state, depth+1)
                the_scores.append(b)

        return min(the_scores)

    def heuristic_game_value(self, state):
        #this method gets the max and min alogithm on each state, and returns a 
        #number between -1 and 1 for each state. 
        start_depth = 0
        curr_state = copy.deepcopy(state)

        #call game value on the state. If terminal, return. 
        if self.game_value(curr_state) == 1: 
            return 1

        #call max value
        return self.Max_Value(curr_state, start_depth) 

    def get_scores(self,state):
        #set options for -0.75, -0.5, -0.25, 0. 0.5, 0.25, and 0.75

        #0.75, if there is a ' ' and 3 in a row. Or 3 and almost a square. (3)
        three_value = self.three_row(state)
        if three_value != 0:
            return three_value

        #0.5, if there is ' ' ' ' and 2 in a row, or ' ' 2 and ' ', 
                #2 row ' ' ' ', or 2 then 2 open below (4)
        two_value = self.two_row(state)
        if two_value != 0:
            return two_value

        #0.25
        one_value = self.one_row(state)
        if one_value != 0:
            return one_value

        #0 if no other options
        return 0

    def three_row(self, state):

        # check horizontal 
        for row in state:
            for i in range(3): #used to be 3.
                if row[i] != ' ' and row[i] == row[i+1] == row[i+2]:
                    if row[i].count(' ') == 2:
                        return 0.75 if row[i]==self.my_piece else -0.75

        # check vertical 
        for col in range(5):
            counter = 0
            for i in range(3): #might need to decrease, if range starts at 0 or 1.
                if state[i][col] == ' ':
                    counter += 1
                if state[i][col] != ' ' and state[i][col] == state[i+1][col] == state[i+2][col]:
                    if counter == 2:
                        return 0.75 if state[i][col]==self.my_piece else -0.75

        # check \ diagonal 
        if state[0][0] != ' ' and state[0][0] == state[1][1] == state[2][2]:
            if state[3][3] == ' ':
                    return 0.75 if state[0][0]==self.my_piece else -0.75

        if state[1][1] != ' ' and state[1][1] == state[2][2] == state[3][3]:
            if state[4][4] == ' ' or state[0][0] == ' ':
                    return 0.75 if state[0][0]==self.my_piece else -0.75

        if state[2][2] != ' ' and state[2][2] == state[3][3] == state[4][4]:
            if state[1][1] == ' ':
                    return 0.75 if state[0][0]==self.my_piece else -0.75

        # check / diagonal 
        if state[0][4] != ' ' and state[0][4] == state[1][3] == state[2][2]: 
            if state[3][1] == ' ':
                    return 0.75 if state[0][4]==self.my_piece else -0.75

        if state[1][3] != ' ' and state[1][3] == state[2][2] == state[3][1]: 
            if state[1][4] == ' ' or state[4][1] == ' ':
                    return 0.75 if state[1][3]==self.my_piece else -0.75

        if state[2][2] != ' ' and state[2][2] == state[3][1] == state[4][0]:
            if state[1][3] == ' ':
                    return 0.75 if state[2][2]==self.my_piece else -0.75

        # check 2x2 box 
        for i in range(4): #number of rows to check  'row'
            for j in range(4): #number of columns to go through 'col'
                if state[i][j] != ' ' and state[i][j] == state[i][j+1]: 
                    if (state[i+1][j] or state[i+1][j+1]) == ' ' and (state[i+1][j] or state[i+1][j+1]) == state[i][j]:
                        return 0.75 if state[i][j]==self.my_piece else -0.75
                if (state[i][j] or state[i][j+1]) == ' ' and (state[i][j] or state[i][j+1]) != ' ':
                    if state[i+1][j] != ' ' and  state[i+1][j] == state[i+1][j+1]:
                        if(state[i][j] or state[i][j+1]) == state[i+1][j]:
                            return 0.75 if state[i][j]==self.my_piece else -0.75

        #put count stuff here. with all.
        #if a row contains 3 of this, and 2 " " or diag, or col.
        diagonal_two = [state[0][4],state[1][3], state[2][2], state[3],[1], state[4][0]]
        diagonal_one = [state[0][0], state[1][1], state[2][2], state[3][3], state[4][4]]

        if diagonal_two.count(self.my_piece) == 3 and diagonal_two.count(' ') == 2:
            return 0.75
        if diagonal_two.count(self.opp) == 3 and diagonal_two.count(' ') == 2:
            return -0.75
        if diagonal_one.count(self.my_piece) == 3 and diagonal_one.count(' ') == 2:
            return 0.75
        if diagonal_one.count(self.opp) == 3 and diagonal_one.count(' ') == 2:
            return -0.75

        return 0

    def two_row(self, state):
        for row in state:
            for i in range(len(row)): 
                a = row[i].count(self.my_piece)
                b = row[i].count(' ')
                c = row[i].count(self.opp)
                if a == 2 and b == 3: 
                    return 0.5
                if c == 2 and b == 3: 
                    return -0.5
                if a == 3 and b == 1:
                    return 0.5
                if c == 3 and b == 1:
                    return -0.5

        for col in range(5):
            column = []
            for i in range(5):
                column.append(state[i][col])
            a = column.count(self.my_piece)
            b = column.count(' ')
            c = column.count(self.opp)
            if a == 2 and b == 3: 
                return 0.5
            if c == 2 and b == 3: 
                return -0.5
            if a == 3 and b == 1:
                return 0.5
            if c == 3 and b == 1:
                return -0.5

        diagonal_two = [state[0][4],state[1][3], state[2][2], state[3],[1], state[4][0]]
        diagonal_one = [state[0][0], state[1][1], state[2][2], state[3][3], state[4][4]]

        a = diagonal_one.count(self.my_piece)
        b = diagonal_one.count(' ')
        c = diagonal_one.count(self.opp)

        d = diagonal_two.count(self.my_piece)
        e = diagonal_two.count(' ')
        f = diagonal_two.count(self.opp)

        if d == 2 and e == 3:
            return 0.5
        if f == 2 and e == 3:
            return -0.5
        if a == 3 and b == 1:
            return 0.5
        if c == 3 and b == 1:
            return -0.5

        if d == 3 and e == 1:
            return 0.5
        if f == 3 and e == 1:
            return -0.5
        if a == 2 and b == 3:
            return 0.5
        if c == 2 and b == 3:
            return -0.5

        # check 2x2 box 
        for i in range(4): #number of rows to check  'row'
            for j in range(4):
                box = [state[i][j],state[i][j+1], state[i+1][j], state[i+1],[j+1]]
                if box.count(self.my_piece) == 2 and box.count(' ') ==2:
                    return 0.5
                if box.count(self.opp) == 2 and box.count(' ') ==2:
                    return -0.5

        return 0

    def one_row(self,state):
        for row in state:
            for i in range(len(row)): 
                a = row[i].count(self.my_piece)
                b = row[i].count(' ')
                c = row[i].count(self.opp)
                if a == 1 and b == 4: 
                    return 0.25
                if c == 1 and b == 4: 
                    return -0.25
                if a == 2 and b == 2:
                    return 0.25
                if c == 2 and b == 2:
                    return -0.25

        for col in range(5):
            column = []
            for i in range(5):
                column.append(state[i][col])
            a = column.count(self.my_piece)
            b = column.count(' ')
            c = column.count(self.opp)
            if a == 1 and b == 4: 
                return 0.25
            if c == 1 and b == 4: 
                return -0.25
            if a == 2 and b == 2:
                return 0.25
            if c == 2 and b == 2:
                return -0.25

        diagonal_two = [state[0][4],state[1][3], state[2][2], state[3],[1], state[4][0]]
        diagonal_one = [state[0][0], state[1][1], state[2][2], state[3][3], state[4][4]]

        a = diagonal_one.count(self.my_piece)
        b = diagonal_one.count(' ')
        c = diagonal_one.count(self.opp)

        d = diagonal_two.count(self.my_piece)
        e = diagonal_two.count(' ')
        f = diagonal_two.count(self.opp)

        if d == 1 and e == 4:
            return 0.25
        if f == 1 and e == 4:
            return -0.25
        if a == 2 and b == 2:
            return 0.25
        if c == 2 and b == 2:
            return -0.25

        if d == 2 and e == 2:
            return 0.25
        if f == 2 and e == 2:
            return -0.25
        if a == 1 and b == 4:
            return 0.25
        if c == 1 and b == 4:
            return -0.25

        # check 2x2 box 
        for i in range(4): #number of rows to check  'row'
            for j in range(4):
                box = [state[i][j],state[i][j+1], state[i+1][j], state[i+1],[j+1]]
                if box.count(self.my_piece) == 1 and box.count(' ') ==3:
                    return 0.25
                if box.count(self.opp) == 1 and box.count(' ') == 3:
                    return -0.25

        return 0



    def make_move(self, state):

        """ Selects a (row, col) space for the next move. You may assume that whenever
        this function is called, it is this player's turn to move.
            
        Args:
            state (list of lists): should be the current state of the game as saved in
                this TeekoPlayer object. Note that this is NOT assumed to be a copy of
                the game state and should NOT be modified within this method (use
                place_piece() instead). Any modifications (e.g. to generate successors)
                should be done on a deep copy of the state.
                
                In the "drop phase", the state will contain less than 8 elements which
                are not ' ' (a single space character).
        
        Return:
            move (list): a list of move tuples such that its format is
                    [(row, col), (source_row, source_col)]
                where the (row, col) tuple is the location to place a piece and the
                optional (source_row, source_col) tuple contains the location of the
                piece the AI plans to relocate (for moves after the drop phase). In
                the drop phase, this list should contain ONLY THE FIRST tuple.

        Note that without drop phase behavior, the AI will just keep placing new markers
            and will eventually take over the board. This is not a valid strategy and
            will earn you no points.
        """

        drop_phase = True
        succ_scores = [] #this is an array that will have 
                         #the heuristic scores for each successor
        next_move = []
        check_heur = True

        #1. check if drop phase or not.
        total_space = 17
        space = 0
        m = 0 #to keep track of the index when finding the right successor

        for row in state:
            for i in range(5):  #used to be row
                if row[i] == ' ':
                    space += 1
        
        if space == 17: 
            drop_phase == False

        if space <= 17: #THEN MOVE PHASE
            #1. Get sucessors 
            succs = self.succ(state)

            #check terminal state
            for i in range(len(succs)):
                if self.game_value(succs[i]) == 1:
                    next_move = copy.deepcopy(succs[i])
                    check_heur = False
            
            if check_heur == True:
                #2. Run them through these Hueristic method 
                for i in range(len(succs)): #MIN MAX MODEL CALLED IN THIS H_METHOD
                    succ_scores.append(self.heuristic_game_value(succs[i]))
                #pick the largest score or if mutiple maxes, then pick first. 
                curr_score = -1 #keeps track of the largest score 
                for i in range(len(succ_scores)):
                    if succ_scores[i] > curr_score:
                        curr_score = copy.deepcopy(succ_scores[i])
                        m = copy.deepcopy(i)
                        if(succ_scores[i] == 1):
                            break

            curr_state = copy.deepcopy(state)
            if check_heur == True:
                next_move = copy.deepcopy(succs[m]) #the succ
            move = []

            #now you have the new state and the old one. 
            for i in range(len(curr_state)):
                for j in range(len(row)): 
                    if curr_state[i][j] != next_move[i][j]:
                        if next_move[i][j] == self.my_piece: #new location
                            move.insert(0, (i, j))
                        else:
                            move.insert(1, (i, j)) #the old location, which should become blank.
                            

            return move

        #DROP PHASE
        succs = self.succ(state) #used to be self,state

        for i in range(len(succs)):
            if self.game_value(succs[i]) == 1: #removed self from parameter
                next_move = copy.deepcopy(succs[i])
                check_heur = False

        if check_heur == True:
            for i in range(len(succs)): #MIN MAX METHOD CALLED IN THIS H METHOD
                succ_scores.append(self.heuristic_game_value(succs[i]))

            #pick the largest score or if mutiple maxes, then pick first. 
            curr_score = -1 #keeps track of the largest score 
            m = 0 #keeps track of the index
            for i in range(len(succ_scores)):
                if succ_scores[i] > curr_score:
                    curr_score = copy.deepcopy(succ_scores[i])
                    m = copy.deepcopy(i)
                    if(succ_scores[i] == 1):
                        break

        curr_state = copy.deepcopy(state)
        if check_heur == True:
            next_move = copy.deepcopy(succs[m]) #the succ
        move = []

        #now you have the new state and the old one. 
        for i in range(len(curr_state)):
            for j in range(len(row)): 
                if curr_state[i][j] != next_move[i][j]:
                    if next_move[i][j] == self.my_piece: #new location
                        move.insert(0, (i, j))
                        break

        return move

    def opponent_move(self, move):
        """ Validates the opponent's next move against the internal board representation.
        You don't need to touch this code.

        Args:
            move (list): a list of move tuples such that its format is
                    [(row, col), (source_row, source_col)]
                where the (row, col) tuple is the location to place a piece and the
                optional (source_row, source_col) tuple contains the location of the
                piece the AI plans to relocate (for moves after the drop phase). In
                the drop phase, this list should contain ONLY THE FIRST tuple.
        """
        # validate input
        if len(move) > 1:
            source_row = move[1][0]
            source_col = move[1][1]
            if source_row != None and self.board[source_row][source_col] != self.opp:
                raise Exception("You don't have a piece there!")
        if self.board[move[0][0]][move[0][1]] != ' ':
            raise Exception("Illegal move detected")
        # make move
        self.place_piece(move, self.opp)
        
    def place_piece(self, move, piece):
        """ Modifies the board representation using the specified move and piece
        
        Args:
            move (list): a list of move tuples such that its format is
                    [(row, col), (source_row, source_col)]
                where the (row, col) tuple is the location to place a piece and the
                optional (source_row, source_col) tuple contains the location of the
                piece the AI plans to relocate (for moves after the drop phase). In
                the drop phase, this list should contain ONLY THE FIRST tuple.
                
                This argument is assumed to have been validated before this method
                is called.
            piece (str): the piece ('b' or 'r') to place on the board
        """
        if len(move) > 1:
            self.board[move[1][0]][move[1][1]] = ' '
        self.board[move[0][0]][move[0][1]] = piece
        
    def print_board(self):
        """ Formatted printing for the board """
        for row in range(len(self.board)):
            line = str(row)+": "
            for cell in self.board[row]:
                line += cell + " "
            print(line)
        print("   A B C D E")
        
    def game_value(self, state):
        """ Checks the current board status for a win condition
        
        Args:
        state (list of lists): either the current state of the game as saved in
            this TeekoPlayer object, or a generated successor state.

        Returns:
            int: 1 if this TeekoPlayer wins, -1 if the opponent wins, 0 if no winner
       
        """
        # check horizontal wins
        for row in state:
            for i in range(2):
                if row[i] != ' ' and row[i] == row[i+1] == row[i+2] == row[i+3]:
                    return 1 if row[i]==self.my_piece else -1

        # check vertical wins
        for col in range(5):
            for i in range(2):
                if state[i][col] != ' ' and state[i][col] == state[i+1][col] == state[i+2][col] == state[i+3][col]:
                    return 1 if state[i][col]==self.my_piece else -1

        # check \ diagonal wins
        if state[0][0] != ' ' and state[0][0] == state[1][1] == state[2][2] == state[3][3]:
                    return 1 if state[0][0]==self.my_piece else -1

        if state[1][1] != ' ' and state[1][1] == state[2][2] == state[3][3] == state[4][4]:
                    return 1 if state[0][0]==self.my_piece else -1

        # check / diagonal wins
        if state[0][4] != ' ' and state[0][4] == state[1][3] == state[2][2] == state[3][1]:
                    return 1 if state[0][4]==self.my_piece else -1

        if state[1][3] != ' ' and state[1][3] == state[2][2] == state[3][1] == state[4][0]:
                    return 1 if state[1][3]==self.my_piece else -1

        # check 2x2 box wins
        for i in range(4): #number of rows to check  'row'
            for j in range(4): #number of columns to go through 'col'
                if state[i][j] != ' ' and state[i][j] == state[i][j+1]: #if 2 in same row same, check below
                    if state[i+1][j] != ' ' and state[i+1][j] == state[i+1][j+1]:
                        if state[i][j] == state[i+1][j+1]:
                            return 1 if state[i][j]==self.my_piece else -1


        return 0 # no winner yet

############################################################################
#
# THE FOLLOWING CODE IS FOR SAMPLE GAMEPLAY ONLY
#
############################################################################

ai = TeekoPlayer()
piece_count = 0
turn = 0

# drop phase
while piece_count < 8:

    # get the player or AI's move
    if ai.my_piece == ai.pieces[turn]:
        ai.print_board()
        move = ai.make_move(ai.board)
        ai.place_piece(move, ai.my_piece)
        print(ai.my_piece+" moved at "+chr(move[0][1]+ord("A"))+str(move[0][0]))
    else:
        move_made = False
        ai.print_board()
        print(ai.opp+"'s turn")
        while not move_made:
            player_move = input("Move (e.g. B3): ")
            while player_move[0] not in "ABCDE" or player_move[1] not in "01234":
                player_move = input("Move (e.g. B3): ")
            try:
                ai.opponent_move([(int(player_move[1]), ord(player_move[0])-ord("A"))])
                move_made = True
            except Exception as e:
                print(e)

    # update the game variables
    piece_count += 1
    turn += 1
    turn %= 2

# move phase - can't have a winner until all 8 pieces are on the board
while ai.game_value(ai.board) == 0:

    # get the player or AI's move
    if ai.my_piece == ai.pieces[turn]:
        ai.print_board()
        move = ai.make_move(ai.board)
        ai.place_piece(move, ai.my_piece)
        print(ai.my_piece+" moved from "+chr(move[1][1]+ord("A"))+str(move[1][0])) #out of range?
        print("  to "+chr(move[0][1]+ord("A"))+str(move[0][0]))
    else:
        move_made = False
        ai.print_board()
        print(ai.opp+"'s turn")
        while not move_made:
            move_from = input("Move from (e.g. B3): ")
            while move_from[0] not in "ABCDE" or move_from[1] not in "01234":
                move_from = input("Move from (e.g. B3): ")
            move_to = input("Move to (e.g. B3): ")
            while move_to[0] not in "ABCDE" or move_to[1] not in "01234":
                move_to = input("Move to (e.g. B3): ")
            try:
                ai.opponent_move([(int(move_to[1]), ord(move_to[0])-ord("A")),
                                 (int(move_from[1]), ord(move_from[0])-ord("A"))])
                move_made = True
            except Exception as e:
                print(e)

    # update the game variables
    turn += 1
    turn %= 2

ai.print_board()
if ai.game_value(ai.board) == 1:
    print("AI wins! Game over.")
else:
    print("You win! Game over.")
