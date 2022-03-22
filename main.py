import time

import chess

from WebHandler import WebHandler
from Game import Game
from time import sleep
if __name__ == '__main__':

    handler = WebHandler()
    handler.findGame()
    roundCount = 0
    turn = 0
    game = Game()
    board = handler.board
    moves = ["e2e4", "g1h3", "f1e2"]
    while roundCount < 10:
        if turn == 1:
            newBoard = handler.board
            if board != newBoard:
                game.setBoard(board, newBoard)
                turn = 0
                roundCount += 1
                board = newBoard
        else:
            if roundCount < len(moves):
                move = chess.Move(getattr(chess, moves[roundCount][:2].upper()), getattr(chess, moves[roundCount][2:].upper()))
            else:
                for move in game.board.legal_moves:
                    break
            handler.makeMove(str(move))
            game.board.push(move)
            board = handler.board
            turn = 1
            # break

    handler.makeMove("e2e4")
    sleep(3)
    handler.makeMove("d2d4")
    sleep(3)
    moves = handler.moves

    game.setBoard(*handler.board)
    z = 3
    # board = handler.parseBoard()



    z = 3