"""
Loyd's Fifteen puzzle - solver and visualizer
Note that solved configuration has the blank (zero) tile in upper left
Use the arrows key to swap this tile with its neighbors
"""

#play at http://www.codeskulptor.org/#user40_kPACZC6YX2wEO8R.py
import poc_fifteen_gui

class Puzzle:
    """
    Class representation for the Fifteen puzzle
    """

    def __init__(self, puzzle_height, puzzle_width, initial_grid=None):
        """
        Initialize puzzle with default height and width
        Returns a Puzzle object
        """
        self._height = puzzle_height
        self._width = puzzle_width
        self._grid = [[col + puzzle_width * row
                       for col in range(self._width)]
                      for row in range(self._height)]

        if initial_grid != None:
            for row in range(puzzle_height):
                for col in range(puzzle_width):
                    self._grid[row][col] = initial_grid[row][col]

    def __str__(self):
        """
        Generate string representaion for puzzle
        Returns a string
        """
        ans = ""
        for row in range(self._height):
            ans += str(self._grid[row])
            ans += "\n"
        return ans

    #####################################
    # GUI methods

    def get_height(self):
        """
        Getter for puzzle height
        Returns an integer
        """
        return self._height

    def get_width(self):
        """
        Getter for puzzle width
        Returns an integer
        """
        return self._width

    def get_number(self, row, col):
        """
        Getter for the number at tile position pos
        Returns an integer
        """
        return self._grid[row][col]

    def set_number(self, row, col, value):
        """
        Setter for the number at tile position pos
        """
        self._grid[row][col] = value

    def clone(self):
        """
        Make a copy of the puzzle to update during solving
        Returns a Puzzle object
        """
        new_puzzle = Puzzle(self._height, self._width, self._grid)
        return new_puzzle

    ########################################################
    # Core puzzle methods

    def current_position(self, solved_row, solved_col):
        """
        Locate the current position of the tile that will be at
        position (solved_row, solved_col) when the puzzle is solved
        Returns a tuple of two integers        
        """
        solved_value = (solved_col + self._width * solved_row)

        for row in range(self._height):
            for col in range(self._width):
                if self._grid[row][col] == solved_value:
                    return (row, col)
        assert False, "Value " + str(solved_value) + " not found"

    def update_puzzle(self, move_string):
        """
        Updates the puzzle state based on the provided move string
        """
        zero_row, zero_col = self.current_position(0, 0)
        for direction in move_string:
            if direction == "l":
                assert zero_col > 0, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row][zero_col - 1]
                self._grid[zero_row][zero_col - 1] = 0
                zero_col -= 1
            elif direction == "r":
                assert zero_col < self._width - 1, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row][zero_col + 1]
                self._grid[zero_row][zero_col + 1] = 0
                zero_col += 1
            elif direction == "u":
                assert zero_row > 0, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row - 1][zero_col]
                self._grid[zero_row - 1][zero_col] = 0
                zero_row -= 1
            elif direction == "d":
                assert zero_row < self._height - 1, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row + 1][zero_col]
                self._grid[zero_row + 1][zero_col] = 0
                zero_row += 1
            else:
                assert False, "invalid direction: " + direction

    ##################################################################
    # Phase one methods

    def lower_row_invariant(self, target_row, target_col):
        """
        Check whether the puzzle satisfies the specified invariant
        at the given position in the bottom rows of the puzzle (target_row > 1)
        Returns a boolean
        """
        if (self._grid[target_row][target_col] != 0):
            return False
        for row in range(target_row + 1, self.get_height()):
            for col in range(0, self.get_width()):
                if self.current_position(row,col) != (row, col):
                    return False
        for col in range(target_col+1, self.get_width()):
            if self.current_position(target_row, col) != (target_row, col):
                return False
        return True

    def solve_interior_tile(self, target_row, target_col):
        """
        Place correct tile at target position
        Updates puzzle and returns a move string
        """

        result = ""
        
        while (self.current_position(target_row, target_col)[0] < self.current_position(0,0)[0]):
            self.update_puzzle('u')
            result += 'u'
        
        if (self.current_position(target_row, target_col)[1] > self.current_position(0,0)[1]):
            while (self.current_position(target_row, target_col)[1] > self.current_position(0,0)[1]):
                self.update_puzzle('r')
                result += 'r'
        else:
            while (self.current_position(target_row, target_col)[1] < self.current_position(0,0)[1]):
                self.update_puzzle('l')
                result += 'l'
        
        if (self.current_position(0,0)[0] != (target_row - 1)):
            while (self.current_position(target_row, target_col)[1] != target_col):
                if (self.current_position(target_row, target_col)[1] > target_col):
                    self.update_puzzle('dllur')
                    result += 'dllur'
                else:
                    self.update_puzzle('drrul')
                    result += 'drrul'
        else:
            while (self.current_position(target_row, target_col)[1] != target_col):
                if (self.current_position(target_row, target_col)[1] > target_col):
                    self.update_puzzle('dllur')
                    result += 'urrdl'
                else:
                    self.update_puzzle('urrdl')
                    result += 'urrdl'
            
        
        if (self.current_position(0,0)[1] > self.current_position(target_row, target_col)[1]):
            if (self.current_position(0,0)[0] != (target_row - 1)):
                self.update_puzzle('dllu')
                result += 'dllu'
            else:
                self.update_puzzle('ulld')
                result += 'ulld'
        
        #assert self.current_position(target_row, target_col)[0] == self.current_position(0,0)[0]
        #assert self.current_position(target_row, target_col)[1] == self.current_position(0,0)[1] + 1
        #assert (self.current_position(target_row, target_col)[1] == target_col)
        
        if (self.current_position(target_row, target_col)[0] == (self.current_position(0,0)[0] + 1)):
            while (self.current_position(target_row, target_col)[0] != target_row):
                self.update_puzzle('lddru')
                result += 'lddru'
            self.update_puzzle('ld')
            result += 'ld'
        while (self.current_position(target_row, target_col)[0] != target_row):
            self.update_puzzle('druld')
            result += 'druld'
            
        #assert self.current_position(target_row, target_col) == (target_row, target_col)
        
        return result

    def solve_col0_tile(self, target_row):
        """
        Solve tile in column zero on specified row (> 1)
        Updates puzzle and returns a move string
        """
        result = ''
        if (self.current_position(target_row, 0) == (target_row-1, 0)):
            self.update_puzzle('u')
            result += 'u'
        else:
            while (self.current_position(target_row, 0)[0] < self.current_position(0,0)[0]):
                self.update_puzzle('u')
                result += 'u'
            
            if (self.current_position(target_row, 0)[1] != 0):
                while (self.current_position(0,0)[1] < self.current_position(target_row, 0)[1]):
                    self.update_puzzle('r')
                    result += 'r'
                    
                while (self.current_position(target_row, 0)[1] != 0):
                    if (self.current_position(0,0)[0] == 0):
                        self.update_puzzle('dllur')
                        result += 'dllur'
                    else:
                        self.update_puzzle('ulldr')
                        result += 'ulldr'
                        
            else:
                self.update_puzzle('rd')
                result += 'rd'
       
            while (self.current_position(target_row, 0)[0] != target_row - 1):
                self.update_puzzle('dlurd')
                result += 'dlurd'
                assert self.current_position(target_row, 0)[1] == 0
            
            self.update_puzzle('dluurddluruldrdlurdlu')
            result += 'dluurddluruldrdlurdlu'
        for dummy_col in range(self.get_width() - 1):
                self.update_puzzle('r')
                result += 'r'
        return result

    #############################################################
    # Phase two methods

    def row0_invariant(self, target_col):
        """
        Check whether the puzzle satisfies the row zero invariant
        at the given column (col > 1)
        Returns a boolean
        """
        
        if (self.current_position(0,0) != (0, target_col)):
            return False
        for col in range(target_col + 1, self.get_width()):
            if self.current_position(0, col) != (0,col):
                return False
            if self.current_position(1, col) != (1,col):
                return False
        if self.current_position(1, target_col) != (1,target_col):
            return False
        for row in range(2, self.get_height()):
            for col in range(self.get_width()):
                if self.current_position(row, col) != (row, col):
                    return False
        return True

    def row1_invariant(self, target_col):
        """
        Check whether the puzzle satisfies the row one invariant
        at the given column (col > 1)
        Returns a boolean
        """
        if (self.current_position(0,0) != (1, target_col)):
            return False
        for col in range(target_col + 1, self.get_width()):
            if self.current_position(0, col) != (0,col):
                return False
            if self.current_position(1, col) != (1,col):
                return False
        for row in range(2, self.get_height()):
            for col in range(self.get_width()):
                if self.current_position(row, col) != (row, col):
                    return False
        return True

    def solve_row0_tile(self, target_col):
        """
        Solve the tile in row zero at the specified column
        Updates puzzle and returns a move string
        """
        result = ''
        if (self.current_position(0,target_col) == (0, target_col - 1)):
            self.update_puzzle('ld')
            return 'ld'
        elif (self.current_position(0,target_col) == (1, target_col - 1)):
            self.update_puzzle('lldurdlurrdluldrruld')
            return 'lldurdlurrdluldrruld'
        if (self.current_position(0,target_col)[0] == 0):
            while (self.current_position(0, target_col)[1] < self.current_position(0,0)[1]):
                self.update_puzzle('l')
                result += 'l'
            while (self.current_position(0,target_col)[1] != target_col - 1):
                self.update_puzzle('drrul')
                result += 'drrul'
            self.update_puzzle('druld')
            result += 'druld'
            self.update_puzzle('urdlurrdluldrruld')
            result += 'urdlurrdluldrruld'
        else:
            while (self.current_position(0,0)[1] > self.current_position(0, target_col)[1]):
                self.update_puzzle('l')
                result += 'l'
            self.update_puzzle('rdl')
            result += 'rdl'
            while (self.current_position(0, target_col)[1] < target_col - 1):
                self.update_puzzle('urrdl')
                result += 'urrdl'
            self.update_puzzle('urdlurrdluldrruld')
            result += 'urdlurrdluldrruld'
        return result

    def solve_row1_tile(self, target_col):
        """
        Solve the tile in row one at the specified column
        Updates puzzle and returns a move string
        """
        #print self
        result = ''
        if (self.current_position(1, target_col)[0] == 1):
            while (self.current_position(0,0)[1] > self.current_position(1,target_col)[1]):
                self.update_puzzle('l')
                result += 'l'
            while (self.current_position(1, target_col)[1] != target_col):
                self.update_puzzle('urrdl')
                result += 'urrdl'
            self.update_puzzle('ur')
            result += 'ur'
        else:
            self.update_puzzle('u')
            result += 'u'
            while (self.current_position(0,0)[1] > self.current_position(1,target_col)[1]):
                self.update_puzzle('l')
                result += 'l'
            while (self.current_position(1, target_col)[1] != target_col):
                self.update_puzzle('drrul')
                result += 'drrul'
            if self.current_position(1, target_col)[0] == 0:
                self.update_puzzle('dru')
                result += 'dru' 
        return result
        

    ###########################################################
    # Phase 3 methods

    def solve_2x2(self):
        """
        Solve the upper left 2x2 part of the puzzle
        Updates the puzzle and returns a move string
        """
        result = ''
        moves = ['r', 'd', 'l', 'u']
        if self.current_position(0,0) == (0,0):
            count = 0
        elif self.current_position(0,0) == (0,1):
            count = 1
        elif self.current_position(0,0) == (1,1):
            count = 2
        else:
            count = 3
        while not (self.current_position(0,0) == (0,0) and self.current_position(0,1) == (0,1) and self.current_position(1,0) == (1,0) and self.current_position(1,1) == (1,1)):
            self.update_puzzle(moves[count%4])
            result += moves[count%4]
            count += 1
        return result

    def solve_puzzle(self):
        """
        Generate a solution string for a puzzle
        Updates the puzzle and returns a move string
        """
        result = ''
        while self.current_position(0,0)[0] != self.get_height() - 1:
            self.update_puzzle('d')
            result += 'd'
        while self.current_position(0,0)[1] != self.get_width() - 1:
            self.update_puzzle('r')
            result += 'r'
        row = self.get_height() - 1
        while row > 1:
            col = self.get_width() - 1
            while col > 0:
                result += self.solve_interior_tile(row, col)
                col -= 1
            result += self.solve_col0_tile(row)
            row -= 1
        col = self.get_width() - 1
        while col > 1:
            result += self.solve_row1_tile(col)
            result += self.solve_row0_tile(col)
            col -= 1
        result += self.solve_2x2()
        return result

# Start interactive simulation
poc_fifteen_gui.FifteenGUI(Puzzle(4, 4))
#obj = obj = Puzzle(4, 5, [[12, 11, 10, 9, 8], [7, 6, 5, 4, 3], [2, 1, 0, 13, 14], [15, 16, 17, 18, 19]])
#print obj.lower_row_invariant(2, 2)
#obj = Puzzle(4, 5, [[12, 11, 10, 9, 15], [7, 6, 5, 4, 3], [2, 1, 8, 13, 14], [0, 16, 17, 18, 19]])
#obj.solve_col0_tile(3)
#obj = Puzzle(4, 5, [[1, 2, 0, 3, 4], [6, 5, 7, 8, 9], [10, 11, 12, 13, 14], [15, 16, 17, 18, 19]])
#print obj.solve_row0_tile(2)
