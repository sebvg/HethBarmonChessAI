# -*- coding: utf-8 -*-
"""
Created on Sat Jan  9 21:11:21 2021

@author: sebas
"""

import chess
import chess.polyglot
import random

#Defining values for the evaluation function. This can be made more complex.
pieceValues = {'p':-100,'n':-320,'b':-330,'r':-500,'q':-900,'k':-20000,
              'P':100,'N':320,'B':330,'R':500,'Q':900,'K':20000}

positionValues = {'P':[0,0,0,0,0,0,0,0,
                           5,10,10,-20,-20,10,10,5,
                           5,-5,-10,0,0,-10,-5,5,
                           0,0,0,20,20,0,0,0,
                           5,5,10,25,25,10,5,5,
                           10,10,20,30,30,20,10,10,
                           50,50,50,50,50,50,50,50,
                           0,0,0,0,0,0,0,0],
                      'N':[-50,-40,-30,-30,-30,-30,-40,-50,
                           -40,-20,0,5,5,0,-20,-40,
                           -30,5,10,15,15,10,5,-30,
                           -30,0,15,20,20,15,0,-30,
                           -30,5,15,20,20,15,5,-30,
                           -30,0,10,15,15,10,0,-30,
                           -40,-20,0,0,0,0,-20,-40,
                           -50,-40,-30,-30,-30,-30,-40,-50],
                      'B':[-20,-10,-10,-10,-10,-10,-10,-20,
                           -10,5,0,0,0,0,5,-10,
                           -10,10,10,10,10,10,10,-10,
                           -10,0,10,10,10,10,0,-10,
                           -10,5,5,10,10,5,5,-10,
                           -10,0,5,10,10,5,0,-10,
                           -10,0,0,0,0,0,0,-10,
                           -20,-10,-10,-10,-10,-10,-10,-20],
                      'R':[0,0,0,5,5,0,0,0,
                           -5,0,0,0,0,0,0,-5,
                           -5,0,0,0,0,0,0,-5,
                           -5,0,0,0,0,0,0,-5,
                           -5,0,0,0,0,0,0,-5,
                           -5,0,0,0,0,0,0,-5,
                           5,10,10,10,10,10,10,5,
                           0,0,0,0,0,0,0,0],
                      'Q':[-20,-10,-10,-5,-5,-10,-10,-20,
                           -10,-0,5,0,0,0,0,-10,
                           -10,5,5,5,5,5,0,-10,
                           0,0,5,5,5,5,0,-5,
                           -5,0,5,5,5,5,0,-5,
                           -10,0,5,5,5,5,0,-5,
                           -10,0,0,0,0,0,0,-10,
                           -20,-10,-10,-5,-5,-10,-10,-20],
                      'K':[20,30,10,0,0,10,30,20,
                           20,20,0,0,0,0,20,20,
                           -10,-20,-20,-20,-20,-20,-20,-10,
                           -20,-30,-30,-40,-40,-30,-30,-20,
                           30,-40,-40,-50,-50,-40,-30,-30,
                           30,-40,-40,-50,-50,-40,-30,-30,
                           30,-40,-40,-50,-50,-40,-30,-30,
                           30,-40,-40,-50,-50,-40,-30,-30,]}
positionValues['p'] = [i * -1 for i in positionValues['P'][::-1]]
positionValues['n'] = [i * -1 for i in positionValues['N'][::-1]]
positionValues['b'] = [i * -1 for i in positionValues['B'][::-1]]
positionValues['r'] = [i * -1 for i in positionValues['R'][::-1]]
positionValues['q'] = [i * -1 for i in positionValues['Q'][::-1]]
positionValues['k'] = [i * -1 for i in positionValues['K'][::-1]]
    
positionValuesEndgame = positionValues.copy()
positionValuesEndgame['K'] = [-50,-30,-30,-30,-30,-30,-30,-50,
                                  -30,-30,0,0,0,0,-30,-30,
                                  30,-10,0,0,0,0,-10,-30,
                                  -30,-10,0,0,0,0,-10,-30,
                                  -30,-10,0,0,0,0,-10,-30,
                                  30,-10,0,0,0,0,-10,-30,
                                  -30,-30,0,0,0,0,-30,-30,
                                  -50,-30,-30,-30,-30,-30,-30,-50]
positionValuesEndgame['k'] = [i * -1 for i in positionValuesEndgame['K'][::-1]]


def evaluate(board):
    val = 0
    if board.is_checkmate():
        if board.result() == "1-0":
            val += 100000
        elif board.result() == "0-1":
            val -= 100000
    for i in range(64):
        try:
            val += pieceValues[board.piece_at(i).symbol()]
        except AttributeError:
            pass
    if (chess.Piece.from_symbol('Q') in board.piece_map().values() 
        or chess.Piece.from_symbol('q') in board.piece_map().values()):
        for i in range(64):
            try:
                val += positionValues[board.piece_at(i).symbol()][i]
            except AttributeError:
                pass
    else:
        for i in range(64):
            try:
                val += positionValuesEndgame[board.piece_at(i).symbol()][i]
            except AttributeError:
                pass
    return val

def minimax(board, depth, alpha, beta):
    if depth == 0 or board.is_checkmate():
        return evaluate(board)
    
    if board.turn == chess.WHITE:
        maxEval = -10000
        for m in board.legal_moves:
            b = board.copy(stack=False)
            b.push(m)
            eva = minimax(b, depth-1, alpha, beta)
            maxEval = max(eva, maxEval)
            alpha = max(alpha, eva)
            if beta <= alpha:
                break
        return maxEval
    
    else:
        minEval = 10000
        for m in board.legal_moves:
            b = board.copy(stack=False)
            b.push(m)
            eva = minimax(b, depth-1, alpha, beta)
            minEval = min(eva, minEval)
            beta = min(beta, eva)
            if beta <= alpha:
                break
        return minEval
    
def bestMove(board, depth):
    lm = list(board.legal_moves)
    bs = lm.copy()
    for i in range(len(lm)):
        bs[i] = board.copy(stack=False)
        bs[i].push(lm[i])
    eva = lm.copy()
    for i in range(len(lm)):
        eva[i] = minimax(bs[i],depth,alpha=-100000,beta=100000)
    res = [x for x in sorted(zip(lm,eva),key=lambda y:y[1],reverse=True)]
    return res[0]