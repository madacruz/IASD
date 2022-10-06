from game import *


# Set up
board = Board()
board.board[0,0] = np.array([RED, 1])
board.board[1,0] = np.array([RED, 1])
board.board[1,1] = np.array([BLUE, 1])
board.board[1,2] = np.array([BLUE, 2]) # cover blue 1
board.board[2,2] = np.array([BLUE, 2])

rug_red_1 = Rug(RED, Position(0,0), Position(1,0))
rug_blue_1 = Rug(BLUE, Position(1,1), Position(1,2))
rug_blue_2 = Rug(BLUE, Position(1,2), Position(2,2))

dice = 2

def test_is_pawn_new_orientation_valid():
    m = Move(board.pawn, SOUTH, rug_red_1, dice)
    assert m.is_pawn_new_orientation_valid() == False 

def test_is_rug_adjacent_to_pawn():
    rug = Rug(RED, Position(2,3), Position(1,3))
    m = Move(board.pawn, EAST, rug, dice)
    assert m.is_rug_adjacent_to_pawn() == True

    rug = Rug(RED, Position(5,3), Position(6,3))
    m = Move(board.pawn, EAST, rug, dice)
    assert m.is_rug_adjacent_to_pawn() == False 

def test_is_rug_covering_another_rug():
    rug = Rug(RED, Position(1,1), Position(1,2))
    m = Move(board.pawn, EAST, rug, dice)
    assert m.is_rug_covering_another_rug(board) == False

    rug = Rug(RED, Position(1,0), Position(1,1))
    m = Move(board.pawn, EAST, rug, dice)
    assert m.is_rug_covering_another_rug(board) == False

    rug = Rug(RED, Position(0,0), Position(1,0))
    m = Move(board.pawn, EAST, rug, dice)
    assert m.is_rug_covering_another_rug(board) == True
