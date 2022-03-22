import chess
import time
from multiprocessing import Pool, cpu_count
from random import randint
import Evaluation.Evaluation as eval
from numba import jit
from collections import defaultdict
import sys

sys.setrecursionlimit(max(sys.getrecursionlimit(), 10 ** 9))
from Decision.Decision import ChessNodeData, IDDFS, IDDFSParallel
from Decision.FastDecision import IDDFS as FastIDDFS, IDDFSParallel as FastIDDFSParallel


class TimedGameHandler(object):
    def __init__(self, numCores):
        """
        """
        self.board = chess.Board()
        # self.calculationTime = calculationTime
        self.numCores = numCores
        self.boardStrings = defaultdict(int)
        self.boardStrings[str(self.board)] += 1
        self.doFastDecision = False

    def makeMove(self, move: chess.Move):
        if self.board.piece_at(move.from_square).piece_type == move.promotion:
            move = chess.Move(move.from_square, move.to_square)
        # if move.promotion == chess.PAWN or move.promotion == chess.KING or self.board.piece_at(move.from_square) is not None and self.board.piece_at(move.from_square).piece_type != chess.PAWN:
        #     move = chess.Move(move.from_square, move.to_square)

        self.board.push(move)
        self.boardStrings[(str(self.board), self.board.turn)] += 1

    def pickMove(self, failSoft=False, calculationTime=10, maxDepth=float('inf')):
        """
        :param failSoft: If true, will do failsoft alpha-beta pruning, otherwise will do fail-hard alpha-beta pruning
        :return:
        """
        # if not self.doFastDecision:
        #     if self.numCores > 1:
        #         options, score = list(IDDFSParallel(ChessNodeData(self.board, None), calculationTime, self.numCores,
        #                                                 trippleOccuranceMoves(self.board, self.boardStrings), failSoft))
        #     else:
        #
        #         options, score = list(IDDFS(ChessNodeData(self.board, None), calculationTime,
        #                                         trippleOccuranceMoves(self.board, self.boardStrings), failSoft))
        #
        # else:
        if self.numCores > 1:
            options, score = FastIDDFSParallel(self.board, {x for x in self.boardStrings if self.boardStrings[x] >= 2}, failSoft,
                                         calculationTime, maxDepth, eval.SimplifiedPlusTableEvaluation,
                                         self.numCores)
        else:
            options, score = FastIDDFS(self.board, {x for x in self.boardStrings if self.boardStrings[x] >= 2}, failSoft,
                                 calculationTime, maxDepth,
                                 eval.SimplifiedPlusTableEvaluation)

        return list(options)[randint(0, len(options) - 1)]

    def moveEndsGame(self, move: chess.Move):
        cpy = self.board.copy(stack=False)
        cpy.push(move)
        return cpy.is_game_over()


def trippleOccuranceMoves(board: chess.Board, boardStrings: dict):
    """
    :param board: chess board
    :param boardStrings: list of board string representations
    :return: A list of moves, if any, that will cause a board to appear for the third time
    """
    toppedOutBoardStrings = {key for key in boardStrings if boardStrings[key] >= 2}
    if len(toppedOutBoardStrings) == 0:
        return []
    badMoves = []
    for move in board.legal_moves:
        cpy = board.copy(stack=False)
        cpy.push(move)
        if str(cpy) in toppedOutBoardStrings:
            badMoves.append(move)
    return set(badMoves)


# def alphaBetaFailHard(board: chess.Board, move: chess.Move, stopTime, alpha=-float('inf'), beta=float('inf')):
#     """
#     :param board: Chess Board
#     :param move: Chess Move
#     :param stopTime: The time at which this function will stop branching and return the result
#     :param alpha: the minimum score that the maximizing player (WHITE) can have after move is taken. Defaults to -inf.
#     Will be set to the board score if not passed in.
#     :param beta: the maximum score that the minimizing player (BLACK) can have after move is taken. Defaults to inf.
#     Will be set to the board score if not passed in.
#     :return: (alpha, beta)
#     """
#     if board.is_game_over():
#         outcome = board.outcome()
#         if outcome is not None:
#             if outcome.winner is not None:
#                 if outcome.winner == chess.WHITE:
#                     # The maximum score possible has been achieved. Game over. White won.
#                     return float('inf')
#                 else:
#                     # The minimum score possible has been achieved. Game over. Black won.
#                     return -float('inf')
#             else:
#                 # Draw:
#                 # Return a value that is really high if player is the minimizing player and really low if
#                 # player is the maximizing player, but not as extreme as +- infinity.
#                 if board.turn == chess.WHITE:
#                     # Maximizing player - wants a big value, but will get a low value to discourage a draw
#                     return -999999
#                 else:
#                     # Miniimizing player - wants a low value, but will get a high value to discourage a draw
#                     return 999999
#
#     if time.time() >= stopTime:
#         return sum(eval.SimplifiedEvaluation(board), eval.TableScore(board, eval.isEndGame(board)))
#
#     cpy = board.copy(stack=False)
#     cpy.push(move)
#     if cpy.turn == chess.WHITE:
#         # Maximize
#         value = -float('inf')
#         for subMove in cpy.legal_moves:
#             value = max(value, alphaBetaFailHard(cpy, subMove, stopTime, alpha, beta))
#
#             if value >= beta:
#                 break
#
#             # fail-hard: update after if-statement
#             alpha = max(alpha, value)
#     else:
#         # Minimize
#         value = float('inf')
#         for subMove in cpy.legal_moves:
#             value = min(value, alphaBetaFailHard(cpy, subMove, stopTime, alpha, beta))
#             # Note to self, only have one of the two below (fail-soft of fail-hard) uncommented
#
#             # fail-soft: update before if-statement
#             # alpha = max(alpha, value)
#
#             if value >= beta:
#                 break
#
#             # fail-hard: update after if-statement
#             beta = min(beta, value)
#     return value
#
# def alphaBetaFailSoft(board: chess.Board, move: chess.Move, stopTime, alpha=-float('inf'), beta=float('inf')):
#     """
#     :param board: Chess Board
#     :param move: Chess Move
#     :param stopTime: The time at which this function will stop branching and return the result
#     :param alpha: the minimum score that the maximizing player (WHITE) can have after move is taken. Defaults to -inf.
#     Will be set to the board score if not passed in.
#     :param beta: the maximum score that the minimizing player (BLACK) can have after move is taken. Defaults to inf.
#     Will be set to the board score if not passed in.
#     :return: (alpha, beta)
#     """
#     if board.is_game_over():
#         outcome = board.outcome()
#         if outcome is not None:
#             if outcome.winner is not None:
#                 if outcome.winner == chess.WHITE:
#                     # The maximum score possible has been achieved. Game over. White won.
#                     return float('inf')
#                 else:
#                     # The minimum score possible has been achieved. Game over. Black won.
#                     return -float('inf')
#             else:
#                 # Draw:
#                 # Return a value that is really high if player is the minimizing player and really low if
#                 # player is the maximizing player, but not as extreme as +- infinity.
#                 if board.turn == chess.WHITE:
#                     # Maximizing player - wants a big value, but will get a low value to discourage a draw
#                     return -999999
#                 else:
#                     # Miniimizing player - wants a low value, but will get a high value to discourage a draw
#                     return 999999
#
#     if time.time() >= stopTime:
#         return sum(eval.SimplifiedEvaluation(board), eval.TableScore(board, eval.isEndGame(board)))
#
#     cpy = board.copy(stack=False)
#     cpy.push(move)
#     if cpy.turn == chess.WHITE:
#         # Maximize
#         value = -float('inf')
#         for subMove in cpy.legal_moves:
#             value = max(value, alphaBetaFailSoft(cpy, subMove, stopTime, alpha, beta))
#
#             if value >= beta:
#                 break
#
#             # fail-hard: update after if-statement
#             alpha = max(alpha, value)
#     else:
#         # Minimize
#         value = float('inf')
#         for subMove in cpy.legal_moves:
#             value = min(value, alphaBetaFailSoft(cpy, subMove, stopTime, alpha, beta))
#             # Note to self, only have one of the two below (fail-soft of fail-hard) uncommented
#
#             # fail-soft: update before if-statement
#             beta = min(beta, value)
#
#             if value >= beta:
#                 break
#     return value
#
