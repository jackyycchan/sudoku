# Sudoku Solver
## Introduction
This is an agent for solving 9x9 Sudoku Puzzles by using **BackTracking Search**, which is combing **Depth First Search (DFS)** and **Constraint Propagation**. Besides, optimization on picking next cell to start was applied in order to provide extra speed up on the searching.
### Sudoku Puzzle
Sudoku is a logic-based, combinatorial number-placement puzzle. In classic Sudoku, the objective is to fill a 9 × 9 grid with digits so that each column, each row, and each of the nine 3 × 3 subgrids that compose the grid contain all of the digits from 1 to 9.
### Methodology
Sudoku can be modeled as Constraint Satification Problem as it is a set of value assigned into multiple variables under constraints [^2].

Constraint Satification Problems can be presented by following:
- X={X<sub>1</sub>, X<sub>2</sub>, ..., X<sub>n</sub>} is a set of variables.
- D={D<sub>1</sub>, D<sub>2</sub>, ..., D<sub>n</sub>} is a set of domains specifying the values each variable can take.
- C is a set of constraints that specifies the values that the variables are allowed to have collectively.

For Sudoku puzzles, we can derive the below information by Constraint Satification Problems definition:
- X={R<sub>0</sub>C<sub>0</sub>, R<sub>0</sub>C<sub>1</sub>, R<sub>0</sub>C<sub>2</sub>, ..., R<sub>8</sub>C<sub>8</sub>} is a set of possible variables (cell)
- D={1, 2, 3, ..., 9} is a set of domains that describing the values can be assigned to each variables
- "Value can only appears on the same row and column and 3x3 block of grid once"

## Detail of Implementation
As mentioned, this solver is using **BackTracking Search** to solve the sudoku puzzles. **Backtracking Search** is a mixture of **Depth First Search (DFS)** and **Constraint Propagation**. **DFS** starts at root node and explore as deepest as possible along each branch before backtracking. In each iteration, an empty cell will be pick up and testing for all possible values. If state is a complete assignment, it will be returned directly as a goal state. If state is a partial assignment, it will explore to next node for the next search.
### State
Sudoku state is representing by `SudokuState`. `SudokuState` contains its current state `final_values` which is an 2-D array for representing current assignment of values. Secondly, `SudokuState` use `possible_values` to contain all the possible values of empty cell. `final_values` and `possible_values` will be created once `SudokuState` is being constructed.
### Constraint Satisfaction
`SudokuState` is able to deal with all the constraints by its `is_valid_value` function. It will check for below constraints. 
- True if Value is equal to zero, zero is a valid case.
- False if Value appear on the same row > 1 
- False if Value appear on the same column > 1
- False if Value appear on a 3x3 block of grid > 1
- True otherwise

### Depth First Search
### test
A valid state is assumed to be passed into `depth_first_search`. `depth_first_search` will first pick up an empty cell (`pick_next_cell`) and the list of possible values of that empty cell (`pick_next_values`). By making use of the list of possible values, it starts to explore as deepest as possible along each possible values. For each iteration, a new value will be assigned to that empty cell by calling `SudokuState.set_value()`, and then a new `SudokuState` will be returned. Base on this new state, if it is already a complete state (`SudokuState.is_goal()`), it will be returned directly. Otherwise, it will be passed to next iteration for further next cell assignment by calling `depth_first_search` recursively until a complete state is found or no more assignment is avaliable.
### Optimization
As mentioned, for each iteration, an empty cell is pick up randomly from the state. However, it is not a desirable way to start with. It makes the search takes longer time to finish if a cell which has many possible values in it is pick up. It affects the hard level sudoku state the most, normally it takes more than 30s to finish the searching. The most extreme case is more than 4 mins. Therefore, an optimization is carried out on `pick_next_cell` function. The aim is to return the cell which contains the fewest possible values. As a result, the searching performance improved significantly from nearly 4 mins to within 10s.

## References
[^1] https://medium.com/my-udacity-ai-nanodegree-notes/solving-sudoku-think-constraint-satisfaction-problem-75763f0742c9
[^2] Simonis, H., 2005, October. Sudoku as a constraint problem. In CP Workshop on modeling and reformulating Constraint Satisfaction Problems (Vol. 12, pp. 13-27). Citeseer.