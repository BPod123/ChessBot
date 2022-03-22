import numpy as np

# from FastChess.Piece import *
# import cython
# GameState = cython.struct(white=cython.in)


# class Board(object):
#     turn = WHITE
#     board = np.array([
#         [WR, WN, WB, WQ, WK, WB, WN, WR],
#         [WP, WP, WP, WP, WP, WP, WP, WP],
#         [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
#         [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
#         [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
#         [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
#         [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
#         [BP, BP, BP, BP, BP, BP, BP, BP],
#         [BR, BN, BB, BQ, BK, BB, BN, BR]
#     ], dtype=PieceType)
#     moveStack = []
#
#     def __init__(self, turn: Color, matrix=None, moveStack=None, castlingRights=uint8(15)):
#         self.turn = turn
#         if matrix is None:
#             self.board = np.array([
#                 [WR, WN, WB, WQ, WK, WB, WN, WR],
#                 [WP, WP, WP, WP, WP, WP, WP, WP],
#                 [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
#                 [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
#                 [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
#                 [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
#                 [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
#                 [BP, BP, BP, BP, BP, BP, BP, BP],
#                 [BR, BN, BB, BQ, BK, BB, BN, BR]
#             ], dtype=PieceType)
#         else:
#             self.board = matrix
#         self.moveStack = moveStack if moveStack is not None else []
#         if moveStack is None:
#             self.moveStack = []
#         # 2^0 = White King side castle, 2^1 = White Queen side castle,
#         # 2^2 = Black King side casle, 2^3 = Black Queen side castle
#         self.castlingRights = castlingRights
#
#     def __copy__(self):
#         """
#         :return: A shallow copy of the Board, with only the last move made remaining in the moveStack (for en passant)
#         """
#         if len(self.moveStack) > 0:
#             return Board(self.turn, self.board.copy(), [self.moveStack[-1]], self.castlingRights)
#
#     def deepCopy(self):
#         return Board(self.turn, self.board.copy(), self.moveStack.copy(), self.castlingRights)