"""
Monte Carlo Tic-Tac-Toe Player
"""

#play at http://www.codeskulptor.org/#user40_0IACtiEglK_0.py

import random
import poc_ttt_gui
import poc_ttt_provided as provided

# Constants for Monte Carlo simulator
# You may change the values of these constants as desired, but
#  do not change their names.
NTRIALS = 1000         # Number of trials to run
SCORE_CURRENT = 1.0 # Score for squares played by the current player
SCORE_OTHER = 1.0   # Score for squares played by the other player
    
# Add your functions here.
def mc_trial(board, player):
    """plays a random game on board with player to move next"""
    while(board.check_win() == None):
        blankies = board.get_empty_squares()
        target = random.choice(blankies)
        board.move(target[0],target[1],player)
        if player == provided.PLAYERX:
            player = provided.PLAYERO
        else:
            player = provided.PLAYERX
        
def mc_update_scores(scores, board, player):
    """scores a board and updates the scores grid"""
    dim = board.get_dim()
    winner = board.check_win()
    if winner == provided.DRAW:
        return
    flag = (player == winner)
    if flag:
        offset = 1
    else:
        offset = -1
    for idx in range(dim):
        for jdx in range(dim):
            if board.square(idx,jdx) == player:
                scores[idx][jdx] += (offset * SCORE_CURRENT)
            elif board.square(idx,jdx) != provided.EMPTY:
                scores[idx][jdx] -= (offset * SCORE_OTHER)

def get_best_move(board, scores):
    """returns the best possible move based on the scores"""
    blankies = board.get_empty_squares()
    max_score = scores[blankies[0][0]][blankies[0][1]]
    result = []
    for current in blankies:
        if scores[current[0]][current[1]] > max_score:
            max_score = scores[current[0]][current[1]]
    for current in blankies:
        if scores[current[0]][current[1]] == max_score:
            result.append(current)
    return random.choice(result)

def mc_move(board, player, trials):
    """ returns the best move for player using all above methods"""
    scores = [[0 for dummy_row in range(board.get_dim())] for dummy_col in range(board.get_dim())]
    for dummy_i in range(trials):
        trial_board = board.clone()
        mc_trial(trial_board,player)
        mc_update_scores(scores, trial_board, player)
    return get_best_move(board, scores)

#my_board = provided.TTTBoard(3)
#print mc_move(my_board, provided.PLAYERX, 1)
#print my_board
#print my_board.get_empty_squares()
#print my_board.check_win()
#my_board.move(0,1,provided.PLAYERX)
#print my_board
#print my_board.get_empty_squares()
#mc_trial(my_board,provided.PLAYERO)
#print my_board
# Test game with the console or the GUI.  Uncomment whichever 
# you prefer.  Both should be commented out when you submit 
# for testing to save time.

#provided.play_game(mc_move, NTRIALS, False)        
# poc_ttt_gui.run_gui(3, provided.PLAYERX, mc_move, NTRIALS, False)
