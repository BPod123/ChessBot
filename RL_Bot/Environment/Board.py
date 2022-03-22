from chess import Board as chessBoard
from collections import defaultdict
class Board(object):
    def __init__(self):
        self._board = chessBoard()
        self.boardCount = defaultdict(int)
    def __hash__(self):
        illegalBoards = [str(x) for x in self.boardCount if self.boardCount[x] >= 2]
    # def makeMove(selfm):
