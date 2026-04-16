"""
Tic Tac Toe Player
"""

import math
import copy
X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    X_count=0
    O_count=0
    for row in board:
        X_count+= row.count("X")
        O_count+=row.count("O")
    if X_count > O_count:
            return(O)
    elif X_count<= O_count:
            return(X)
        


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    column=0
    r=0
    moves=set()
    for row in board:
         for val in row:
              if val == EMPTY:
                   i,j=r,column
                   moves.add (i,j)
              column+=1
         r+=1
         column=0

    return moves


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    player_num=player(board)
    row=0
    column=0
    i,j=action
    if board[i][j] != EMPTY:
         raise Exception("Invalid move")
    
    new_board=copy.deepcopy(board)
    new_board[i][j]=player_num
    return new_board
         


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    for row in board:
         if row[0] != EMPTY and row[0]==row[1]==row[2]:
              return row[0]
    for j in range(0,3):
         if board[0][j] != EMPTY and board[0][j]==board[1][j]==board[2][j]:
              return board[0][j]
         
    if board[0][0] != EMPTY and board[0][0]==board[1][1]==board[2][2]:
              return board[0][0]
    
    if board[2][2] != EMPTY and board[0][2]==board[1][1]==board[2][0]:
              return board[0][2]
    
    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    return winner(board) is not None  or len(actions(board)) == 0


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    who_won=winner(board)
    if(who_won=='X'):
         return 1
    elif who_won=='O':
         return -1
    else:
         return 0


def max_val(board):
     if terminal(board):
          return utility(board)
     score= float("-inf")
     for action in actions(board):
          score=max(score,min_val(result(board,action)))
     return score

def min_val(board):
     if terminal(board):
          return utility(board)
     score= float("inf")
     for action in actions(board):
          score=min(score,max_val(result(board,action)))
     return score

def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
         return None
    player_who=player(board)

    if player_who == 'X':
         best_act=None
         best_score= float("-inf")
         for action in actions(board):
              score= min_val(result(board,action))
              if score > best_score:
                   best_score=score
                   best_act=action
         return best_act
    
    elif player_who == 'O':
         best_act=None
         best_score=float("inf")
         for action in actions(board):
              score=max_val(result(board,action))
              if score<best_score:
                   best_score=score
                   best_act=action
         return best_act

