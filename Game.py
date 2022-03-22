import chess
from enum import Enum
from WebHandler import WebHandler

class Color(Enum):
    White = 0
    Black = 1


class Game(object):
    def __init__(self):
        self.board = chess.Board()
        self.round = 1
        self.turn = Color.White
        # self.white = Player(Color.White)
        # self.black = Player(Color.Black)
        # self.handler = WebHandler()


    def setBoard(self, oldBoard: dict, newBoard: dict):
        if oldBoard != newBoard:
            start = [x.upper() for x in oldBoard if x not in newBoard]
            end = [x.upper() for x in newBoard if x not in oldBoard or (newBoard[x] != oldBoard[x])]
            if len(start) == 1 and len(end) == 1:
                self.board.push(chess.Move(getattr(chess, start[0]), getattr(chess, end[0])))
            else:
                z = 3

    # def makeMove(self, move:chess.Move):
    #     # self.handler.makeMove(str(move))


    # def updateBoard(self, whiteMoves, blackMoves):
    #     while self.round < min(len(whiteMoves), len(blackMoves)):
    #         if self.turn == Color.White:
    #             move = whiteMoves[self.round - 1]
    #         else:
    #             move = blackMoves[self.round - 1]
    #         z = 3


# class Player(object):
#     def __init__(self, color: Color):
#         self.color = color
#
#     def selectMove(self, board):
#         z = 3
