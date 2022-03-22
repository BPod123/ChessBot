from TimedGameHandler import TimedGameHandler
from WebHandler import WebHandler
from time import sleep
class ChessBot(object):
    def __init__(self, numCores:int, timePerMove, failSoft):
        """
        :param numCores: The number of cpu cores the game handler is allowed to use when picking a move
        """
        self.webHandler = WebHandler()
        self.numCores = numCores
        self.timePerMove = timePerMove
        self.failSoft = failSoft
        self.gameHandler = None

    def playGame(self):
        self.gameHandler = TimedGameHandler(numCores=self.numCores)
        if not self.webHandler.color:
            # if playing black, wait for first move to be made
            while self.webHandler.turn != self.webHandler.color:
                sleep(0.01)
            self.gameHandler.makeMove(self.webHandler.lastMove)
        while not self.gameHandler.board.is_game_over():
            move = self.gameHandler.pickMove(self.failSoft, self.timePerMove)
            self.webHandler.makeMove(move)
            if self.gameHandler.moveEndsGame(move):
                self.gameHandler.makeMove(move)
                break

            while self.webHandler.turn != self.webHandler.color:
                sleep(0.01)

            lastMove = self.webHandler.lastMove
            while lastMove is None or lastMove == move:
                lastMove = self.webHandler.lastMove
            self.gameHandler.makeMove(lastMove)
        z = 3






