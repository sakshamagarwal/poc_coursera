"""
Student facing implement of solitaire version of Mancala - Tchoukaillon
Goal: Move as many seeds from given houses into the store
In GUI, you make ask computer AI to make move or click to attempt a legal move
"""
#use this url to run in codeskulptor:
#http://www.codeskulptor.org/#user40_arJBKSIB4U_1.py

class SolitaireMancala:
    """
    Simple class that implements Solitaire Mancala
    """
    
    def __init__(self):
        """
        Create Mancala game with empty store and no houses
        """
        self.board = [0]
    
    def set_board(self, configuration):
        """
        Take the list configuration of initial number of seeds for given houses
        house zero corresponds to the store and is on right
        houses are number in ascending order from right to left
        """
        self.board = []
        for x in configuration:
            self.board.append(x)
        self.board.reverse()
    
    def __str__(self):
        """
        Return string representation for Mancala board
        """
        return str(self.board)
    
    def get_num_seeds(self, house_num):
        """
        Return the number of seeds in given house on board
        """
        return self.board[(len(self.board)-1)-house_num]

    def is_game_won(self):
        """
        Check to see if all houses but house zero are empty
        """
        for i in range(1,len(self.board)):
            if self.get_num_seeds(i) != 0:
                return False
        return True
    
    def is_legal_move(self, house_num):
        """
        Check whether a given move is legal
        """
        if house_num==0:
            return False
        elif self.board[(len(self.board)-1)-house_num]==house_num:
            return True
        else:
            return False

    
    def apply_move(self, house_num):
        """
        Move all of the stones from house to lower/left houses
        Last seed must be played in the store (house zero)
        """
        if self.is_legal_move(house_num):
            for i in range(0,house_num):
                self.board[(len(self.board)-1)-i] += 1
            self.board[(len(self.board)-1)-house_num] = 0

    def choose_move(self):
        """
        Return the house for the next shortest legal move
        Shortest means legal move from house closest to store
        Note that using a longer legal move would make smaller illegal
        If no legal move, return house zero
        """
        for i in range(0,len(self.board)):
            if self.is_legal_move(i):
                return i
        return 0
    
    def plan_moves(self):
        """
        Return a sequence (list) of legal moves based on the following heuristic: 
        After each move, move the seeds in the house closest to the store 
        when given a choice of legal moves
        Not used in GUI version, only for machine testing
        """
        new_board = SolitaireMancala()
        self.board.reverse()
        new_board.set_board(self.board)
        self.board.reverse()
        move_list = []
        next_move =  new_board.choose_move()
        while next_move != 0:
            new_board.apply_move(next_move)
            move_list.append(next_move)
            next_move = new_board.choose_move()
        return move_list
 

# Create tests to check the correctness of your code

def test_mancala():
    """
    Test code for Solitaire Mancala
    """
    
    my_game = SolitaireMancala()
    print "Testing init - Computed:", my_game, "Expected: [0]"
    
    config1 = [0, 0, 1, 1, 3, 5, 0]    
    my_game.set_board(config1)   
    
    print "Testing set_board - Computed:", str(my_game), "Expected:", str([0, 5, 3, 1, 1, 0, 0])
    print "Testing get_num_seeds - Computed:", my_game.get_num_seeds(1), "Expected:", config1[1]
    print "Testing get_num_seeds - Computed:", my_game.get_num_seeds(3), "Expected:", config1[3]
    print "Testing get_num_seeds - Computed:", my_game.get_num_seeds(5), "Expected:", config1[5]
    print my_game.plan_moves()
    """
    temp = 0
    for i in config1:
        print my_game.is_legal_move(temp)
        temp += 1
    my_game.apply_move(5)
    print str(my_game)
    my_game.apply_move(1)
    print str(my_game)
    my_game.apply_move(my_game.choose_move())
    print str(my_game)
    print my_game.choose_move()
    for i in range(0,7):
        my_game.apply_move(my_game.choose_move())
        print str(my_game)
        print my_game.is_game_won()
    """
    # add more tests here
    
#test_mancala()

# Import GUI code once you feel your code is correct
import poc_mancala_gui
poc_mancala_gui.run_gui(SolitaireMancala())