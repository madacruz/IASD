from pickle import NEWOBJ_EX
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colors
from itertools import cycle, count
import random 

###########################
# --- GLOBAL VARIABLES ---
###########################

# Colors of the rugs
RED = 1 #player 1
BLUE = 2 #player 2
PINK = 3 #player 1
GREEN = 4 #player 2

colors = [RED, BLUE, PINK, GREEN]
color_cycle = cycle(colors)
#next(color_cycle) gives the next color to play

# Counters for each color to increment when instanciating new Rug, starts at 1
red_counter = count(1)
blue_counter = count(1)
pink_counter = count(1)
green_counter = count(1)

# Orientations of the pawn
NORTH = (0, 1)
SOUTH = (0, -1)
EAST = (1, 0)
WEST = (-1, 0)

orientations_int2str = {NORTH: "north", SOUTH: "south", EAST: "east", WEST: "west"}
colors_int2str = {RED: "red", BLUE: "blue", PINK: "pink", GREEN: "green"}

# U turns (demi tour) of the pawn
u_turn = {
    NORTH: SOUTH,
    SOUTH: NORTH,
    EAST: WEST,
    WEST: EAST,
}

####################
# --- FUNCTIONS ---
####################

def adjacent_coord(coord):
    """Returns all squares' coordinates (x', y') adjacent to square of coordinate `coord` (x, y)

    Args:
        coord (tuple of int): coordinate (x,y) of the square of interest

    Returns:
        list of tuples: list of adjacent positions
    """
    x, y = coord
    answer = []
    if -1 < x - 1 < 7:
        answer.append((x - 1, y))
    if -1 < x + 1 < 7:
        answer.append((x + 1, y))
    if -1 < y - 1 < 7:
        answer.append((x, y - 1))
    if -1 < y + 1 < 7:
        answer.append((x, y + 1))
    return answer

def next_color(color):
  next = ''
  if color == RED:
    next = BLUE
  elif color == BLUE:
    next = PINK
  elif color == PINK:
    next = GREEN
  elif color == GREEN:
    next = RED
  
  if next == '':
    print('The color is incorrect')

  return next
  
'''
def adjacent_coord(coord):
    """Returns all squares' coordinates (x', y') adjacent to square of coordinate `coord` (x, y)

    Args:
        coord (tuple of int): coordinate (x,y) of the square of interest

    Returns:
        list of tuples: list of adjacent positions
    """
    x, y = coord
    left = (x-1, y)
    right = (x+1, y)
    up = (x, y+1)
    down = (x, y-1)
    L = [left, right, up, down]

    if x == 0:
        L.remove(left)
    if y == 0:
        L.remove(down)
    if x == 6:
        L.remove(right)
    if y == 6:
        L.remove(up)

    return L
'''

##################
# --- CLASSES ---
##################

class Position(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return f'({self.x},{self.y})'

    def get_coord(self):
        return self.x, self.y

    def is_out_of_board(self, board_limit):
        """Check if the position of coordinates (x,y) is outside the board.
        
        Args:
            board_limit (int): board limit in terms of indices 
                               (e.g. if board is of size 7, then board_limit = 6)
        """

        if self.x < 0 or self.x > board_limit or self.y < 0 or self.y > board_limit:
            return True
        return False


class Rug(object):

    def __init__(self, color, sq1_pos, sq2_pos, incr=False):
        self.color = color
        self.sq1_pos = Position(sq1_pos[0], sq1_pos[1]) 
        self.sq2_pos = Position(sq2_pos[0], sq2_pos[1])
        if incr:
            self.id = self.increment_id()
        else:
            self.id = 0

    def __str__(self):
        return f"Rug {colors_int2str[self.color]} of id {self.id} at position ({self.sq1_pos}, {self.sq2_pos})."

    def increment_id(self):
        if self.color == RED:
            return next(red_counter)
        if self.color == BLUE:
            return next(blue_counter)
        if self.color == PINK:
            return next(pink_counter)
        if self.color == GREEN:
            return next(green_counter)

    def create_real(self, incr=True):
        rug_copy = Rug(self.color, self.sq1_pos.get_coord(), self.sq2_pos.get_coord(), incr)
        return rug_copy

class Pawn(object):
    def __init__(self):
        # The pawn start at the center of the board
        self.position = Position(3, 3)
        self.orientation = NORTH

    def __str__(self):
        result = f'({self.position}, {orientations_int2str[self.orientation]})'
        return result
    
    def set_position(self, x, y):
        self.position.x = x
        self.position.y = y

    def set_orientation(self, orientation):
        self.orientation = orientation

    def legal_orientations(self):
        # The pawn cannot make a u turn
        orientations = [NORTH, SOUTH, EAST, WEST]
        orientations.remove(u_turn[self.orientation])
        return orientations

    def legal_move(self, new_orientation, dice):

        #   Case 1: pawn does not go out from the board
        legal_x = self.position.x + new_orientation[0] * dice
        legal_y = self.position.y + new_orientation[1] * dice
        legal_position = Position(legal_x, legal_y)

        #   Case 2: pawn goes out from the board (implementation brute-force)
        if legal_position.is_out_of_board(board_limit=6): 
            # Count the number of steps left after moving out of the board
            # Place the pawn at the limit of the board
            if new_orientation == NORTH:
                steps_left = legal_y - 6
                legal_y = 6
            elif new_orientation == EAST:
                steps_left = legal_x - 6
                legal_x = 6
            elif new_orientation == SOUTH:
                steps_left = -legal_y
                legal_y = 0
            elif new_orientation == WEST:
                steps_left = -legal_x
                legal_x = 0

            # Place the pawn after it has moved out from the board 
            # It counts as a step
            new_orientation, legal_x, legal_y = self.get_move_in_board(new_orientation, legal_x, legal_y)
            steps_left = steps_left - 1
            
            # Move the pawn according to the number of steps left
            legal_x = legal_x + new_orientation[0] * steps_left
            legal_y = legal_y + new_orientation[1] * steps_left
        
        return new_orientation, legal_x, legal_y

    def get_move_in_board(self, orientation, x, y):
        """Get the new orientation and coordinates (new_x, new_y) of the pawn after moving out of the board."""
        # Bottom left corner (0,0)
        #to read again by mathilde
        if (x, y) == (0,0) and orientation == SOUTH:
            orientation = EAST
        elif (x, y) == (0,0) and orientation == WEST:
            orientation = NORTH
        # Top right corner (6,6)
        elif (x, y) == (6,6) and orientation == EAST:
            orientation = SOUTH
        elif (x, y) == (6,6) and orientation == NORTH:
            orientation = WEST
        # Bottom side (y = 0)
        elif orientation == SOUTH:
            x = x + 1 if x % 2 == 1 else x - 1
            orientation = NORTH
        # Right side (x = 6)
        elif orientation == EAST:
            y = y + 1 if y % 2 == 0 else y - 1
            orientation = WEST
        # Top side (y = 6)
        elif orientation == NORTH:
            x = x + 1 if x % 2 == 0 else x - 1
            orientation = SOUTH
        # Left side (x = 0)
        elif orientation == WEST:
            y = y + 1 if y % 2 == 1 else y - 1
            orientation = EAST
        return orientation, x, y

    def move(self, new_orientation, new_x, new_y):
        self.set_orientation(new_orientation)
        self.set_position(new_x, new_y)

    def get_nb_same_color_squares(self, board):
        """Compute the number of adjacents squares of the same color
        as the square's color on which the pawn is"""
        counter = 1 # Init to 1 because the initial square counts
        pawn_x, pawn_y = self.position.get_coord()
        pawn_color = board.get_color(pawn_x, pawn_y)

        coords_to_check = adjacent_coord((pawn_x, pawn_y))
        visited_coords = set((pawn_x, pawn_y))
        while coords_to_check:
            x, y = coords_to_check.pop(0)
            visited_coords.add((x, y))
            color = board.get_color(x, y)
            if color == pawn_color:
                counter += 1
                adj_coords = adjacent_coord((x,y))
                # Only append to coords_to_check not visited coords yet and of same color as the pawn
                for coord in adj_coords:
                    if coord not in visited_coords:
                        coords_to_check.append(coord)
        return counter

  
class Player(object):
    def __init__(self, id, colors):
        self.id = id
        self.colors = colors
        self.rugs_left = 24
        self.coins = 30
    
    def pay(self, amount, opponent_player):
        #I think that we should just focus on the 2 players game
        #If the player doesn't have enough money
        if self.coins - amount < 0:
            opponent_player.coins += self.coins
            self.coins = 0
        #If the player can pay
        else:
            self.coins -= amount
            opponent_player.coins += amount

    def score(self, board):
        # Sum of coins and the number of squares of the player's colors
        s = self.coins
        for x in range(board.size):
            for y in range(board.size):
                if board.board[x,y][0] in self.colors:
                    s += 1
        return s
  
class Move(object):
    def __init__(self, pawn, new_orientation, new_x, new_y, rug, dice):
        self.pawn = pawn
        self.new_orientation = new_orientation
        self.new_x = new_x
        self.new_y = new_y
        self.rug = rug
        self.dice = dice
        
    def __str__(self):
        
        if self.pawn.orientation == self.new_orientation:
            assam = f'The pawn stays in his orientation ({orientations_int2str[self.pawn.orientation]}).\n'
        else:
            assam = f'The pawn is reoriented from {orientations_int2str[self.pawn.orientation]} to {orientations_int2str[self.new_orientation]}.\n'
        assam_move = f'Assam is moving from {self.pawn.position.__str__()} to ({self.new_x},{self.new_y}).\n'
        tapis = f"A rug of color {colors_int2str[self.rug.color]} (id={self.rug.id}) is placed at ({self.rug.sq1_pos}, {self.rug.sq2_pos})."
        result = assam + assam_move + tapis
        return result
        
        #result = f'({orientations_int2str[self.new_orientation]}, ({self.new_x, self.new_y}), {self.rug})'
        #return result 

    def is_pawn_new_orientation_valid(self):
        # It is valid if no u-turn
        return self.new_orientation in self.pawn.legal_orientations()

    def is_pawn_new_position_valid(self):
        _, legal_x, legal_y = self.pawn.legal_move(self.new_orientation, self.dice)
        return self.new_x == legal_x and self.new_y == legal_y

    def is_rug_adjacent_to_pawn(self):
        # Check if adjacent to pawn and also not on the pawn's position

        # List of all valid coordinates around the pawn
        x, y = self.new_x, self.new_y
        init_valid_coord = adjacent_coord((x, y))
        valid_coord = init_valid_coord.copy()
        for coord in init_valid_coord:
            valid_coord.extend(adjacent_coord(coord))
        set_valid_coord = set(valid_coord)
        set_valid_coord.remove((x, y))

        # Check if the rug's both squares are in the set
        if self.rug.sq1_pos.get_coord() and self.rug.sq2_pos.get_coord() in set_valid_coord:
            return True
        return False

    def is_rug_covering_another_rug(self, board):
        # Rug's new placement is valid if it doesn't cover another rug
        # We need to check if the both squares are covered by the same rug (same color and same id)
        sq1_color_and_id = board.board[self.rug.sq1_pos.x, self.rug.sq1_pos.y]
        sq2_color_and_id = board.board[self.rug.sq2_pos.x, self.rug.sq2_pos.y]
        if not np.array_equal(sq1_color_and_id, np.zeros(2)) and np.array_equal(sq1_color_and_id, sq2_color_and_id):
            return True
        return False

    def valid(self, board):
        #print(self.is_pawn_new_orientation_valid(), self.is_pawn_new_position_valid(), self.is_rug_adjacent_to_pawn(), self.is_rug_covering_another_rug(board)) 
        if not self.is_pawn_new_orientation_valid():
            return False
        elif not self.is_pawn_new_position_valid():
            return False
        elif not self.is_rug_adjacent_to_pawn():
            return False
        elif self.is_rug_covering_another_rug(board):
            return False
        return True

class Board(object):
    def __init__(self, size=7, verbose=False):
        self.size = size
        self.board = np.zeros((size, size, 2))
        self.pawn = Pawn() # Initialize at (3,3)
        self.players = [Player(0, [RED, PINK]), Player(1, [BLUE, GREEN])]
        self.current_player = self.players[0]
        self.current_color = RED # Start with first color of first player
        self.verbose=verbose
        self.nb_turns = 1

        self.cycle_players = cycle(players)
        
    def __str__(self):
        #print(self.board)
        pass

    def throw_dice(self):
        dice = [1, 2, 2, 3, 3, 4]
        return random.choice(dice)

    def get_color(self, x, y):
        """Get the color of the square (x,y)"""
        return self.board[x,y][0]

    def get_number(self, x, y):
        """Get the number of the square (x,y)"""
        return self.board[x,y][1]

    def legal_moves(self, dice):
        """Get list of legal moves among 4x49x12 possible moves.

        - Orientation (4, including 3 valid)
        - Pawn movement (49, including 1 valid according to the orientation and dice's result)
        - Rug placement (12, including ? according to the pawn and other rugs' position)

        """
        moves = [] # List of all possible valid moves

        # For every orientation
        for orientation in [NORTH, SOUTH, EAST, WEST]:
            # For every position in the board
            for x in range(7):
                for y in range(7):
                    # For every square around the pawn
                    for sq1_coord in adjacent_coord((x, y)):
                        # For every square around those squares
                        for sq2_coord in adjacent_coord(sq1_coord):
                            rug_notreal = Rug(self.current_color, sq1_coord, sq2_coord)
                            m = Move(self.pawn, orientation, x, y, rug_notreal, dice)
                            # Check if the move is legal
                            if m.valid(self):
                                # If yes, add to moves
                                moves.append(m)
        return moves

    def score(self):
        # We can think the score as player1's score - player2's score
        # Such that if it's positive, player 1 wins, if negative player 2 wins 
        player1_score = self.players[0].score(self)
        player2_score = self.players[1].score(self)
        return player1_score - player2_score

    def terminal(self):
        total = 0
        for player in self.players:
            total += player.rugs_left
        if total == 0:
            return True
        return False

    def play(self, move):
        
        move.rug = move.rug.create_real()
        if self.verbose:
          print(move.__str__())

        # 1. Orientate and move the pawn
        self.pawn.move(move.new_orientation, move.new_x, move.new_y)

        # 2. Place a rug
        self.board[move.rug.sq1_pos.x, move.rug.sq1_pos.y] = np.array([move.rug.color, move.rug.id])
        self.board[move.rug.sq2_pos.x, move.rug.sq2_pos.y] = np.array([move.rug.color, move.rug.id])
        self.current_player.rugs_left -= 1

        # 3. Pay opponent
        # Pay only if the pawn is on an opponent color
        current_square_color = self.get_color(self.pawn.position.x, self.pawn.position.y)
        opponent_player_id = abs(self.current_player.id - 1)
        if self.verbose:
            if current_square_color:
                print(f'The players ends on a {colors_int2str[current_square_color]} rug.')
            else:
                print(f'The player ends on an empty case.')
        #very important : the player only have to pay if he is on an opponent rug ! not if it is an empty case !
        if current_square_color:
            if current_square_color not in self.current_player.colors:
                amount = self.pawn.get_nb_same_color_squares(self)
                if self.verbose:
                    print(f'This rug belongs to player {self.players[opponent_player_id].id}.')
                    print(f'The current player has to give him {amount} coins.')
                self.current_player.pay(amount, self.players[opponent_player_id])
            else:
                if self.verbose:
                    print("The rug is his so he doesn't have to pay.")
        if self.verbose:
            print(f'Player {self.players[0].id} has {self.players[0].coins} coins. Player {self.players[1].id} has {self.players[1].coins}.')
          
        # Change turn
        self.current_player = self.players[opponent_player_id]
        #self.current_payer = next(self.cycle_players)
        self.current_color = next_color(self.current_color)

    def playout(self):
        """Play a random game from the current state.
        Returns the result of the random game."""

        while(True):
            # Throw the dice for the current player
            dice_result = self.throw_dice()
            #We get all the legal moves for this dice result
            moves = self.legal_moves(dice=dice_result)

            # If the game is over
            if self.terminal():
                # Victory for player 1
                if self.score() < 0:
                    if self.verbose:
                        print("Player 1 wins !!!")
                    return -1
                # Victory for player 0
                elif self.score() > 0:
                    if self.verbose:
                        print("Player 0 wins !!!")
                    return 1
                # Draw
                else:
                    if self.verbose:
                        print("Draw...")
                    return 0
            
            if self.verbose:
              print(f'{self.nb_turns}.')
              print(f'Player {self.current_player.id} throws the dice. The result is {dice_result}.')

            # The game isn't over: rugs are remaining
            # We play another move chosen randomly
            n = random.randint(0, len(moves)-1)
            self.play(moves[n])
            self.nb_turns+=1
            if self.verbose:
                print('\n')