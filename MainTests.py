import unittest
from WebHandler import WebHandler
from TimedGameHandler import TimedGameHandler
from time import sleep
from random import randint
from ChessBot import ChessBot
from multiprocessing import cpu_count
import chess
from chess import Move
A1, B1, C1, D1, E1, F1, G1, H1, A2, B2, C2, D2, E2, F2, G2, H2, A3, B3, C3, D3, E3, F3, G3, H3, A4, B4, C4, D4, E4, F4, G4, H4, A5, B5, C5, D5, E5, F5, G5, H5, A6, B6, C6, D6, E6, F6, G6, H6, A7, B7, C7, D7, E7, F7, G7, H7, A8, B8, C8, D8, E8, F8, G8, H8 = range(64)
class MyTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.webHandler = WebHandler()
        self.gameHandler = TimedGameHandler(1)
        # sleep(2)
            #GameHandler(6, 20)
    def test_ShortGame(self):

        self.webHandler.findGame()
        moves = [Move(x[0], x[1]) for x in [(D2, D4), (C7, C6), (C1, G5), (D8, C7), (D1, D3), (G7, G6), (D3, E3), (G8, H6), (E3, E4), (F8, G7), (E4, E7)]]

        self.webHandler.playTestGame(moves)
    def test_escapableCheck(self):

        moves = [Move(x[0], x[1]) for x in
                 [(D2, D4), (C7, C6), (C1, G5), (D8, C7), (D1, D3), (G7, G6), (D3, E3), (G8, H6), (E3, E4), (H6, G8),
                  (E4, E7)]]

        self.webHandler.playTestGame(moves)
    def test_blackPromotion(self):
        moves = [Move(B2, B4), Move(C7, C5), Move(A2, A3), Move(C5, B4), Move(A3, A4), Move(B4, B3), Move(C1, A3),
        Move(B3, B2), Move(B1, C3)]
        self.webHandler.practiceGame()
        for i in range(len(moves)):
            self.webHandler.makeMove(moves[i])
            self.gameHandler.makeMove(moves[i])
            if i > 0:
                lastMove = self.webHandler.lastMove
            if i % 2 == 0:
                while self.webHandler.turn != self.webHandler.color:
                    sleep(0.01)
                self.webHandler.undoMove()
        z = 3

    def test_playComputer(self):
        self.webHandler.findGame()
        while not self.gameHandler.board.is_game_over():
            if self.webHandler.turn == self.webHandler.color:
                move = self.gameHandler.pickMove()
                self.webHandler.makeMove(move)
                self.gameHandler.makeMove(move)
                if not self.gameHandler.board.is_game_over():
                    while not self.webHandler.turn:# or self.webHandler.lastMove != move or self.gameHandler.board.piece_at(self.webHandler.lastMove.from_square) is None:
                        sleep(0.01)
                    # while not self.webHandler.moveHasBeenMade:
                    #     sleep(0.01)

                    # while self.webHandler.lastMove == self.gameHandler.board.move_stack[-1] and self.gameHandler.board.piece_at(self.gameHandler.board.move_stack[-1].from_square) is None:
                    #     pass
                    # while self.webHandler.lastMove.from_square == self.webHandler.lastMoveMade.from_square and self.webHandler.lastMove.to_square == self.webHandler.lastMoveMade.to_square:
                    #     pass
                    self.gameHandler.makeMove(self.webHandler.lastMove)
    def test_playBot(self):
        self.webHandler.practiceGame()
        while True:
            sleep(0.1)
            try:
                lastMove = self.webHandler.lastMove
            except:
                lastMove = None
            self.gameHandler.makeMove(lastMove)
            move = self.gameHandler.pickMove(False, 5)
            self.gameHandler.makeMove(move)
            self.webHandler.makeMove(move)


        z = 3




    # def test_determineIfLost(self):
    #     moves = [Move(x[0], x[1]) for x in
    #              [(G2, G3), (D7, D5), (F1, H3), (C8, G4), (C2, C3), (D8, D6), (D1, B3), (D6, F4), (G1, F3), (F4, F3), (B3, B7)]]
    #
    #     self.webHandler.practiceGame()
    #     for i in range(len(moves)):
    #         self.webHandler.makeMove(moves[i])
    #         self.gameHandler.makeMove(moves[i])
    #         sleep(0.1)
    #         lastMove = self.webHandler.lastMove
    #         if not self.gameHandler.moveEndsGame(lastMove):
    #          and i % 2 == 0:
    #             while self.webHandler.lastMove.from_square == moves[i].from_square and self.webHandler.lastMove.to_square == moves[i].to_square:
    #                 sleep(0.1)
    #             self.webHandler.undoMove()
    #
    #             #
    #             # while not (self.webHandler.turn != i % 2 and self.webHandler.lastMove.from_square == moves[i].from_square and self.webHandler.lastMove.to_square == moves[i].to_square):
    #             #     pass
    #             # self.webHandler.undoMove()
    #     z = 3











    def test_IDDFS(self):
        roundCount = 0
        while roundCount < 75 and not self.gameHandler.board.is_game_over():
            try:
                try:
                    while self.webHandler.turn != self.webHandler.color:
                        sleep(0.01)
                except:
                    continue
                lastMove = self.webHandler.lastMove
            except:
                sleep(1)
                try:
                    lastMove = self.webHandler.lastMove
                except:
                    sleep(1)
                    lastMove = self.webHandler.lastMove
            if lastMove is not None:
                self.gameHandler.makeMove(lastMove)
            nextMoves, score = self.gameHandler.pickMove(True, False, 10, float('inf'))
            nextMove = list(nextMoves)[randint(0, len(nextMoves) - 1)]
            self.gameHandler.makeMove(nextMove)
            try:
                self.webHandler.makeMove(nextMove)
            except:
                sleep(1)
                try:
                    self.webHandler.makeMove(nextMove)
                except:
                    sleep(1)
                    self.webHandler.makeMove(nextMove)

            roundCount += 1
        z = 3
    def test_fastIDDFS(self):
        self.gameHandler.doFastDecision = True
        roundCount = 0
        while roundCount < 75 and not self.gameHandler.board.is_game_over():
            try:
                try:
                    while self.webHandler.turn != self.webHandler.color:
                        sleep(0.01)
                except:
                    continue
                lastMove = self.webHandler.lastMove
            except:
                sleep(1)
                try:
                    lastMove = self.webHandler.lastMove
                except:
                    sleep(1)
                    lastMove = self.webHandler.lastMove
            if lastMove is not None:
                self.gameHandler.makeMove(lastMove)
            nextMoves, score = self.gameHandler.pickMove(True, False, 10, float('inf'))
            nextMove = list(nextMoves)[randint(0, len(nextMoves) - 1)]
            self.gameHandler.makeMove(nextMove)
            try:
                self.webHandler.makeMove(nextMove)
            except:
                sleep(1)
                try:
                    self.webHandler.makeMove(nextMove)
                except:
                    sleep(1)
                    self.webHandler.makeMove(nextMove)

            roundCount += 1
        z = 3






if __name__ == '__main__':
    unittest.main()
