"""
Clone of 2048 game.
"""
import random
import poc_2048_gui

# Directions, DO NOT MODIFY
UP = 1
DOWN = 2
LEFT = 3
RIGHT = 4

# Offsets for computing tile indices in each direction.
# DO NOT MODIFY this dictionary.
OFFSETS = {UP: (1, 0),
           DOWN: (-1, 0),
           LEFT: (0, 1),
           RIGHT: (0, -1)}

def merge(line):
    """
    Function that merges a single row or column in 2048.
    """
    result_list = []
    for	element in line:
        if element!=0:
            result_list.append(element)
    size = len(result_list)
    for	idx in range(len(result_list),len(line)):
        result_list.append(0)
    result_list.append(0)
    for idx in range(0,size):
        if (result_list[idx]==result_list[idx+1]):
            result_list[idx] += result_list[idx+1]
            for jdx in range(idx+1,size):
                result_list[jdx] = result_list[jdx+1]
    result_list.pop()
    return result_list

class TwentyFortyEight:
    """
    Class to run the game logic.
    """

    def __init__(self, grid_height, grid_width):
        self.height = grid_height
        self.width = grid_width
        self.reset()

    def reset(self):
        """
        Reset the game so the grid is empty except for two
        initial tiles.
        """
        self.grid = [[0 for dummy_x in range(self.width)]
                     for dummy_y in range(self.height)]
        self.new_tile()
        self.new_tile()

    def __str__(self):
        """
        Return a string representation of the grid for debugging.
        """
        # replace with your code
        return str(self.grid)

    def get_grid_height(self):
        """
        Get the height of the board.
        """
        # replace with your code
        return self.height

    def get_grid_width(self):
        """
        Get the width of the board.
        """
        # replace with your code
        return self.width

    def move(self, direction):
        """
        Move all tiles in the given direction and add
        a new tile if any tiles moved.
        """
        # replace with your code
        pass

    def new_tile(self):
        """
        Create a new tile in a randomly selected empty
        square.  The tile should be 2 90% of the time and
        4 10% of the time.
        """
        # replace with your code
        empty_cells = []
        for idx in range(self.height):
            for jdx in range(self.width):
                if self.grid[idx][jdx]==0:
                    empty_cells.append((idx,jdx))
        new_place = random.choice(empty_cells)
        if random.random() < 0.9:
            self.grid[new_place[0]][new_place[1]] = 2
        else:
            self.grid[new_place[0]][new_place[1]] = 4
            

    def set_tile(self, row, col, value):
        """
        Set the tile at position row, col to have the given value.
        """
        # replace with your code
        pass

    def get_tile(self, row, col):
        """
        Return the value of the tile at position row, col.
        """
        # replace with your code
        return self.grid[row][col]

print TwentyFortyEight(5,4)
poc_2048_gui.run_gui(TwentyFortyEight(5, 4))
