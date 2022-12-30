import copy
import random
import numpy as np

class SudokuState:
    def __init__(self, sudoku):
        
        ## current broad state
        self.final_values = sudoku
        
        ## possible values for this state, initialized 9x9 grid by empty list
        self.possible_values = [[list() for _ in range(0, 9)] for _ in range(0, 9)]
        
        ## loop through current broad state to create possible values
        for (row, col), value in np.ndenumerate(self.final_values):
            # if value not set
            if value == 0: 
                for i in range(1, 10):
                    # check if this value is valid
                    if self.is_valid_value(row, col, i):
                        self.possible_values[row][col].append(i)
        
    def get_possible_values(self):
        return self.possible_values.copy()
    
    """ 
    get the row and col which have no final value but exactly 1 possible value
    
    return list of tuple, (int, int)
    """
    def get_singleton_cell(self):
        return [(row, col) for (row, col), values in np.ndenumerate(self.possible_values)
                if len(values) == 1 and self.final_values[row][col] == 0]
    
    """
    check is current state has possible values
    
    return bool
    """
    def has_possible_values(self):
        for (row, col), value in np.ndenumerate(self.final_values):
            # if state has value not yet assigned and has no possible values
            if value == 0 and len(self.possible_values[row][col]) == 0:
                return False
            
        return True
        
    """ 
    check is current state is a goal state
    
    return bool
    """
    def is_goal(self):            
#         return self.is_valid_state() and not(0 in self.final_values)
        return not (0 in self.final_values)
    
    """
    check is current state is a valid state
    
    return bool
    """
    def is_valid_state(self):
        # loop through all cell in the state
        for (row, col), value in np.ndenumerate(self.final_values):
            if not self.is_valid_value(row, col, value):
                return False
        return True
    
    """ 
    check the value is valid to specific cell
    used for construct possible values and state validation
    
    param int
    param int
    param int
    return bool
    """
    def is_valid_value(self, row, col, value):
        # value 0 is valid for successor state
        if value == 0:
            return True
        
        # check row and col
        for i in range(9):
            ## check row
            if value == self.final_values[row][i] and col != i:
                return False
            ## check col
            if value == self.final_values[i][col] and row != i:
                return False
        
        # check 3x3
        block_row_start = row - (row % 3)
        block_col_start = col - (col % 3)
        ## loop through all cell in block
        for block_row in range(3):
            for block_col in range(3):                
                ### check value does exists in 3x3 and not checking the same target cell, return false
                if self.final_values[block_row_start + block_row][block_col_start + block_col] == value \
                and (block_row_start + block_row) != row \
                and (block_col_start + block_col) != col:
                    return False
        
        return True
    
    """
    Returns a new state with this column set to this row, and the change propagated to other domains
    
    param int
    param int
    param int
    return SudokuState
    """
    def set_value(self, row, col, value):
        if value not in self.possible_values[row][col]:
            raise ValueError(f"value {value} is not a valid choice in {row}, {col}")
        
        new_state = copy.deepcopy(self)
        
        # assign value to cell
        new_state.final_values[row][col]    = value
        new_state.possible_values[row][col] = []
            
        # update other cell
        new_state.update_possible_values(row, col, value)
        
        # update singleton cell
        singleton_cell = new_state.get_singleton_cell()
        while len(singleton_cell) > 0:
            (row, col) = singleton_cell[0]
        
            ## assign value to cell
            singleton_value                     = new_state.possible_values[row][col][0]
            new_state.final_values[row][col]    = singleton_value
            new_state.possible_values[row][col] = []
            
            ## update other cell
            new_state.update_possible_values(row, col, singleton_value)
            
            ## refresh singleton cell, coz possible values might be updated
            singleton_cell = new_state.get_singleton_cell()
            
        return new_state    
            
    """
    Update all other cells possible values
    
    param int
    param int
    param int
    return void
    """
    def update_possible_values(self, row, col, value):
        for i in range(9):
            # remove from the same row
            if value in self.possible_values[row][i]:
                self.possible_values[row][i].remove(value)
                
            # remove from the same col
            if value in self.possible_values[i][col]:
                self.possible_values[i][col].remove(value)
        
        # remove from the same block
        block_row_start = row - (row % 3)
        block_col_start = col - (col % 3)
        for block_row in range(3):
            for block_col in range(3):                
                if value in self.possible_values[block_row_start + block_row][block_col_start + block_col]:
                    self.possible_values[block_row_start + block_row][block_col_start + block_col].remove(value)
        
        return

"""
using depth first search to deal with sudoku state
"""        
def depth_first_search(sudoku_state):
    (row, col) = pick_next_cell(sudoku_state)
    values     = pick_next_values(sudoku_state, row, col)
    
    for value in values:
        new_state = sudoku_state.set_value(row, col, value)
        
        if new_state.is_goal():
            return new_state
        if new_state.has_possible_values():
            deep_state = depth_first_search(new_state)
            if deep_state is not None and deep_state.is_goal():
                return deep_state
    return None

"""
randomly pick the next search cell from sudoku state

param SudokuState
return tuple, (int, int)
"""
def pick_next_cell(sudoku_state):
    # random pick
#     next_cells = [(row, col) for (row, col), values in np.ndenumerate(sudoku_state.possible_values) if len(values) >= 1]
#     return random.choice(next_cells)

    # pick the less possible values
    less_cell = []
    for (row, col), values in np.ndenumerate(sudoku_state.possible_values):
        # has possible values
        if (len(values) > 0):
            if (len(less_cell) == 0):
                less_cell = [row, col]
            elif (len(values) < len(sudoku_state.possible_values[less_cell[0]][less_cell[1]])):
                less_cell = [row, col]
    return less_cell

"""
randomly pick the next assign value from sudoku state

param SudokuState
param int
param int
return list of int
"""
def pick_next_values(sudoku_state, row, col):
    possible_values = sudoku_state.get_possible_values()
    values          = possible_values[row][col]
    random.shuffle(values)
    return values
    
def sudoku_solver(sudoku):
    """
    Solves a Sudoku puzzle and returns its unique solution.

    Input
        sudoku : 9x9 numpy array
            Empty cells are designated by 0.

    Output
        9x9 numpy array of integers
            It contains the solution, if there is one. If there is no solution, all array entries should be -1.
    """
    ### YOUR CODE HERE
    initial_state = SudokuState(sudoku)
    no_solution = [[-1 for _ in range(9)] for _ in range(9)]
    
    # check sudoku state is valid
    if not initial_state.is_valid_state():
        return no_solution
    
    # check sudoku state is goal
    if initial_state.is_goal():
        return initial_state.final_values
    
    final_state = depth_first_search(initial_state)
    if not final_state:
        return no_solution
    
    return final_state.final_values
