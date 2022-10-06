from game import *

# Set up
board = Board()
board.board[3,3] = np.array([RED, 1])
board.board[4,3] = np.array([RED, 1])
board.board[4,2] = np.array([RED, 1])
board.board[5,3] = np.array([RED, 1])
board.board[5,4] = np.array([RED, 1])

rug_red_1 = Rug(RED, (0,0), (1,0))
rug_blue_1 = Rug(BLUE, (1,1), (1,2))
rug_blue_2 = Rug(BLUE, (1,2), (2,2))

dice = 2

def test_pawn_set_position():
    pawn = Pawn()
    pawn.set_position(5,5)
    assert pawn.position.x == 5 and pawn.position.y == 5

def test_pawn_legal_orientations():
    pawn = Pawn()
    orientations = pawn.legal_orientations()
    expected_orientations = [NORTH, EAST, WEST]
    assert orientations == expected_orientations

def test_pawn_move_case_1():
    pawn = Pawn() # (3, 3, N)

    # NORTH
    new_orientation, new_x, new_y = pawn.legal_move(NORTH, 1)
    assert new_x == 3 and new_y == 4 and new_orientation == NORTH
    
    # EAST
    new_orientation, new_x, new_y = pawn.legal_move(EAST, 1)
    assert new_x == 4 and new_y == 3 and new_orientation == EAST
    
    ## WEST
    new_orientation, new_x, new_y = pawn.legal_move(WEST, 1)
    assert new_x == 2 and new_y == 3 and new_orientation == WEST

def test_pawn_move_case_2():
    pawn = Pawn() # (3, 3, N)

    # Bottom left corner (0, 0)
    pawn.set_position(0, 0)  
    new_orientation, new_x, new_y = pawn.legal_move(WEST, 1)
    assert new_x == 0 and new_y == 0 and new_orientation == NORTH

    # Top right corner (6, 6)
    pawn.set_position(4, 6)
    new_orientation, new_x, new_y = pawn.legal_move(EAST, 3)
    assert new_x == 6 and new_y == 6 and new_orientation == SOUTH
   
    # Bottom side
    pawn.set_position(3, 1)
    new_orientation, new_x, new_y = pawn.legal_move(SOUTH, 2)
    assert new_x == 4 and new_y == 0 and new_orientation == NORTH
    
    # Right side
    pawn.set_position(4, 2)
    new_orientation, new_x, new_y = pawn.legal_move(EAST, 3)
    assert new_x == 6 and new_y == 3 and new_orientation == WEST
    
    # Top side
    pawn.set_position(4, 6)
    new_orientation, new_x, new_y = pawn.legal_move(NORTH, 3)
    assert new_x == 5 and new_y == 4 and new_orientation == SOUTH
    
    # Left side
    pawn.set_position(1, 4)
    new_orientation, new_x, new_y = pawn.legal_move(WEST, 3)
    assert new_x == 1 and new_y == 3 and new_orientation == EAST
    
def test_get_nb_same_color_squares():
    n = board.pawn.get_nb_same_color_squares(board)
    assert n == 6