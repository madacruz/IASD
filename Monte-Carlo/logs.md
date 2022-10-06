# Logs

## 10/06/22

__DONE__

In `game.py`:

- Creation of counters (starting at 1) for each color, automatically incremented when we instanciate a new Rug of a particular color. For example:
  - Rug(RED, ...) -> 1
  - Rug(BLUE, ...) -> 1
  - Rug(RED, ...) -> 2
- `Move.valid()`
  - if-else statements because there is a hierarchy of errors. We need to satisfy a certain condition before checking the next condition. For example, need to check if the new orientation of the pawn is valid before checking if the rug is well placed, since it depends on the pawn orientation
  - 4 inner methods for clarity
- Creation of a `Position` class 
  - Why? Because we needed to check if a position (x,y) was inside or outside the board several times. It is a simple *if* statement (`x < 0 or x > 6 or y < 0 or y > 6`). We write it as a method of the class.
  - Changes in `Pawn` class. From `self.x`, `self.y` to `self.position` and then we can refer to the coordinates with`self.position.x` and `self.position.y`. Modifications in all methods accordingly.
  - In `Rug` class, we keep the position of the first and second squares separately
- `Board` class
  - `self.board` from a 2D-matrix to a 3D-matrix to assign to each square of the board an array([rug_color, rug_id]), where rug_color=0 means empty square. 
  
__TODO__

- [x] Test `Pawn.move()` --> 11/06/22
- [x] Test `Move.valid()` --> 11/06/22
- [x] How to deal with the dice? --> 11/06/22

## 11/06/22

- Function `adjacent_coord()`. For coordinates on the board's frontiers, only returns coordinates that are not out of the board. 
  - So we don't need to check if a rug will be out of board in `Move.valid()`
- How do we deal with the stochastic event during a player's turn (the dice)?
  - In the course's example, `play()` function corresponds to the whole turn of a player, and at the end, the turn is changed to the other player. But in our case, to deal with the stochastic event, in `play()` only the deterministic move (orientation, place the rug) and in `playout()`, we throw the dice, move the pawn and pay the opponent. 
- Pay opponent
  - Keep track of the current player -> Add in `Board` class, `self.players` which is a list of all the players (`Player` objects)
  - Compute the number of adjacents squares of the same color as the square's color on which the pawn is, in `get_nb_same_color_squares()` of `Pawn`. 
- `Board.terminal()`
  - Add in `Player` an attribute `rugs_left` (initialized at 30) which we decrement each time a rug of its color is placed (in the `play()` method).
  - If all players have no more rugs left to place, then the game is over.
- `Board.score()`
  - Add in `Player` a `score()` function
  - Used to compute the score of the game

__TODO__
- [ ] Board visualization
- [ ] Test the whole modelisation

--> Once the tests completed and we are good with the modelisation, let's start MCTS!
Bonus: a pygame UI ;)

## 14/06/22

- Check if a pawn placement is valid or not among the 7x7 possible placements in the board.

# Terms

- "Coordinates" = tuple of int (x,y)
- "Position" = object of class `Position` with attributes `x` and `y`