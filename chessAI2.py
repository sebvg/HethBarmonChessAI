# -*- coding: utf-8 -*-
"""
Created on Fri Jan  8 14:55:12 2021

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

def minimaxInit(board, depth, alpha, beta):
    #The below sorts the legal moves by their rating, so the order is more
    #efficient for future iterations.
    lm = list(board.legal_moves)
        
    initEval = lm.copy()
    for i in range(len(lm)):
        b = board.copy()
        b.push(lm[i])
        initEval[i] = evaluate(b)
        
    lm = [x for _,x in sorted(zip(initEval,lm),key=lambda x:x[0], reverse=False)]
    bestMoves = [None] * depth
    
    return minimax(board, depth, alpha, beta, lm, bestMoves)

def minimax(board, depth, alpha, beta, moves, bestMoves):
    if depth==0 or board.is_game_over():
        return evaluate(board), bestMoves
    
    if board.turn == chess.WHITE:
        maxEval = -100000
        for m in moves:
            b = board.copy()
            b.push(m)
            eva = minimax(b, depth-1, alpha, beta, list(b.legal_moves),bestMoves)[0]
            if eva > maxEval:
                maxEval = eva
                bestMoves[depth-1] = m
            alpha = max(alpha, eva)
            if beta <= alpha:
                break
        return maxEval, bestMoves
    
    else:
        minEval = 100000
        for m in moves:
            b = board.copy()
            b.push(m)
            eva = minimax(b, depth-1, alpha, beta, list(b.legal_moves),bestMoves)[0]
            if eva < minEval:
                minEval = eva
                bestMoves[depth-1] = m
            beta = min(beta, eva)
            if beta <= alpha:
                break
        return minEval, bestMoves
    
def AI(board, depth):
    openings = []
    w = []
    with chess.polyglot.open_reader("polyglot-collection/codekiddy.bin") as reader:
        for entry in reader.find_all(board):
            openings.append(entry.move)
            w.append(entry.weight)

    if len(openings) > 0:
        #print("The best move is %s (book move)" % board.san(openings[0]))
        return random.choices(openings,weights=w,k=1)[0]

    else:
        final = minimaxInit(board,depth,alpha=-100000,beta=100000)
        #print("The best move is %s, with an evaluation of %.2f" %
        #  (board.san(final[1].move_stack[0]),final[0]/100.0))
        return final[1][-1]
        
def play(white=1, start_fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1", depth=4):
    game = chess.Board(start_fen)
    if not white:
        move = AI(game.copy(stack=False),depth)
        print("Heth Barmon played %s" % game.san(move))
        game.push(move)
        print(game)
        
    while not game.is_game_over():
        cont = False
        while not cont:
            userMove = input("Input move -> ")
            try:
                if game.parse_san(userMove) in game.legal_moves:
                    print("You played %s" % userMove)
                    game.push_san(userMove)
                    cont = True
                else:
                    print("%s is not a legal move. Please check you are inputting the correct SAN move." % userMove)
            except ValueError:
                print("%s is not a legal move. Please check you are inputting the correct SAN move." % userMove)
        
        move = AI(game.copy(stack=False),depth)
        print("Heth Barmon played %s" % game.san(move))
        game.push(move)
        print(game)
        
def main():
    playerColour = None
    while playerColour==None:
        entry = input("Which colour would you like to play? (white/black)\n> ")
        if "white" in entry.lower():
            playerColour = 1
            print("You play with the white pieces - it's your turn to move.")
        elif "black" in entry.lower():
            playerColour = 0
            print("You play with the black pieces.")
        else:
            print("Please enter either \"white\" or \"black\" ")
            print(entry)
    play(white=playerColour)
    
main()
        