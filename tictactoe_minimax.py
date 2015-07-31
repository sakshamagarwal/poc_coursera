"""
Mini-max Tic-Tac-Toe Player
"""

import poc_ttt_gui
import poc_ttt_provided as provided

# Set timeout, as mini-max can take a long time
import codeskulptor
codeskulptor.set_timeout(60)

# SCORING VALUES - DO NOT MODIFY
SCORES = {provided.PLAYERX: 1,
          provided.DRAW: 0,
          provided.PLAYERO: -1}

def other_player(player):
    """Helper function which returns the opposite player to the provided player"""
    if player == provided.PLAYERX:
        return provided.PLAYERO
    else:
        return provided.PLAYERX

    
def select_best(results, player):
    """Helper function which returns the best move"""
    for idx in range(len(results)):
        if player == provided.PLAYERX and results[idx][0] == 1:
            return results[idx]
        elif player == provided.PLAYERO and results[idx][0] == -1:
            return results[idx]
    
    for idx in range(len(results)):
        if results[idx][0] == 0:
            return results[idx]
        
    return results[0]
    
def mm_move(board, player):
    """
    Make a move on the board.
    
    Returns a tuple with two elements.  The first element is the score
    of the given board and the second element is the desired move as a
    tuple, (row, col).
    """
    empties = board.get_empty_squares()
    if board.check_win() == None:
        results = []
        for idx in range(len(empties)):
            my_board = board.clone()
            my_board.move(empties[idx][0], empties[idx][1], player)
            results.append((mm_move(my_board, other_player(player))[0], empties[idx]))
        my_max = select_best(results, player)
        return my_max
    elif board.check_win() == provided.PLAYERX:
        return 1, (-1, -1)
    elif board.check_win() == provided.PLAYERO:
        return -1, (-1, -1)
    else:
        return 0, (-1, -1)

def move_wrapper(board, player, trials):
    """
    Wrapper to allow the use of the same infrastructure that was used
    for Monte Carlo Tic-Tac-Toe.
    """
    move = mm_move(board, player)
    assert move[1] != (-1, -1), "returned illegal move (-1, -1)"
    return move[1]

# Test game with the console or the GUI.
# Uncomment whichever you prefer.
# Both should be commented out when you submit for
# testing to save time.

# provided.play_game(move_wrapper, 1, False)        
# poc_ttt_gui.run_gui(3, provided.PLAYERO, move_wrapper, 1, False)
#print dir(provided.TTTBoard)
#print mm_move(provided.TTTBoard(3, False, [[provided.PLAYERX, provided.PLAYERX, provided.PLAYERO], [provided.PLAYERO, provided.PLAYERX, provided.PLAYERX], [provided.PLAYERO, provided.EMPTY, provided.PLAYERO]]), provided.PLAYERX)
#print mm_move(provided.TTTBoard(2, False, [[provided.EMPTY, provided.EMPTY], [provided.EMPTY, provided.EMPTY]]), provided.PLAYERX)