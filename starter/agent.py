"""
An AI player for Othello. 
"""

import random
import sys
import time

from tests import *
# You can use the functions from othello_shared to write your AI
from othello_shared import find_lines, get_possible_moves, get_score, play_move

cache = {} # Use this for state caching

def eprint(*args, **kwargs): #use this for debugging, to print to sterr
    print(*args, file=sys.stderr, **kwargs)
    
def compute_utility(board, color):
    # IMPLEMENT!
    """
    Method to compute the utility value of board.
    INPUT: a game state and the player that is in control
    OUTPUT: an integer that represents utility
    """
    p1_score, p2_score = get_score(board)

    util = None
    if color == 1:
        util = p1_score - p2_score

    if color == 2:
        util = p2_score - p1_score

    return util

def compute_heuristic(board, color):
    # IMPLEMENT! 
    """
    Method to heuristic value of board, to be used if we are at a depth limit.
    INPUT: a game state and the player that is in control
    OUTPUT: an integer that represents heuristic value
    """
    raise RuntimeError("Method not implemented") # Replace this line!



############ MINIMAX ###############################
def minimax_min_node(board, color, limit, caching = 0):
    # IMPLEMENT!
    """
    A helper function for minimax that finds the lowest possible utility
    """
    # HINT:
    # 1. Get the allowed moves
    # 2. Check if w are at terminal state
    # 3. If not, for each possible move, get the max utiltiy
    # 4. After checking every move, you can find the minimum utility
    # ...
    if caching == 1:
        if board in cache:
            return cache[board]

    opp = 3 - color
    possible_moves = get_possible_moves(board, opp)
    highest_util = []
    moves_list = []
    best_move = None
    utility = None

    if len(possible_moves) == 0 or limit == 0:
        return best_move, compute_utility(board, color)

    for i in possible_moves:
        next_move = play_move(board, opp, i[0], i[1])
        _, util = minimax_max_node(next_move, color, limit - 1, caching)
        moves_list.append((i, util))
        highest_util.append(util)
        if caching == 1:
            if i not in cache:
                cache[next_move] = (i,util)

    idx = highest_util.index(min(highest_util))
    best_move = moves_list[idx][0]
    utility = moves_list[idx][1]
    return best_move, utility


def minimax_max_node(board, color, limit, caching = 0):
    # IMPLEMENT!
    """
    A helper function for minimax that finds the highest possible utility
    """
    # HINT:
    # 1. Get the allowed moves
    # 2. Check if w are at terminal state
    # 3. If not, for each possible move, get the min utiltiy
    # 4. After checking every move, you can find the maximum utility
    # ...
    if caching == 1:
        if board in cache:
            return cache[board]
        
    possible_moves = get_possible_moves(board, color)
    lowest_util = []
    moves_list = []
    best_move = None
    utility = None

    if len(possible_moves) == 0 or limit == 0:
        return best_move, compute_utility(board, color)

    for i in possible_moves:
        next_move = play_move(board, color, i[0], i[1])
        _, util = minimax_min_node(next_move, color, limit - 1, caching)
        moves_list.append([i, util])
        lowest_util.append(util)
        if caching == 1:
            if i not in cache:
                cache[next_move] = (i,util)

    idx = lowest_util.index(max(lowest_util))
    best_move = moves_list[idx][0]
    utility = moves_list[idx][1]
    return best_move, utility

    
def select_move_minimax(board, color, limit, caching = 0):
    # IMPLEMENT!
    """
    Given a board and a player color, decide on a move using Minimax algorithm. 
    Note that other parameters are accepted by this function:
    If limit is a positive integer, your code should enfoce a depth limit that is equal to the value of the parameter.
    Search only to nodes at a depth-limit equal to the limit.  If nodes at this level are non-terminal return a heuristic 
    value (see compute_utility)
    If caching is ON (i.e. 1), use state caching to reduce the number of state evaluations.
    If caching is OFF (i.e. 0), do NOT use state caching to reduce the number of state evaluations.
    INPUT: a game state, the player that is in control, the depth limit for the search, and a flag determining whether state caching is on or not
    OUTPUT: a tuple of integers (i,j) representing a move, where i is the column and j is the row on the board.
    """
    if caching == 1:
        cache.clear()

    possible_moves = get_possible_moves(board, color)
    best_move = None
    max_util = float('-inf')
    
    for i in possible_moves:
        next_move = play_move(board, color, i[0], i[1])
        _, util = minimax_min_node(next_move, color, limit - 1, caching)
        if util > max_util:
            max_util = util
            best_move = i
            if caching == 1:
                if i not in cache:
                    cache[next_move] = (i,util)
    return best_move

############ ALPHA-BETA PRUNING #####################
def alphabeta_min_node(board, color, alpha, beta, limit, caching = 0, ordering = 0):
    # IMPLEMENT!
    """
    A helper function for alpha-beta that finds the lowest possible utility (don't forget to utilize and update alpha and beta!)
    """
    opp = 3 - color
    possible_moves = get_possible_moves(board, opp)
    highest_util = []
    moves_list = []
    best_move = None
    utility = None

    if caching == 1:
        if board in cache:
            return cache[board]
    
    if len(possible_moves) == 0 or limit == 0:
        return best_move, compute_utility(board, color)


    for i in possible_moves:
        next_move = play_move(board, opp, i[0], i[1])
        _, util = alphabeta_max_node(next_move, color, alpha, beta, limit - 1, caching, ordering)
        moves_list.append((i, util))
        highest_util.append(util)
        beta = min(beta, util)
        if beta <= alpha:
            break


    idx = highest_util.index(min(highest_util))
    best_move = moves_list[idx][0]
    utility = moves_list[idx][1]

    if caching == 1:
        cache[board] = (best_move, utility)

    return best_move, utility



def alphabeta_max_node(board, color, alpha, beta, limit, caching = 0, ordering = 0):
    # IMPLEMENT!
    """
    A helper function for alpha-beta that finds the highest possible utility (don't forget to utilize and update alpha and beta!)
    """
    possible_moves = get_possible_moves(board, color)
    lowest_util = []
    moves_list = []
    best_move = None
    utility = None
    if caching == 1:
        if board in cache:
            return cache[board]

    if len(possible_moves) == 0 or limit == 0:
        return best_move, compute_utility(board, color)
    
    if ordering == 1:
        moves = []
        for j in possible_moves:
            moves.append((j, compute_utility(play_move(board, color, j[0], j[1]), color)))
        ordered_moves = sorted(moves, key=lambda x: -x[1])
        possible_moves = []
        for k in ordered_moves:
            possible_moves.append(k[0])

        
    for i in possible_moves:
        next_move = play_move(board, color, i[0], i[1])
        _, util = alphabeta_min_node(next_move, color, alpha, beta, limit - 1, caching, ordering)
        moves_list.append((i, util))
        lowest_util.append(util)
        alpha = max(alpha, util)
        if alpha >= beta:
            break
    
    idx = lowest_util.index(max(lowest_util))
    best_move = moves_list[idx][0]
    utility = moves_list[idx][1]

    if caching:
        cache[board] = (best_move, utility)

    return best_move, utility

def select_move_alphabeta(board, color, limit = -1, caching = 0, ordering = 0):
    # IMPLEMENT!
    """
    Given a board and a player color, decide on a move using Alpha-Beta algorithm. 
    Note that other parameters are accepted by this function:
    If limit is a positive integer, your code should enfoce a depth limit that is equal to the value of the parameter.
    Search only to nodes at a depth-limit equal to the limit.  If nodes at this level are non-terminal return a heuristic 
    value (see compute_utility)
    If caching is ON (i.e. 1), use state caching to reduce the number of state evaluations.
    If caching is OFF (i.e. 0), do NOT use state caching to reduce the number of state evaluations.    
    If ordering is ON (i.e. 1), use node ordering to expedite pruning and reduce the number of state evaluations. 
    If ordering is OFF (i.e. 0), do NOT use node ordering to expedite pruning and reduce the number of state evaluations. 
    INPUT: a game state, the player that is in control, the depth limit for the search, a flag determining whether state caching is on or not, a flag determining whether node ordering is on or not
    OUTPUT: a tuple of integers (i,j) representing a move, where i is the column and j is the row on the board.
    """
    possible_moves = get_possible_moves(board, color)
    best_move = None
    max_util = float('-inf')
    alpha = float('-inf')
    beta = float('inf')

    if caching == 1:
        cache.clear()

    if ordering == 1:
        moves = []
        for j in possible_moves:
            moves.append((j, compute_utility(play_move(board, color, j[0], j[1]), color)))
        ordered_moves = sorted(moves, key=lambda x: -x[1])
        possible_moves = []
        for k in ordered_moves:
            possible_moves.append(k[0])

    
    for i in possible_moves:
        next_move = play_move(board, color, i[0], i[1])
        _, util = alphabeta_min_node(next_move, color, alpha, beta, limit - 1, caching, ordering)
        if util > max_util:
            max_util = util
            best_move = i

        alpha = max(alpha, util)
        if beta <= alpha:
            break

    return best_move

####################################################
def run_ai():
    """
    This function establishes communication with the game manager.
    It first introduces itself and receives its color.
    Then it repeatedly receives the current score and current board state until the game is over.
    """
    print("Othello AI") # First line is the name of this AI
    arguments = input().split(",")
    
    color = int(arguments[0]) # Player color: 1 for dark (goes first), 2 for light. 
    limit = int(arguments[1]) # Depth limit
    minimax = int(arguments[2]) # Minimax or alpha beta
    caching = int(arguments[3]) # Caching 
    ordering = int(arguments[4]) # Node-ordering (for alpha-beta only)

    if (minimax == 1): eprint("Running MINIMAX")
    else: eprint("Running ALPHA-BETA")

    if (caching == 1): eprint("State Caching is ON")
    else: eprint("State Caching is OFF")

    if (ordering == 1): eprint("Node Ordering is ON")
    else: eprint("Node Ordering is OFF")

    if (limit == -1): eprint("Depth Limit is OFF")
    else: eprint("Depth Limit is ", limit)

    if (minimax == 1 and ordering == 1): eprint("Node Ordering should have no impact on Minimax")

    while True: # This is the main loop
        # Read in the current game status, for example:
        # "SCORE 2 2" or "FINAL 33 31" if the game is over.
        # The first number is the score for player 1 (dark), the second for player 2 (light)
        next_input = input()
        status, dark_score_s, light_score_s = next_input.strip().split()
        dark_score = int(dark_score_s)
        light_score = int(light_score_s)

        if status == "FINAL": # Game is over.
            print
        else:
            board = eval(input()) # Read in the input and turn it into a Python
                                  # object. The format is a list of rows. The
                                  # squares in each row are represented by
                                  # 0 : empty square
                                  # 1 : dark disk (player 1)
                                  # 2 : light disk (player 2)

            # Select the move and send it to the manager
            if (minimax == 1): # run this if the minimax flag is given
                movei, movej = select_move_minimax(board, color, limit, caching)
            else: # else run alphabeta
                movei, movej = select_move_alphabeta(board, color, limit, caching, ordering)
            
            print("{} {}".format(movei, movej))

if __name__ == "__main__":
    run_ai()
