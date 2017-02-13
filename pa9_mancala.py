##################################
# 15110 Principles of Computing  #
# PA9: Mancala                   #                  
# Fall 2016                      #
##################################


# ~ Imports ~ #
import tkinter
from tkinter import Canvas
from random import randint, seed
from time import sleep

# ~ Global Variables ~ #
# [ DO NOT MODIFY! ] 

BOARD_WIDTH = 360
BOARD_HEIGHT = 720
BOARD_MARGIN = 30

HOUSE_WIDTH = 135
HOUSE_HEIGHT = 60
STORE_WIDTH = 300
STORE_HEIGHT = 90
X_MARGIN = 30
Y_MARGIN = 15
HOUSE_PADDING = 10
STORE_PADDING = 15
X_COUNT_MARGIN = 15
Y_COUNT_MARGIN = 30

PEBBLE_RADIUS = 10
ID_RADIUS = 10

"""
###########################
# ~ Let's play Mancala! ~ #
###########################
"""

WINDOW = tkinter.Tk()
CANVAS = Canvas(WINDOW, width=BOARD_WIDTH, height=BOARD_HEIGHT)
CANVAS.pack()


# ~ Tkinter custom circle function ~ #
def _create_circle(self, x, y, r, **kwargs):
    return self.create_oval(x-r, y-r, x+r, y+r, **kwargs)

tkinter.Canvas.create_circle = _create_circle


#########
# MODEL #
#########

# Creates a list representing a new board at the start of the game.
# @return {list} Represents the start state of the board 
def new_board(): 
    board = [4, 4, 4, 4, 4, 4, 0, 4, 4, 4, 4, 4, 4, 0]
    return board

# Returns the moves available to the given player according to the state of
# the board. A player can only choose a house on his side of the board which
# is not empty. 
# @param board {list} Represents pebbles in each pit on board
# @param player {int} Player, can either be 0 or 1
# @return {list} Pits available for the player to pick 
def get_available_moves(board, player):
    available_move_list = [] #list of available moves
    if player == 0:
        for i in range(0,6): #player 0 pit
            if board[i] > 0:
                available_move_list.append(i)
    else:
        for i in range(7,13): #player 1 pit
            if board[i] > 0:
                available_move_list.append(i)
    return available_move_list
 
# Returns the Pit index of the given player's store
# @param player {int} Player, can either be 0 or 1
# @return {int} Pit index of player's store
def get_player_store(player):
    if player == 0:
        return 6
    else:
        return 13

# Returns True if pit is a house on the player's side of the board
# @param player {int} Player, can either be 0 or 1
# @param pit {int} Pit index to evaluate
# @return {bool} True if pit is a house on player's side of the board
def is_player_house(player, pit):
    if pit < 6 and player == 0:
        return True
    elif pit in range(7,13) and player == 1:
        return True
    else:
        return False
    
# Returns False if there are no pebbles in any of the houses on the player's 
# side of the board.
# @param board {list} Mancala board model
# @param player {int} Player, can only be 0 or 1
# @return {bool} False if player has no valid move to make
def has_move(board, player):
    x = []
    if player == 0:
        for i in range(0,6): #player 0 pit
            x.append(board[i])
        if sum(x) > 0: #any pit has a pebble
            return True
        else:
            return False
    else:
        for i in range(7,13): #player 1 pit
            x.append(board[i])
        if sum(x) > 0: #any pit has a pebble
            return True
        else:
            return False

# Returns True if the match has ended.
# @param board {list} Board model
# @return {bool} True if match has ended
def is_end_match(board):
    if has_move(board,0) or has_move(board,1): #at least one player has a move
        return False
    else:
        return True

# Prints feedback to let the players know the result of the match
# @param board {list} Board model
# @return {None}
def finish_match(board):
    if is_end_match(board):
        if board[6] > board[13]:
            print('Congratulations! Player 0 Wins!')
            return
        elif board[6] < board[13]:
            print('Congratulations! Player 1 Wins!')
            return
        else:
            print('Great game. It\'s a tie!')


########
# VIEW #
########

# Returns drawing bounds of given pit.
# @param {int} Pit index
# @return {list} Drawing bounds of pit as [left, top, right, bottom]
def get_pit_coords(pit):
    # If pit is in right column
    # CALCULATE PIT DIMENSIONS FROM BOTTOM UP
    if (0 <= pit <= 5):
        # Left side of right column
        left = BOARD_MARGIN + HOUSE_WIDTH + X_MARGIN
        right = left + HOUSE_WIDTH
        # Bottom edge of player0 side of board, i.e. the bottom edge of the 
        # houses at the bottom of the board
        side0_baseline = BOARD_HEIGHT - (BOARD_MARGIN + STORE_HEIGHT + Y_MARGIN)
        # If pit is in bottom half (side0) of board
        if (pit <= 2): # (pits 0-2)
            bottom = side0_baseline - (HOUSE_HEIGHT * pit) - (Y_MARGIN * pit)
            top = bottom - HOUSE_HEIGHT
        # If pit is in top half (side1) of board
        else: # (pits 3-5)
            # Subtract extra Y_MARGIN to previous calculation 
            bottom = (side0_baseline - Y_MARGIN) - (HOUSE_HEIGHT * pit) - (Y_MARGIN * pit)
            top = bottom - HOUSE_HEIGHT
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~        
    elif (7 <= pit <= 12):
        left = BOARD_MARGIN
        right = left + HOUSE_WIDTH
        side1_topline = BOARD_MARGIN + STORE_HEIGHT + Y_MARGIN
        if (pit <= 9): 
            pit -= 7 
            top = side1_topline + (HOUSE_HEIGHT * pit) + (Y_MARGIN * pit)
            bottom = top + HOUSE_HEIGHT
        else: 
            pit -= 7 
            top = (side1_topline + Y_MARGIN) + (HOUSE_HEIGHT * pit) + (Y_MARGIN * pit)
            bottom = top + HOUSE_HEIGHT
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~        
    else: 
        left = BOARD_MARGIN
        right = left + STORE_WIDTH
        if (pit == 6): 
            top = BOARD_MARGIN
            bottom = top + STORE_HEIGHT 
        else: 
            bottom = BOARD_HEIGHT - BOARD_MARGIN
            top = bottom - STORE_HEIGHT
    return [left, top, right, bottom]

# Returns random drawing center coordinates of a pebble placed within bounds of 
# given pit.
# @param {int} Pit index
# @return {int list} Random center coordinates as [center_x, center_y]
def get_pebble_coords(pit):
    pit_coords = get_pit_coords(pit)
    L = pit_coords[0]
    T = pit_coords[1]
    R = pit_coords[2]
    B = pit_coords[3]
    if pit == 6 or pit == 13:
        center_x = randint(L + PEBBLE_RADIUS + STORE_PADDING, R - PEBBLE_RADIUS - STORE_PADDING)
        center_y = randint(T + PEBBLE_RADIUS + STORE_PADDING, B - PEBBLE_RADIUS - STORE_PADDING)
    else:
        center_x = randint(L + PEBBLE_RADIUS + HOUSE_PADDING, R - PEBBLE_RADIUS - HOUSE_PADDING)
        center_y = randint(T + PEBBLE_RADIUS + HOUSE_PADDING, B - PEBBLE_RADIUS - HOUSE_PADDING)
    return [center_x, center_y]

# ~ DO NOT DELETE PROVIDED LINES OF CODE ~
# Draws the entire board display based on the model.
# @param {list} Board model
# return {None}
def display_board(board):
    CANVAS.delete(tkinter.ALL) # DO NOT REMOVE
    seed(15110) # DO NOT REMOVE
    # Draw board body
    CANVAS.create_rectangle(0,0,BOARD_WIDTH,BOARD_HEIGHT,fill='#996633')
    
    # Draw all store and house pits 
    for pit in range(0, 14):
        coords = get_pit_coords(pit)
        if pit == 6 or pit == 13: #stores
            draw_pit(coords[0],coords[1],coords[2],coords[3],STORE_PADDING)
        else: #houses
            draw_pit(coords[0],coords[1],coords[2],coords[3],HOUSE_PADDING)

    # Draw pebble counts for each pit
    for pit in range(0,14):
        draw_pebble_count(board,pit)

    # Draw pebbles in each pit
    for pit in range(0,14):
        for pebble in range(0,board[pit]):
            x = get_pebble_coords(pit)
            draw_pebble(x[0],x[1])
    
    # Draw pit id
    # at the end so pebbles don't overlap
    for pit in range(0,14):
        draw_pit_id(pit)
            
    sleep(0.2) # DO NOT REMOVE
    WINDOW.update() # DO NOT REMOVE

# GRAPHICAL ELEMENT DRAW FUNCTIONS - DO NOT EDIT THIS CODE        
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Draw one pit.
# @params left, top, right, bottom {int} Dimensions of pit
# @param padding {int} Width of pit padding (HOUSE_PADDING or STORE_PADDING)
# @return {None}
def draw_pit(left, top, right, bottom, padding): 
    CANVAS.create_rectangle(left, top, right, bottom, fill='#634321', width=0)
    CANVAS.create_line(left, top, left+padding, top+padding, fill='#4F361A')
    CANVAS.create_line(right, bottom, right-padding, bottom-padding, fill='#4F361A')
    CANVAS.create_line(right, top, right-padding, top+padding, fill='#4F361A')
    CANVAS.create_line(left, bottom, left+padding, bottom-padding, fill='#4F361A')
    CANVAS.create_rectangle(left, top, right, bottom, fill=None, outline='#966C43')
    CANVAS.create_rectangle(left+padding, top+padding, right-padding, bottom-padding, fill='#704B25', outline='#4F361A')


# Draw pit ID.
# @params pit {int} ID of house
# return {None}
def draw_pit_id(pit):
    coords = get_pit_coords(pit)
    center_x = coords[0] + ID_RADIUS
    center_y = coords[1] + ID_RADIUS
    if pit <= 6:
        CANVAS.create_circle(center_x,center_y,ID_RADIUS,fill = 'green')
    else:
        CANVAS.create_circle(center_x,center_y,ID_RADIUS,fill = 'yellow')
    CANVAS.create_text(center_x, center_y, text = pit, anchor = 'center')


# Draw one pebble.
# @params center_x, center_y {int} Center coordinates for pebble
# return {None}
def draw_pebble(center_x, center_y):
    CANVAS.create_circle(center_x, center_y, PEBBLE_RADIUS, fill='#A01F1F', outline='DarkRed')
    CANVAS.create_circle(center_x, center_y, PEBBLE_RADIUS, fill='FireBrick', width=0)
    CANVAS.create_circle(center_x+4, center_y-4, 1.5, fill='GhostWhite', width=0)

# Draw one pebble count for pit next to pit on board.
# @param board {list} Board model
# @param pit {pit} Pit for which to draw count
# return {None}
def draw_pebble_count(board, pit):
    pit_coors = get_pit_coords(pit)
    (left, top) = (pit_coors[0], pit_coors[1])
    (right, bottom) = (pit_coors[2], pit_coors[3])
    if (pit < 7): # Pits in the right column have pebble counts drawn on right
                  # of pit
        x = right + X_COUNT_MARGIN
        y = top + Y_COUNT_MARGIN
    else: # Pits in left column have pebble counts drawn on left of pit
        x = left - X_COUNT_MARGIN
        y = top + Y_COUNT_MARGIN
    count = str(board[pit])
    CANVAS.create_text(x, y, text=count, anchor="center")

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# END GRAPHICAL ELEMENT DRAW FUNCTIONS 


##############
# CONTROLLER #
##############

# Allows players to interact with the terminal to pick the pits 
def pick_pit(board, player):
     #TODO: Read the code and edit two lines by implementing get_available_moves(board, player)
    while True: 
        print("-----It is player " + str(player) + "'s turn.-----")
        # Edit the following line
        valid_pits = get_available_moves(board,player)
        
        pit = input("Pick a pit number {} to sow pebbles: ".format(valid_pits))
        if (pit == "quit"):
            break
        else: 
            try: pit = int(pit)
            except:
                print("Please provide a valid integer.")
                continue
        if (not is_player_house(player, pit)):
            print("Input is not a valid pit. Pick a pit {}.".format(valid_pits))
        elif (board[pit] == 0):
            print("There are no pebbles in the pit that you have chosen. Please pick a valid pit.")
        else: 
            break
    return pit

# Given a valid pit, distribute the pebbles in pit one at a time to subsequent 
# pits taking into account the player, meaning that the function should skip 
# the opponent's store. 
# @param pit {int} Pit from which pebbles are distributed
# @param board {list} Board model 
# @param player {int} Player (0 or 1)
# @return {(list,int)} tuple of updated board state and
#  last pit to receive a pebble
def distribute_pebbles(pit, board, player):
    j = board[pit]
    board[pit] = 0
    if player == 0:
        while j > 0:
            pit += 1
            if pit == 13:
                pit = 0
            board[pit] += 1
            j = j - 1
    else:
        while j > 0:
            pit += 1
            if pit == 14:
                pit = 0
            elif pit == 6:
                pit = 7
            board[pit] += 1
            j = j - 1
    return (board, pit)

# Runs a turn for one player move.
# @param pit {int} Pit index at which to start turn (i.e. start by distributing)
#                  pebbles from this pit
# @param board {list} Board model at the start of the turn
# @param player {int} Player, can only be 0 or 1
# @return {(list, bool)} Board model at the end of the turn,
#  bool of whether player takes another turn
def run_turn(pit, board, player):
    if distribute_pebbles(pit, board, player)[1] == get_player_store(player):
        return (board,True)
    else:
        return (board,False)
    

# Switches current player to opponent if opponent has move to make and returns
# new current player. 
# @param player {int} Original player
# @return {int} New current player (0 or 1)
def switch_player(player):
    if player == 0:
        player = 1
    else:
        player = 0
    return player
    

# Quits the game by printing feedback to user and destroying Tkinter window.
# @return {None}
def quit_game():
    print("Goodbye!")
    try: WINDOW.destroy()  
    except: return None


# Starts and runs game until player quits. 
# @return {None}
def run_game():
    board = new_board()
    display_board(board)
    player = 0
    while is_end_match(board) == False:
        while has_move(board, player) == True:
            pit = pick_pit(board, player)
            if pit == 'quit':
                quit_game()
            else:
                if run_turn(pit, board, player)[1] == False:
                    run_turn(pit, board, player)
                    player = switch_player(player)
                else:
                    run_turn(pit, board, player)
            display_board(board)
        player = switch_player(player)
        while has_move(board, player) == True:
            pit = pick_pit(board, player)
            run_turn(pit, board, player)
            display_board(board)
    return finish_match(board)



