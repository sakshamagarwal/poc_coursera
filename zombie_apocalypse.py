"""
Student portion of Zombie Apocalypse mini-project
"""

#play at http://www.codeskulptor.org/#user40_DGbmaeU970_7.py
import random
import poc_grid
import poc_queue
import poc_zombie_gui

# global constants
EMPTY = 0 
FULL = 1
FOUR_WAY = 0
EIGHT_WAY = 1
OBSTACLE = 5
HUMAN = 6
ZOMBIE = 7


class Apocalypse(poc_grid.Grid):
    """
    Class for simulating zombie pursuit of human on grid with
    obstacles
    """

    def __init__(self, grid_height, grid_width, obstacle_list = None, 
                 zombie_list = None, human_list = None):
        """
        Create a simulation of given size with given obstacles,
        humans, and zombies
        """
        poc_grid.Grid.__init__(self, grid_height, grid_width)
        if obstacle_list != None:
            self._obstacle_list = list(obstacle_list)
            for cell in obstacle_list:
                self.set_full(cell[0], cell[1])
        else:
            self._obstacle_list = []
        if zombie_list != None:
            self._zombie_list = list(zombie_list)
        else:
            self._zombie_list = []
        if human_list != None:
            self._human_list = list(human_list)  
        else:
            self._human_list = []
        
    def __str__(self):
        res = poc_grid.Grid.__str__(self)
        res += "Humans: " + str(self._human_list) + "\nZombies: " + str(self._zombie_list)
        return res
    
    def clear(self):
        """
        Set cells in obstacle grid to be empty
        Reset zombie and human lists to be empty
        """
        poc_grid.Grid.clear(self)
        self._zombie_list = []
        self._human_list = []
        
    def add_zombie(self, row, col):
        """
        Add zombie to the zombie list
        """
        self._zombie_list.append((row, col))
                
    def num_zombies(self):
        """
        Return number of zombies
        """
        return len(self._zombie_list)   
          
    def zombies(self):
        """
        Generator that yields the zombies in the order they were
        added.
        """
        # replace with an actual generator
        for zombie in self._zombie_list:
            yield zombie

    def add_human(self, row, col):
        """
        Add human to the human list
        """
        self._human_list.append((row,col))
        
    def num_humans(self):
        """
        Return number of humans
        """
        return len(self._human_list)
    
    def humans(self):
        """
        Generator that yields the humans in the order they were added.
        """
        # replace with an actual generator
        for human in self._human_list:
            yield human
        
    def compute_distance_field(self, entity_type):
        """
        Function computes and returns a 2D distance field
        Distance at member of entity_list is zero
        Shortest paths avoid obstacles and use four-way distances
        """
        width = self.get_grid_width()
        height = self.get_grid_height()
        visited = poc_grid.Grid(height, width)
        distance_field = [[width * height for dummy_col in range(width)]
                          for dummy_row in range(height)]
        
        boundary = poc_queue.Queue()
        for obstacle in self._obstacle_list:
            visited.set_full(obstacle[0], obstacle[1])
        if (entity_type == HUMAN):
            for human in self._human_list:
                distance_field[human[0]][human[1]] = 0
                visited.set_full(human[0], human[1])
                boundary.enqueue(human)
        elif (entity_type == ZOMBIE):
            for zombie in self._zombie_list:
                distance_field[zombie[0]][zombie[1]] = 0
                visited.set_full(zombie[0], zombie[1])
                boundary.enqueue(zombie)
        
        while len(boundary)!=0:
            current_cell = boundary.dequeue()
            neighbor_cells = self.four_neighbors(current_cell[0],current_cell[1])
            for cell in neighbor_cells:
                if (visited.is_empty(cell[0], cell[1])):
                    visited.set_full(cell[0], cell[1])
                    boundary.enqueue(cell)
                    distance_field[cell[0]][cell[1]] = distance_field[current_cell[0]][current_cell[1]] + 1
        return distance_field
    
    def move_humans(self, zombie_distance_field):
        """
        Function that moves humans away from zombies, diagonal moves
        are allowed
        """
        temp = poc_grid.Grid(self.get_grid_height(), self.get_grid_width())
        for idx in range(len(self._human_list)):
            human = self._human_list[idx]
            neighbors = temp.eight_neighbors(human[0], human[1])
            safest_pos = human
            max_distance = zombie_distance_field[human[0]][human[1]]
            for position in neighbors:
                if ((zombie_distance_field[position[0]][position[1]] > max_distance) and self.is_empty(position[0], position[1])):
                    max_distance = zombie_distance_field[position[0]][position[1]]
                    safest_pos = position
            self._human_list[idx] = safest_pos
    
    def move_zombies(self, human_distance_field):
        """
        Function that moves zombies towards humans, no diagonal moves
        are allowed
        """
        temp = poc_grid.Grid(self.get_grid_height(), self.get_grid_width())
        for idx in range(len(self._zombie_list)):
            zombie = self._zombie_list[idx]
            neighbors = temp.four_neighbors(zombie[0], zombie[1])
            safest_pos = zombie
            min_distance = human_distance_field[zombie[0]][zombie[1]]
            for position in neighbors:
                if ((human_distance_field[position[0]][position[1]] < min_distance) and self.is_empty(position[0], position[1])):
                    min_distance = human_distance_field[position[0]][position[1]]
                    safest_pos = position
            self._zombie_list[idx] = safest_pos
    

poc_zombie_gui.run_gui(Apocalypse(30, 40))