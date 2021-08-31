'''
hexapawn.py
Alyssa Rodriguez
SID: 917730599
ECS 170 - HW3

ASSIGNMENT:
- hexapawn intended to be played on a 3x3 chessboard
- we are extending the definition of hexapawn to include any similar game
  invovling n white pawns, n black pawns, and a nxn board
- two players face each other across the board
- each player begins with three white pawns or three black pawns
- player with the white pawn always moves first
- white is always on top of board
- black is always on bottom of board

REQUIREMENTS:
- function must select the best next move by using MiniMax search.
- need to devise a static board evaluation function (can use the one that was given in class)

NOTES:
- if next_player_to_move is 'b', then board_state should be a board where 'w' has already moved
  since 'w' always goes first. It would never be a "fresh" game if 'b' is to move next
- if next_player_to_move is 'w', then board_state could either be a "fresh" game OR a game that is
  already in progress and 'b' has already moved

TEST INPUTS:
hexapawn(["www","---","bbb"],3,'w',2)
output: ['-ww', 'w--', 'bbb']

hexapawn(["w-w","-w-","b-b"],3,'b',2)
output: ['w-w', '-b-', '--b']

hexapawn(["--w","w--","bbb"],3,'b',2)
output: ['--w', 'b--', 'b-b']

hexapawn(['wwwww','-----','-----','-----','bbbbb'], 5, 'w', 5)
output: ['-wwww', 'w----', '-----', '-----', 'bbbbb']

hexapawn(["wwwwwwwwww","----------","----------","----------","----------","----------","----------","----------","----------","bbbbbbbbbb"],10,'w',6)
output: ['-wwwwwwwww', 'w---------', '----------', '----------', '----------', '----------', '----------', '----------', '----------', 'bbbbbbbbbb']
'''

import math
# import time

# global variables
white_pawn = 'w'
black_pawn = 'b'

maximizer = None
minimizer = None

best_move = None

# top-level function
def hexapawn(board_state, size_of_board, next_player_to_move, num_moves_ahead):
    '''
    - takes as args:
    --> board_state: a representation of the state of a hexapawn game (i.e. a board position)
    --> size_of_board: an integer representing the size of the board
    --> next_player_to_move: an indication as to which player is to move next 'w' or 'b'
    --> num_moves_ahead: an integer representing the number of moves to look ahead
    
    - this function returns as output the best next move(best_move) that the designated player
      can make from that given board position.
    - the output is represented as a hexapawn board position in the same format
      that is used for the input board position.
    '''
    # start_time = time.time()
    
    global maximizer
    global minimizer
    
    # error handling
    fresh_board = ["www", "---", "bbb"]
    if board_state == fresh_board:
        # ensure that next player to move is white, invalid if it is black
        if next_player_to_move != 'w':
            print("ERR:fresh board inputted, thus only white can move")
            return
    # make sure that the inputted board is equivalent to the inputted board size
    if len(board_state) == size_of_board:
        # also check if the row length in board is equal to board size
        for row in board_state:
            if len(row) != size_of_board:
                print("ERR:row length is not equal to board size")
                return
    else:
        print("ERR:inputted board is not equal to the board size")
    # end of error handling

    # set the maximizer and minimizer 
    if next_player_to_move == white_pawn:
        maximizer = white_pawn
        minimizer = black_pawn
    else:
        maximizer = black_pawn
        minimizer = white_pawn

    '''
    for row in board_state:
        print(row)
    print('\n')
    '''

    # minimax will update the global variable, best_move, which is what program is ultimately returning
    minimax(board_state, size_of_board, next_player_to_move, num_moves_ahead, True)

    # print("--- %s seconds ---" % (time.time() - start_time))
    
    return best_move
    
def minimax(board, size, next_player, depth, is_maximizing_player):
    '''
    - minimax algorithm to alternately propagate minima and maxima upward from "bottom"
    - recursive algorithm for choosing the next move in a n-player game
    - a value is associated with each state of the game
    - the value is computed by the static board evaluation

    - takes as args:
    --> board: a representation of the state of a hexapawn game (i.e. a board position)
    --> size: an integer representing the size of the board
    --> next_player: an indication as to which player is to move next 'w' or 'b'
    --> depth: an integer representing the number of moves to look ahead
    --> is_maximizing_player: bool value that indicates whether it is the maximizer's turn or not

    - updates global variable best_move 
    '''
    global best_move

    value_board_arr = []
    
    win_result = win_checker(board, size)
        
    # check if depth is 0 or if the game is over in the current board
    if depth == 0 or win_result != None:
        # return static evaluation of board
        return evaluation(board, size, next_player)

    # otherwise if it's currently the turn of the maximizing player, which means it is next_player turn to move then
    # want to find the highest evaluation that can be obtained from this board state
    if is_maximizing_player:
        # print("is_maximizing_player")
        max_eval = -math.inf
        
        # loop through all the possible new_states
        new_states = generate_new_states(board, size, next_player)
        # print("new_states:", new_states)
        
        for new_state in new_states:
            # print("max new_state:", new_state)
            # find the evaluation of each new_state
            # make recursive call to the minimax function, passing in new_state, depth - 1, and false
            # false because it is now MIN's turn to move
            
            next_player = minimizer
        
            new_state_eval = minimax(new_state, size, next_player, depth - 1, False)
            # print("max new_state_eval:", new_state_eval)

            #value_board_dict["board"] = new_state
            #print("value_board_dict:", value_board_dict)

            # store the new_state_eval along with its associated board in value_board_arr array
            value_board_arr.append({new_state_eval: new_state})

            # set max_eval to whichever is greater between the current max evaluation and the evaulation of child position
            max_eval = max(max_eval, new_state_eval)
            # print("max_eval:", max_eval)

        # once all the new states have been evaluated, set best_move to be the board with the max_eval

        # print("value_board_arr:", value_board_arr)

        # loop through elements in value_board_arr
        for value_board in value_board_arr:
            # get the board with key that is equal to max_eval and set that to best_move
            if max_eval in value_board:
                best_move = (value_board[max_eval])
                break

        return max_eval
    else:
        # print("is_minimizing_player")
        min_eval = math.inf

        new_states = generate_new_states(board, size, next_player)

        for new_state in new_states:
            # print("min new_state:", new_state)
            
            next_player = maximizer
            
            new_state_eval = minimax(new_state, size, next_player, depth - 1, True)
            # print("new_state_eval:", new_state_eval)

            min_eval = min(min_eval, new_state_eval)
            # print("min_eval:", min_eval)

        return min_eval
    
'''
OPERATORS:
- a player may choose to move on of their pawns in one of these ways:
--> a pawn may be moved one square forward to an empty space
--> a pawn may be moved one square diagnolly forward to a square occupied by
    an opponent's pawn. The opponent's pawn is then removed.
'''
def move_pawn_forward(board, size, next_player):
    '''
    - move forward operator function
    
    - takes as args:
    --> board: a representation of the state of a hexapawn game (i.e. a board position)
    --> size: an integer representing the size of the board
    --> next_player: an indication as to which player is to move next 'w' or 'b'

    - returns array, new_boards, that contains boards with a pawn shifted forwards
    '''
    # print("\n===FORWARD===")

    dup_board = board[:]
    new_boards = []
    
    if next_player == white_pawn:
        # print("move white pawn forward")
        # list that stores dictionaries of white_pawn position info
        white_pawn_arr = []

        for row in dup_board:
            for char_index, char in enumerate(row):
                if char == white_pawn:
                    # dictionary that stores the board row index a white pawn appears in
                    # and the char index the pawn appears in 
                    white_pawn_pos = {}
                    
                    row_index = dup_board.index(row)
                    
                    white_pawn_pos["row_pos"] = row_index
                    white_pawn_pos["char_pos"] = char_index
                    
                    white_pawn_arr.append(white_pawn_pos)

        # print("white_pawn_arr:",white_pawn_arr)

        for i in range(len(white_pawn_arr)):
            # print("white pawn", i, "row", white_pawn_arr[i]["row_pos"], "char index", white_pawn_arr[i]["char_pos"])
            white_pawn_row_pos = white_pawn_arr[i]["row_pos"]
            white_pawn_char_pos = white_pawn_arr[i]["char_pos"]

            # makes sure when white pawn gets to the end of board, it doesn't move forward any further
            if white_pawn_row_pos + 1 != size:
                forward_space_row = white_pawn_row_pos + 1
                forward_space_char = white_pawn_char_pos
            else:
                # break when white pawn is at the end of board
                continue

            # for each white pawn, check if the space in front of them is empty or not
            if dup_board[forward_space_row][forward_space_char] == '-':
                # convert to list so that elements can be updated
                white_pawn_row_list = list(dup_board[white_pawn_row_pos])
                
                # update white pawn char pos to be empty
                white_pawn_row_list[white_pawn_char_pos] = '-'
                white_pawn_row = ''.join(white_pawn_row_list)

                # update dup_board
                dup_board[white_pawn_row_pos] = white_pawn_row

                # convert to list so that elements can be updated
                white_pawn_row_list_2 = list(dup_board[forward_space_row])
                
                # update the forward space to be white pawn
                white_pawn_row_list_2[white_pawn_char_pos] = white_pawn
                white_pawn_row2 = ''.join(white_pawn_row_list_2)

                # update dup_board
                dup_board[forward_space_row] = white_pawn_row2

                if dup_board not in new_boards:
                    new_boards.append(dup_board)
                    dup_board = board[:]
                    
        # print("new_boards:", new_boards)
        return new_boards  
    else:
        # print("move black pawn forward")
        # list that stores dictionaries of black_pawn position info
        black_pawn_arr = []

        for row in dup_board:
            for char_index, char in enumerate(row):
                if char == black_pawn:
                    # dictionary that stores the board row index a black pawn appears in
                    # and the char index the pawn appears in 
                    black_pawn_pos = {}
                    
                    row_index = dup_board.index(row)
                    
                    black_pawn_pos["row_pos"] = row_index
                    black_pawn_pos["char_pos"] = char_index
                    
                    black_pawn_arr.append(black_pawn_pos)

        # print("black_pawn_arr:", black_pawn_arr)

        for i in range(len(black_pawn_arr)):
            # print("black pawn", i, "row", black_pawn_arr[i]["row_pos"], "char index", black_pawn_arr[i]["char_pos"])
            black_pawn_row_pos = black_pawn_arr[i]["row_pos"]
            black_pawn_char_pos = black_pawn_arr[i]["char_pos"]
            
            # makes sure when black pawn gets to the end of board, it doesn't move forward any further
            if black_pawn_row_pos != 0:
                forward_space_row = black_pawn_row_pos - 1
                forward_space_char = black_pawn_char_pos
            else:
                # continue when black pawn is at the end of board
                continue

            # for each black pawn, check if the space in front of them is empty or not
            if dup_board[forward_space_row][forward_space_char] == '-':
                # convert to list so that elements can be updated
                black_pawn_row_list = list(dup_board[black_pawn_row_pos])
                
                # update black pawn char pos to be empty
                black_pawn_row_list[black_pawn_char_pos] = '-'
                black_pawn_row = ''.join(black_pawn_row_list)

                # update dup_board
                dup_board[black_pawn_row_pos] = black_pawn_row

                # convert to list so that elements can be updated
                black_pawn_row_list_2 = list(dup_board[forward_space_row])
                
                # update the forward space to be black pawn
                black_pawn_row_list_2[black_pawn_char_pos] = black_pawn
                black_pawn_row_2 = ''.join(black_pawn_row_list_2)

                # update dup_board
                dup_board[forward_space_row] = black_pawn_row_2

                if dup_board not in new_boards:
                    new_boards.append(dup_board)
                    dup_board = board[:]
                    
        # print("new_boards:", new_boards)
        return new_boards  

def move_pawn_diagnolly(board, size, next_player):
    '''
    - move forward diagnolly operator function

    - takes as args:
    --> board: a representation of the state of a hexapawn game (i.e. a board position)
    --> size: an integer representing the size of the board
    --> next_player: an indication as to which player is to move next 'w' or 'b'
    
    - returns array, new_boards, that contains boards with a pawn shifted forwards diagnolly
    '''
    # print("\n===DIAGNOL===")

    dup_board = board[:]
    new_boards = []

    if next_player == white_pawn:
        # list that stores dictionaries of white_pawn position info
        white_pawn_arr = []

        for row in dup_board:
            for char_index, char in enumerate(row):
                if char == white_pawn:
                    # dictionary that stores the board row index a white pawn appears in
                    # and the char index the pawn appears in 
                    white_pawn_pos = {}
                    
                    row_index = dup_board.index(row)
                    
                    white_pawn_pos["row_pos"] = row_index
                    white_pawn_pos["char_pos"] = char_index
                    
                    white_pawn_arr.append(white_pawn_pos)

        # print("white_pawn_arr:",white_pawn_arr)

        for i in range(len(white_pawn_arr)):
            # print("white pawn", i, "row", white_pawn_arr[i]["row_pos"], "char index", white_pawn_arr[i]["char_pos"])
            white_pawn_row_pos = white_pawn_arr[i]["row_pos"]
            white_pawn_char_pos = white_pawn_arr[i]["char_pos"]
            
            # makes sure when white pawn gets to the end of board, it doesn't move diagnolly forward any further
            if white_pawn_row_pos + 1 != size:
                diagnol_space_row = white_pawn_row_pos + 1
            else:
                # break when white pawn is at the end of board
                continue

            # case where white pawn is at the leftmost edge of board
            # can't move left diagnolly, but can move right diagnolly
            if [white_pawn_row_pos, white_pawn_char_pos] == [white_pawn_row_pos,0]:
                # print([white_pawn_row_pos, white_pawn_char_pos], "cannot move left diagnolly, out of bounds")
                
                right_diagnol_space_char = white_pawn_char_pos + 1
                # print("R:", diagnol_space_row, right_diagnol_space_char)
                
                # though pawn is in the position to move right diagnolly
                # check if it actually can by checking if there is black pawn in that diagnol space
                if dup_board[diagnol_space_row][right_diagnol_space_char] == black_pawn:
                    # print("white pawn can move right diagnolly by capturing black pawn")

                    # convert the row the white pawn is in into a list so that updating its elements is possible
                    white_pawn_row_list = list(dup_board[white_pawn_row_pos])

                    # position where white pawn resides is going to now be empty
                    white_pawn_row_list[white_pawn_char_pos] = '-'
                    white_pawn_row = ''.join(white_pawn_row_list)

                    # update dup_board
                    dup_board[white_pawn_row_pos] = white_pawn_row
                    
                    right_diagnol_row_list = list(dup_board[diagnol_space_row])

                    # since there is a black pawn in right diagnol forward space, white pawn moves to that space and captures black pawn
                    right_diagnol_row_list[right_diagnol_space_char] = white_pawn
                    move_right_diagnolly = ''.join(right_diagnol_row_list)

                    # update dup_board
                    dup_board[diagnol_space_row] = move_right_diagnolly

                    if dup_board not in new_boards:
                        new_boards.append(dup_board)
                        dup_board = board[:]
            # case where white pawn is at the rightmost edge of board
            # can't move right diagnolly, but can move left diagnolly
            elif [white_pawn_row_pos, white_pawn_char_pos] == [white_pawn_row_pos,size - 1]:
                # print([white_pawn_row_pos, white_pawn_char_pos], "cannot move right diagnolly, out of bounds")
                
                left_diagnol_space_char = white_pawn_char_pos - 1
                # print("L:", diagnol_space_row, left_diagnol_space_char)

                # though pawn is in the position to move left diagnolly
                # check if it actually can by checking if there is black pawn in that diagnol space
                if dup_board[diagnol_space_row][left_diagnol_space_char] == black_pawn:
                    # print("white pawn can move left diagnolly by capturing black pawn")

                    # convert the row the white pawn is in into a list so that updating its elements is possible
                    white_pawn_row_list = list(dup_board[white_pawn_row_pos])

                    # position where white pawn resides is going to now be empty
                    white_pawn_row_list[white_pawn_char_pos] = '-'
                    white_pawn_row = ''.join(white_pawn_row_list)

                    # update dup_board
                    dup_board[white_pawn_row_pos] = white_pawn_row
                    
                    left_diagnol_row_list = list(dup_board[diagnol_space_row])

                    # since there is a black pawn in left diagnol forward space, white pawn moves to that space and captures black pawn
                    left_diagnol_row_list[left_diagnol_space_char] = white_pawn
                    move_left_diagnolly = ''.join(left_diagnol_row_list)

                    # update dup_board
                    dup_board[diagnol_space_row] = move_left_diagnolly

                    if dup_board not in new_boards:
                        new_boards.append(dup_board)
                        dup_board = board[:]
            # case where white pawn is somewhere in the middle of board, thus can move left or right diagnolly
            else:
                left_diagnol_space_char = white_pawn_char_pos - 1
                right_diagnol_space_char = white_pawn_char_pos + 1
                # print("L:", diagnol_space_row, left_diagnol_space_char)
                # print("R:", diagnol_space_row, right_diagnol_space_char)

                if dup_board[diagnol_space_row][left_diagnol_space_char] == black_pawn:
                    # print("white pawn can move left diagnolly by capturing black pawn")

                    # convert the row the white pawn is in into a list so that updating its elements is possible
                    white_pawn_row_list = list(dup_board[white_pawn_row_pos])

                    # position where white pawn resides is going to now be empty
                    white_pawn_row_list[white_pawn_char_pos] = '-'
                    white_pawn_row = ''.join(white_pawn_row_list)

                    # update dup_board
                    dup_board[white_pawn_row_pos] = white_pawn_row
                    
                    left_diagnol_row_list = list(dup_board[diagnol_space_row])

                    # since there is a black pawn in left diagnol forward space, white pawn moves to that space and captures black pawn
                    left_diagnol_row_list[left_diagnol_space_char] = white_pawn
                    move_left_diagnolly = ''.join(left_diagnol_row_list)

                    # update dup_board
                    dup_board[diagnol_space_row] = move_left_diagnolly

                    if dup_board not in new_boards:
                        new_boards.append(dup_board)
                        dup_board = board[:]

                if dup_board[diagnol_space_row][right_diagnol_space_char] == black_pawn:
                    # print("white pawn can move right diagnolly by capturing black pawn")

                    # convert the row the white pawn is in into a list so that updating its elements is possible
                    white_pawn_row_list = list(dup_board[white_pawn_row_pos])

                    # position where white pawn resides is going to now be empty
                    white_pawn_row_list[white_pawn_char_pos] = '-'
                    white_pawn_row = ''.join(white_pawn_row_list)

                    # update dup_board
                    dup_board[white_pawn_row_pos] = white_pawn_row
                    
                    right_diagnol_row_list = list(dup_board[diagnol_space_row])
                    
                    # since there is a black pawn in right diagnol forward space, white pawn moves to that space and captures black pawn
                    right_diagnol_row_list[right_diagnol_space_char] = white_pawn
                    move_right_diagnolly = ''.join(right_diagnol_row_list)

                    # update dup_board
                    dup_board[diagnol_space_row] = move_right_diagnolly

                    if dup_board not in new_boards:
                        new_boards.append(dup_board)
                        dup_board = board[:]
                        
        # print("new_boards:", new_boards)
        return new_boards  
    else:
        # print("move black pawn diagnolly forward")
        # list that stores dictionaries of black_pawn position info
        black_pawn_arr = []

        for row in dup_board:
            for char_index, char in enumerate(row):
                if char == black_pawn:
                    # dictionary that stores the board row index a black pawn appears in
                    # and the char index the pawn appears in 
                    black_pawn_pos = {}
                    
                    row_index = dup_board.index(row)
                    
                    black_pawn_pos["row_pos"] = row_index
                    black_pawn_pos["char_pos"] = char_index
                    
                    black_pawn_arr.append(black_pawn_pos)

        # print("black_pawn_arr:", black_pawn_arr)

        for i in range(len(black_pawn_arr)):
            # print("black pawn", i, "row", black_pawn_arr[i]["row_pos"], "char index", black_pawn_arr[i]["char_pos"])
            black_pawn_row_pos = black_pawn_arr[i]["row_pos"]
            black_pawn_char_pos = black_pawn_arr[i]["char_pos"]

            # makes sure when black pawn gets to the end of board, it doesn't move diagnolly forward any further
            if black_pawn_row_pos != 0:
                diagnol_space_row = black_pawn_row_pos - 1
            else:
                # break when black pawn is at the end of board
                continue

            # case where black pawn is at the leftmost edge of board
            # can't move left diagnolly, but can move right diagnolly
            if [black_pawn_row_pos, black_pawn_char_pos] == [black_pawn_row_pos,0]:
                # print([black_pawn_row_pos, black_pawn_char_pos], "cannot move left diagnolly, out of bounds")
                
                right_diagnol_space_char = black_pawn_char_pos + 1
                # print("R:", diagnol_space_row, right_diagnol_space_char)
                
                # though pawn is in the position to move right diagnolly
                # check if it actually can by checking if there is white pawn in that diagnol space
                if dup_board[diagnol_space_row][right_diagnol_space_char] == white_pawn:
                    # print("black pawn can move right diagnolly by capturing white pawn")

                    # convert the row the black pawn is in into a list so that updating its elements is possible
                    black_pawn_row_list = list(dup_board[black_pawn_row_pos])

                    # position where black pawn resides is going to now be empty
                    black_pawn_row_list[black_pawn_char_pos] = '-'
                    black_pawn_row = ''.join(black_pawn_row_list)

                    # update dup_board
                    dup_board[black_pawn_row_pos] = black_pawn_row
                    
                    right_diagnol_row_list = list(dup_board[diagnol_space_row])

                    # since there is a white pawn in right diagnol forward space, black pawn moves to that space and captures white pawn
                    right_diagnol_row_list[right_diagnol_space_char] = black_pawn
                    move_right_diagnolly = ''.join(right_diagnol_row_list)

                    # update dup_board
                    dup_board[diagnol_space_row] = move_right_diagnolly

                    if dup_board not in new_boards:
                        new_boards.append(dup_board)
                        dup_board = board[:]
            # case where black pawn is at the rightmost edge of board
            # can't move right diagnolly, but can move left diagnolly
            elif [black_pawn_row_pos, black_pawn_char_pos] == [black_pawn_row_pos,size - 1]:
                # print([black_pawn_row_pos, black_pawn_char_pos], "cannot move right diagnolly, out of bounds")
                
                left_diagnol_space_char = black_pawn_char_pos - 1
                # print("L:", diagnol_space_row, left_diagnol_space_char)

                # though pawn is in the position to move left diagnolly
                # check if it actually can by checking if there is white pawn in that diagnol space
                if dup_board[diagnol_space_row][left_diagnol_space_char] == white_pawn:
                    # print("black pawn can move left diagnolly by capturing white pawn")

                    # convert the row the black pawn is in into a list so that updating its elements is possible
                    black_pawn_row_list = list(dup_board[black_pawn_row_pos])

                    # position where black pawn resides is going to now be empty
                    black_pawn_row_list[black_pawn_char_pos] = '-'
                    black_pawn_row = ''.join(black_pawn_row_list)

                    # update dup_board
                    dup_board[black_pawn_row_pos] = black_pawn_row
                    
                    left_diagnol_row_list = list(dup_board[diagnol_space_row])

                    # since there is a white pawn in left diagnol forward space, black pawn moves to that space and captures white pawn
                    left_diagnol_row_list[left_diagnol_space_char] = black_pawn
                    move_left_diagnolly = ''.join(left_diagnol_row_list)

                    # update dup_board
                    dup_board[diagnol_space_row] = move_left_diagnolly

                    if dup_board not in new_boards:
                        new_boards.append(dup_board)
                        dup_board = board[:]
            # case where black pawn is somewhere in the middle of board, thus can move left or right diagnolly
            else:
                left_diagnol_space_char = black_pawn_char_pos - 1
                right_diagnol_space_char = black_pawn_char_pos + 1
                # print("L:", diagnol_space_row, left_diagnol_space_char)
                # print("R:", diagnol_space_row, right_diagnol_space_char)

                if dup_board[diagnol_space_row][left_diagnol_space_char] == white_pawn:
                    # print("black pawn can move left diagnolly by capturing white pawn")

                    # convert the row the black pawn is in into a list so that updating its elements is possible
                    black_pawn_row_list = list(dup_board[black_pawn_row_pos])

                    # position where white pawn resides is going to now be empty
                    black_pawn_row_list[black_pawn_char_pos] = '-'
                    black_pawn_row = ''.join(black_pawn_row_list)

                    # update dup_board
                    dup_board[black_pawn_row_pos] = black_pawn_row
                    
                    left_diagnol_row_list = list(dup_board[diagnol_space_row])

                    # since there is a white pawn in left diagnol forward space, black pawn moves to that space and captures white pawn
                    left_diagnol_row_list[left_diagnol_space_char] = black_pawn
                    move_left_diagnolly = ''.join(left_diagnol_row_list)

                    # update dup_board
                    dup_board[diagnol_space_row] = move_left_diagnolly

                    if dup_board not in new_boards:
                        new_boards.append(dup_board)
                        dup_board = board[:]

                if dup_board[diagnol_space_row][right_diagnol_space_char] == white_pawn:
                    # print("black pawn can move right diagnolly by capturing white pawn")

                    # convert the row the black pawn is in into a list so that updating its elements is possible
                    black_pawn_row_list = list(dup_board[black_pawn_row_pos])

                    # position where white pawn resides is going to now be empty
                    black_pawn_row_list[black_pawn_char_pos] = '-'
                    black_pawn_row = ''.join(black_pawn_row_list)

                    # update dup_board
                    dup_board[black_pawn_row_pos] = black_pawn_row
                    
                    right_diagnol_row_list = list(dup_board[diagnol_space_row])
                    
                    # since there is a white pawn in right diagnol forward space, black pawn moves to that space and captures white pawn
                    right_diagnol_row_list[right_diagnol_space_char] = black_pawn
                    move_right_diagnolly = ''.join(right_diagnol_row_list)

                    # update dup_board
                    dup_board[diagnol_space_row] = move_right_diagnolly

                    if dup_board not in new_boards:
                        new_boards.append(dup_board)
                        dup_board = board[:]
        # print("new_boards:", new_boards)
        return new_boards  

def generate_new_states(board, size, next_player):
    '''
    move generator function
    main functionality is to generate new states by calling the operator functions

    - takes as args:
    --> board: a representation of the state of a hexapawn game (i.e. a board position)
    --> size: an integer representing the size of the board
    --> next_player: an indication as to which player is to move next 'w' or 'b'

    returns concatenated list of newly generated valid states
    '''
    move_forward_result = move_pawn_forward(board, size, next_player)
    move_diagnolly_result = move_pawn_diagnolly(board, size, next_player)

    #print("move_forward_result:", move_forward_result)
    #print("move_diagnolly_result:", move_diagnolly_result)

    return move_forward_result + move_diagnolly_result
    
def evaluation(board, size, next_player):
    '''
    - static board evaluation function
    - using the one shown in class
    - if MAX won then board value = +10
    - else if MIN won, then board value = -10
    - else board value = # of MAX'S pawns - # of MIN'S pawns

    - takes as args:
    --> board: a representation of the state of a hexapawn game (i.e. a board position)
    --> size: an integer representing the size of the board
    --> next_player: an indication as to which player is to move next 'w' or 'b'
    '''

    # result can either be 'w', 'b', or None
    win_checker_result = win_checker(board, size)

    if win_checker_result == maximizer:
        return 10
    elif win_checker_result == minimizer:
        return -10
    elif win_checker_result == "Stuck":
        if next_player == maximizer:
            return -10
        else:
            return 10
    elif win_checker_result == None:
        num_of_maximizer_pawns = 0
        num_of_minimizer_pawns = 0
        
        for row in board:
            for char in row:
                if char == maximizer:
                    num_of_maximizer_pawns += 1
                elif char == minimizer:
                    num_of_minimizer_pawns += 1
        return (num_of_maximizer_pawns - num_of_minimizer_pawns)

# HELPER FUNCTIONS
def win_checker(board, size):
    '''
    - takes as args:
    --> board: a representation of the state of a hexapawn game (i.e. a board position)
    --> size: an integer representing the size of the board

    - checks to see if there is a win on the board
    - if there is a win on the board, return which player won 'w' or 'b'
    - else return None

    - a player wins when:
    --> a player's pawn has advanced to the other end of the board
    --> the opponent has no pawns remaning on the board
    --> it is the opponent's turn to move a pawn but is unable to do so
    '''
    # check if black or white pawn has advanced to the other end of the board
    if white_pawn in board[size - 1]:
        # print("white wins, for it made it to the other end of board!")
        return white_pawn
    elif black_pawn in board[0]:
        # print("black wins, for it made it to the other end of board!")
        return black_pawn
    else:
        # check if there are any black or white pawns on the board
        # if no white pawns -> black wins
        # if no black pawns -> white wins
        # print("black wins, no more white pawns on board")
        num_of_white_pawns = 0
        num_of_black_pawns = 0
        
        for row in board:
            for char in row:
                if char == white_pawn:
                    num_of_white_pawns += 1
                elif char == black_pawn:
                    num_of_black_pawns += 1

        #print("num_of_white_pawns on board:", num_of_white_pawns)
        #print("num_of_black_pawns on board:", num_of_black_pawns)

        if num_of_white_pawns == 0:
            # print("black wins, no more white pawns on board")
            return black_pawn
        elif num_of_black_pawns == 0:
            # print("white wins, no more white pawns on board")
            return white_pawn
        else:
            # check if anybody is able to move by calling can_move_checker helper function
            can_move_result = can_move_checker(board, size)

            # if no one can move, either white or black pawn wins (depends on whose turn is next)
            if can_move_result == False:
                # print("someone wins, because pawns are stuck, no one can move")
                return "Stuck"
            else:
                # if got to this point, no one wins
                return None

def can_move_checker(board, size):
    '''
    - takes as args:
    --> board: a representation of the state of a hexapawn game (i.e. a board position)
    --> size: an integer representing the size of the board
    
    - does a simple analysis of the board and sees if anybody is able to move
    - doesn't move anything
    - returns True if somebody can move and returns False if nobody can move
    '''
    # list that stores dictionaries of white_pawn position info
    white_pawn_arr = []

    for row in board:
        for char_index, char in enumerate(row):
            if char == white_pawn:
                # dictionary that stores the board row index a white pawn appears in
                # and the char index the pawn appears in 
                white_pawn_pos = {}
                
                row_index = board.index(row)
                
                white_pawn_pos["row_pos"] = row_index
                white_pawn_pos["char_pos"] = char_index
                
                white_pawn_arr.append(white_pawn_pos)

    # print("white_pawn_arr:",white_pawn_arr)

    num_of_white_pawns_blocked = 0

    for i in range(len(white_pawn_arr)):
        # print("white pawn", i, "row", white_pawn_arr[i]["row_pos"], "char index", white_pawn_arr[i]["char_pos"])
        white_pawn_row_pos = white_pawn_arr[i]["row_pos"]
        white_pawn_char_pos = white_pawn_arr[i]["char_pos"]
        
        # for each white pawn, check if the space in front of them is empty or not
        forward_space_row = white_pawn_row_pos + 1
        forward_space_char = white_pawn_char_pos
        
        if board[forward_space_row][forward_space_char] != '-':
            blocking_char = board[forward_space_row][forward_space_char]
            # print("white pawn can't move forward, it is blocked by", blocking_char)
            num_of_white_pawns_blocked += 1

        '''
        - also check that the white pawn cannot move left/right diagnolly
        - can only move diagnolly left/right if there is a black pawn in that diagnol space
        
        - cannot move left diagnolly if:
        --> white pawn is on the leftmost edge of board (row[i][0])
        --> or left diagnol space is empty
        
        - cannot move right diagnolly if:
        --> white pawn is on the rightmost edge of board (row[i][size_of_board - 1])
        --> or right diagnol space is empty
        '''
        
        diagnol_space_row = white_pawn_row_pos + 1
        can_move_diagnolly = False

        # case where white pawn is at the leftmost edge of board
        # can't move left diagnolly, but can move right diagnolly
        if [white_pawn_row_pos, white_pawn_char_pos] == [white_pawn_row_pos,0]:
            # print([white_pawn_row_pos, white_pawn_char_pos], "cannot move left diagnolly, out of bounds")
            
            right_diagnol_space_char = white_pawn_char_pos + 1
            # print("R:", diagnol_space_row, right_diagnol_space_char)
            
            # though pawn is in the position to move right diagnolly
            # check if it actually can by checking if there is black pawn in that diagnol space
            if board[diagnol_space_row][right_diagnol_space_char] == black_pawn:
                # print("white pawn can move right diagnolly by capturing black pawn")
                can_move_diagnolly = True
        # case where white pawn is at the rightmost edge of board
        # can't move right diagnolly, but can move left diagnolly
        elif [white_pawn_row_pos, white_pawn_char_pos] == [white_pawn_row_pos,size - 1]:
            # print([white_pawn_row_pos, white_pawn_char_pos], "cannot move right diagnolly, out of bounds")
            
            left_diagnol_space_char = white_pawn_char_pos - 1
            # print("L:", diagnol_space_row, left_diagnol_space_char)

            # though pawn is in the position to move left diagnolly
            # check if it actually can by checking if there is black pawn in that diagnol space
            if board[diagnol_space_row][left_diagnol_space_char] == black_pawn:
                # print("white pawn can move left diagnolly by capturing black pawn")
                can_move_diagnolly = True
        # case where white pawn is somewhere in the middle of board, thus can move left or right diagnolly
        else:
            left_diagnol_space_char = white_pawn_char_pos - 1
            right_diagnol_space_char = white_pawn_char_pos + 1
            # print("L:", diagnol_space_row, left_diagnol_space_char)
            # print("R:", diagnol_space_row, right_diagnol_space_char)

            if board[diagnol_space_row][left_diagnol_space_char] == black_pawn:
                # print("white pawn can move left diagnolly by capturing black pawn")
                can_move_diagnolly = True

            if board[diagnol_space_row][right_diagnol_space_char] == black_pawn:
                # print("white pawn can move right diagnolly by capturing black pawn")
                can_move_diagnolly = True

    # print("num_of_white_pawns_blocked:", num_of_white_pawns_blocked)

    # if the num of white pawns blocked is equal to the board size and if no pawns can move diagnolly, no pawn can move
    if num_of_white_pawns_blocked == size and can_move_diagnolly == False:
        # return False because no pawn can move forward nor move diagnolly
        return False
    else:
        # return True because some pawn can move forward or move diagnolly
        return True
