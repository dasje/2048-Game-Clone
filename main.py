"""
Clone of 2048 game.
Must be played through codeskulptor.com in order to make use of the simplegui library.
"""

import poc_2048_gui
import random, math

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
    Helper function that merges a single row or column in 2048
    """
    length_of_list = len(line)
    temp_list_1 = []
    temp_list_2 = []
    for index in range(length_of_list):
        if line[index] > 0:
            temp_list_1.append(line[index])
    for index in range(length_of_list):
        if line[index] == 0:
            temp_list_1.append(line[index])
    # check is first two items in list are same,
    # add to new list if so and pop from original list
    # try/except for odd numbered lists
    while temp_list_1:
        try:
            if temp_list_1[0] == temp_list_1[1]:
                temp_list_2.append(temp_list_1[0] * 2)
                for dummy_task in range(2):
                    temp_list_1.pop(0)
            elif temp_list_1[0] != temp_list_1[1]:
                temp_list_2.append(temp_list_1[0])
                temp_list_1.pop(0)
        except IndexError:
            temp_list_2.append(temp_list_1.pop(0))
    # add missing zeroes to return list
    for dummy_number in range(length_of_list - len(temp_list_2)):
        temp_list_2.append(0)
    return temp_list_2


class TwentyFortyEight:
    """
    Class to run the game logic.
    """

    def __init__(self, grid_height, grid_width):
        self._grid_height = grid_height
        self._grid_width = grid_width
        self._grid = []
        self._grid_dict = {UP: [[0, col] for col in range(self._grid_width)],
                           DOWN: [[self._grid_height - 1, col] for col in range(self._grid_width)],
                           LEFT: [[row, 0] for row in range(self._grid_height)],
                           RIGHT: [[row, self._grid_width - 1] for row in range(self._grid_height)]}
        self.reset()

    def reset(self):
        """
        Reset the game so the grid is empty except for two
        initial tiles.
        """
        self._grid = [[0 for dummy_col in range(self._grid_width)]
                      for dummy_row in range(self._grid_height)]
        for dummy_task in range(2):
            self.new_tile()

    def __str__(self):
        """
        Return a string representation of the grid for debugging.
        """
        returned_string = ""
        for row in self._grid:
            returned_string = returned_string + str(row) + '\n'
        return returned_string

    def get_grid_height(self):
        """
        Get the height of the board.
        """
        return self._grid_height

    def get_grid_width(self):
        """
        Get the width of the board.
        """
        return self._grid_width

    def move(self, direction):
        """
        Move all tiles in the given direction and add
        a new tile if any tiles moved.
        """
        # reset grid_dict
        self.reset_grid_dict()
        dict_list = self._grid_dict[direction]
        offset = OFFSETS[direction]
        range_var = 0
        if direction == LEFT or direction == RIGHT:
            range_var = self._grid_width
        if direction == UP or direction == DOWN:
            range_var = self._grid_height
        temp_grid = []
        temp_line = []
        for coords in dict_list:
            for dummy_item in range(range_var):
                temp_line.append(self._grid[coords[0]][coords[1]])
                coords[0] += offset[0]
                coords[1] += offset[1]
            temp_grid.append(temp_line)
            temp_line = []
        temp_list = []
        for line in temp_grid:
            new_line = merge(line)
            for num in new_line:
                temp_list.append(num)
        self.reset_grid_dict()
        dict_list = self._grid_dict[direction]
        counter = 0
        for coords in dict_list:
            for dummy_item in range(range_var):
                self._grid[coords[0]][coords[1]] = temp_list[counter]
                coords[0] += offset[0]
                coords[1] += offset[1]
                counter += 1
        self.new_tile()

    def reset_grid_dict(self):
        """
        Reset the grid dictionary.
        """
        self._grid_dict = {UP: [[0, col] for col in range(self._grid_width)],
                           DOWN: [[self._grid_height - 1, col] for col in range(self._grid_width)],
                           LEFT: [[row, 0] for row in range(self._grid_height)],
                           RIGHT: [[row, self._grid_width - 1] for row in range(self._grid_height)]}

    def new_tile(self):
        """
        Create a new tile in a randomly selected empty
        square.  The tile should be 2 90% of the time and
        4 10% of the time.
        """
        # make one list of bools to earmark 0's
        zero_list = []
        for row in self._grid:
            for column in row:
                if column == 0:
                    zero_list.append(True)
                else:
                    zero_list.append(False)  # tested, works
        # if zero is present:
        if True in zero_list:
            zero_bools = []  # list of booleans marking where zeros are
            counter = 0
            for zero_bool in zero_list:
                if zero_bool == True:
                    zero_bools.append(counter)
                counter += 1
            new_index = random.choice(zero_bools)  # select random zero-index
            row_in_grid = ((new_index + self._grid_width) / self._grid_width) - 1  # get zero row location
            # rows counted from zero
            column_in_grid = new_index % self._grid_width  # get zero column location
            # columns counted from zero
            chance_of_2 = random.random()
            # ensure that 10% of the time the random number is 4
            if chance_of_2 < 0.9:
                self._grid[row_in_grid][column_in_grid] = 2
            elif chance_of_2 > 0.9:
                self._grid[row_in_grid][column_in_grid] = 4

        else:
            pass

    def set_tile(self, row, col, value):
        """
        Set the tile at position row, col to have the given value.
        """
        self._grid[row][col] = value

    def get_tile(self, row, col):
        """
        Return the value of the tile at position row, col.
        """
        return self._grid[row][col]


poc_2048_gui.run_gui(TwentyFortyEight(4, 4))