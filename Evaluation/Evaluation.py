import chess
from chess import PAWN, KNIGHT, BISHOP, ROOK, QUEEN, KING, WHITE, BLACK, Piece
import numpy as np
from collections import defaultdict
from numba import jit
from itertools import product

# Piece values in order of their hash values
#                        P     N   B    R    Q    K      p     n     b     r     q     k
PIECE_VALUES = np.array([100, 320, 330, 500, 900, 20000, -100, -320, -330, -500, -900, -20000])

SIMPLE_PIECE_VALUE_DICT = defaultdict(int,
                                      {Piece(PAWN, WHITE): 100, Piece(PAWN, BLACK): -100, Piece(ROOK, WHITE): 500,
                                       Piece(ROOK, BLACK): -500, Piece(QUEEN, WHITE): 900, Piece(QUEEN, BLACK): -900,
                                       Piece(BISHOP, WHITE): 330, Piece(BISHOP, BLACK): -330, Piece(KNIGHT, WHITE): 320,
                                       Piece(KNIGHT, BLACK): -320, Piece(KING, WHITE): 20000,
                                       Piece(KING, BLACK): -20000})
# https://www.chessprogramming.org/Simplified_Evaluation_Function
PAWN_SQUARE_TABLE = np.array([
    [ 0,   0,   0,  0,    0, 0, 0, 0],
    [50,  50,  50,  50,  50, 50, 50, 50],
    [10,  10,  20,  30,  30, 20, 10, 10],
    [ 5,   5,  10,  25,  25, 10, 5, 5],
    [ 0,   0,  0,   20,  20, 0, 0, 0],
    [ 5,  -5, -10,   0,   0, -10, -5, 5],
    [ 5,  10,  10, -20, -20, 10, 10, 5],
    [ 0,   0,  0, 0, 0,   0, 0, 0]
])

KNIGHT_SQUARE_TABLE = np.array([
    [-50, -40, -30, -30, -30, -30, -40, -50],
    [-40, -20, 0, 0, 0, 0, -20, -40],
    [-30, 0, 10, 15, 15, 10, 0, -30],
    [-30, 5, 15, 20, 20, 15, 5, -30],
    [-30, 0, 15, 20, 20, 15, 0, -30],
    [-30, 5, 10, 15, 15, 10, 5, -30],
    [-40, -20, 0, 5, 5, 0, -20, -40],
    [-50, -40, -30, -30, -30, -30, -40, -50],
])
BISHOP_SQUARE_TABLE = np.array([
    [-20, -10, -10, -10, -10, -10, -10, -20],
    [-10, 0, 0, 0, 0, 0, 0, -10],
    [-10, 0, 5, 10, 10, 5, 0, -10],
    [-10, 5, 5, 10, 10, 5, 5, -10],
    [-10, 0, 10, 10, 10, 10, 0, -10],
    [-10, 10, 10, 10, 10, 10, 10, -10],
    [-10, 5, 0, 0, 0, 0, 5, -10],
    [-20, -10, -10, -10, -10, -10, -10, -20],
])

ROOK_SQUARE_TABLE = np.array([
    [0, 0, 0, 0, 0, 0, 0, 0],
    [5, 10, 10, 10, 10, 10, 10, 5],
    [-5, 0, 0, 0, 0, 0, 0, -5],
    [-5, 0, 0, 0, 0, 0, 0, -5],
    [-5, 0, 0, 0, 0, 0, 0, -5],
    [-5, 0, 0, 0, 0, 0, 0, -5],
    [-5, 0, 0, 0, 0, 0, 0, -5],
    [0, 0, 0, 5, 5, 0, 0, 0],
])
QUEEN_SQUARE_TABLE = np.array([
    [-20, -10, -10, -5, -5, -10, -10, -20],
    [-10, 0, 0, 0, 0, 0, 0, -10],
    [-10, 0, 5, 5, 5, 5, 0, -10],
    [-5, 0, 5, 5, 5, 5, 0, -5],
    [0, 0, 5, 5, 5, 5, 0, -5],
    [-10, 5, 5, 5, 5, 5, 0, -10],
    [-10, 0, 5, 0, 0, 0, 0, -10],
    [-20, -10, -10, -5, -5, -10, -10, -20],
])
KING_MID_GAME_SQUARE_TABLE = np.array([
    [-30, -40, -40, -50, -50, -40, -40, -30],
    [-30, -40, -40, -50, -50, -40, -40, -30],
    [-30, -40, -40, -50, -50, -40, -40, -30],
    [-30, -40, -40, -50, -50, -40, -40, -30],
    [-20, -30, -30, -40, -40, -30, -30, -20],
    [-10, -20, -20, -20, -20, -20, -20, -10],
    [20, 20, 0, 0, 0, 0, 20, 20],
    [20, 30, 10, 0, 0, 10, 30, 20]
])
KING_END_GAME_SQUARE_TABLE = np.array([
    [-50, -40, -30, -20, -20, -30, -40, -50],
    [-30, -20, -10, 0, 0, -10, -20, -30],
    [-30, -10, 20, 30, 30, 20, -10, -30],
    [-30, -10, 30, 40, 40, 30, -10, -30],
    [-30, -10, 30, 40, 40, 30, -10, -30],
    [-30, -10, 20, 30, 30, 20, -10, -30],
    [-30, -30, 0, 0, 0, 0, -30, -30],
    [-50, -30, -30, -30, -30, -30, -30, -50]
])
# Square tables from black's perspective
PAWN_SQUARE_TABLE_FLIPPED = -np.flipud(PAWN_SQUARE_TABLE)
KNIGHT_SQUARE_TABLE_FLIPPED = -np.flipud(KNIGHT_SQUARE_TABLE)
BISHOP_SQUARE_TABLE_FLIPPED = -np.flipud(BISHOP_SQUARE_TABLE)
ROOK_SQUARE_TABLE_FLIPPED = -np.flipud(ROOK_SQUARE_TABLE)
QUEEN_SQUARE_TABLE_FLIPPED = -np.flipud(QUEEN_SQUARE_TABLE)
KING_MID_GAME_SQUARE_TABLE_FLIPPED = -np.flipud(KING_MID_GAME_SQUARE_TABLE)
KING_END_GAME_SQUARE_TABLE_FLIPPED = -np.flipud(KING_END_GAME_SQUARE_TABLE)


#@jit
def SimplePieceScore(piece: chess.Piece):
    return PIECE_VALUES[piece.__hash__()]
#@jit
def SimplifiedEvaluationMoveScore(board: chess.Board, move: chess.Move, simpleScore:float):
    """
    :param board: chess Board
    :param move: chess Move
    :param simpleScore: The current simplified evaluation of the board
    :return: The simplified evaluation score of the board after move is made
    """
    startPiece, endPiece = board.piece_at(move.from_square), board.piece_at(move.to_square)
    score = simpleScore
    if move.promotion is not None:
        score = score - SimplePieceScore(startPiece) + SimplePieceScore(Piece(move.promotion, startPiece.color))
    if endPiece is not None:
        # A piece is being captured
        score -= SimplePieceScore(endPiece)
    return score

#@jit
def SimplifiedEvaluation(board: chess.Board):
    """
    This method of board evaluation only considers what pieces are on the board, and not their positions.
    The following priority rules are adhered to:
    1. B > N > 3P
    2. R + 2P > B + N > R + P
    3. Q + P =  2R
    The piece values are as follows:
    P = 100,     N = 320,     B = 330,     R = 500,     Q = 900,     K = 20000
    :param board: chess board
    :return: An integer score for the board
    """
    return sum([len(board.pieces(pieceType, color)) * SimplePieceScore(Piece(pieceType, color)) for pieceType, color in
                product(range(1, 7), range(2))])


@jit
def SquareToCoordinate(chessSquare: int):
    return chessSquare // 8, chessSquare % 8


@jit
def CoordinateToSquare(x: int, y: int):
    return x * 8 + y % 8


#@jit
def numMinorPieces(board: chess.Board, color: chess.Color):
    return len(board.pieces(KNIGHT, color)) + len(board.pieces(BISHOP, color)) + len(board.pieces(ROOK, color))


#@jit
def isEndGame(board: chess.Board):
    """
    :return: True if the any of the following end-game conditions are met:
    1. Both sides have no queens
    2. Every side that has a queen has at most one other minor piece (R B N)
    3. A side has more than one queen (a pawn was promoted)
    """
    whiteQueens = len(board.pieces(PAWN, WHITE))
    blackQueens = len(board.pieces(PAWN, BLACK))
    if whiteQueens == 0 and blackQueens == 0:
        return True
    elif (whiteQueens > 0 and numMinorPieces(board, chess.WHITE) <= 1) or (
            blackQueens > 0 and numMinorPieces(board, chess.BLACK) <= 1):
        return True
    elif whiteQueens > 1 or blackQueens > 1:
        return True
    return False


#@jit
def PieceTableScore(piece: chess.Piece, square: chess.Square, endGame: bool):
    """
    :param piece: A chess piece
    :param square: An int representing a square on the board
    :param endGame: a boolean that affects the value for kings
    :return: The table score contribution of piece at square
    """
    coords = SquareToCoordinate(square)
    if piece.piece_type == PAWN:
        return PAWN_SQUARE_TABLE[coords] if piece.color else PAWN_SQUARE_TABLE_FLIPPED[coords]
    elif piece.piece_type == ROOK:
        return ROOK_SQUARE_TABLE[coords] if piece.color else ROOK_SQUARE_TABLE_FLIPPED[coords]
    elif piece.piece_type == KING:
        if endGame:
            return KING_END_GAME_SQUARE_TABLE[coords] if piece.color else KING_END_GAME_SQUARE_TABLE_FLIPPED[coords]
        else:
            return KING_MID_GAME_SQUARE_TABLE[coords] if piece.color else KING_MID_GAME_SQUARE_TABLE_FLIPPED[coords]
    elif piece.piece_type == QUEEN:
        return QUEEN_SQUARE_TABLE[coords] if piece.color else QUEEN_SQUARE_TABLE_FLIPPED[coords]
    elif piece.piece_type == BISHOP:
        return BISHOP_SQUARE_TABLE[coords] if piece.color else BISHOP_SQUARE_TABLE_FLIPPED[coords]
    elif piece.piece_type == KNIGHT:
        return KNIGHT_SQUARE_TABLE[coords] if piece.color else KNIGHT_SQUARE_TABLE_FLIPPED[coords]
    raise Exception("Un-accounted for piece type passed in: {0}".format(piece))


#@jit
def isCastle(board: chess.Board, move: chess.Move):
    """
    :return: True if the move is castling
    """
    startPiece = board.piece_at(move.from_square)
    if startPiece.piece_type == KING:
        if startPiece.color == WHITE:
            return move.from_square == chess.E1 and (move.to_square == chess.G1 or move.to_square == chess.C1)
        else:
            return move.from_square == chess.E8 and (move.to_square == chess.G8 or move.to_square == chess.C8)
    return False


#@jit
def TableMoveScore(board: chess.Board, move: chess.Move, tableScore: float):
    """
    :param board: A chess Board
    :param move: A legal move to make on the board
    :param tableScore: The table score of the passed in board
    :return: Table score of the board after the move is made
    """
    movedPiece = board.piece_at(move.from_square)
    # Subtract the value of moved piece's starting position table score
    if movedPiece.piece_type == KING:
        endGame = isEndGame(board)
        if isCastle(board, move):
            rook = Piece(ROOK, movedPiece.color)
            king = movedPiece
            kingSide = move.to_square == chess.G1 or move.to_square == chess.G8

            if kingSide:
                if movedPiece.color == WHITE:
                    rookStart, rookEnd, kingStart, kingEnd = chess.H1, chess.F1, chess.E1, chess.G1
                else:
                    rookStart, rookEnd, kingStart, kingEnd = chess.H8, chess.F8, chess.E8, chess.G8
            else:
                if movedPiece.color == WHITE:
                    rookStart, rookEnd, kingStart, kingEnd = chess.A1, chess.D1, chess.E1, chess.C1
                else:
                    rookStart, rookEnd, kingStart, kingEnd = chess.A8, chess.D8, chess.E8, chess.C8
            score = tableScore - PieceTableScore(rook, rookStart, True) + PieceTableScore(rook, rookEnd,
                                                                                          True) - PieceTableScore(
                king, kingStart, endGame) + PieceTableScore(king, kingEnd, endGame)
        else:
            # If the king captures a piece, then it could triger the end game condition
            targetPiece = board.piece_at(move.to_square)
            if targetPiece is not None and targetPiece.color != movedPiece.color:
                # The king is capturing a piece
                cpy = board.copy(stack=False)
                cpy.push(move)
                postMoveEndGame = endGame or isEndGame(cpy)
                score = tableScore - PieceTableScore(movedPiece, move.from_square, endGame) - PieceTableScore(
                    targetPiece, move.to_square, endGame) + PieceTableScore(movedPiece, move.from_square,
                                                                            postMoveEndGame)
            else:
                score = tableScore - PieceTableScore(movedPiece, move.from_square, endGame) + PieceTableScore(
                    movedPiece, move.to_square, endGame)
    else:
        score = tableScore - PieceTableScore(board.piece_at(move.from_square), move.from_square, True)
        targetPiece = board.piece_at(move.to_square)
        if targetPiece is not None:
            score -= PieceTableScore(targetPiece, move.to_square, True)
        if move.promotion is not None:
            score += PieceTableScore(Piece(move.promotion, movedPiece.color), move.to_square, True)
        else:
            score += PieceTableScore(movedPiece, move.to_square, True)
    return score


#@jit
def TableScoreEvaluate(board: chess.Board, endGame=None):
    """
    :param board: Chess board
    :param endGame: Bool, used to determine which king square taable to used. If None, then it will be calculated.
    :return: The sum of position valuations for each piece on the board
    """
    if endGame is None:
        endGame = isEndGame(board)
    pieceMap = board.piece_map()
    return sum([PieceTableScore(pieceMap[square], square, endGame) for square in pieceMap])

def subBoard(board: chess.Board, move: chess.Move):
    cpy = board.copy(stack=False)
    cpy.push(move)
    return cpy

def SimplifiedPlusTableEvaluation(board:chess.Board):
    return SimplifiedEvaluation(board) + TableScoreEvaluate(board)
if __name__ == '__main__':
    board = chess.Board()
    A1, B1, C1, D1, E1, F1, G1, H1, A2, B2, C2, D2, E2, F2, G2, H2, A3, B3, C3, D3, E3, F3, G3, H3, A4, B4, C4, D4, E4, F4, G4, H4, A5, B5, C5, D5, E5, F5, G5, H5, A6, B6, C6, D6, E6, F6, G6, H6, A7, B7, C7, D7, E7, F7, G7, H7, A8, B8, C8, D8, E8, F8, G8, H8 = range(64)
    from chess import Move
    moves = [Move(x[0], x[1]) for x in [(D2, D4), (C7, C6), (C1, G5), (D8, C7), (D1, D3), (G7, G6), (D3, E3), (G8, H6), (E3, E4), (F8, G7), (E4, E7)]]
    del A1, B1, C1, D1, E1, F1, G1, H1, A2, B2, C2, D2, E2, F2, G2, H2, A3, B3, C3, D3, E3, F3, G3, H3, A4, B4, C4, D4, E4, F4, G4, H4, A5, B5, C5, D5, E5, F5, G5, H5, A6, B6, C6, D6, E6, F6, G6, H6, A7, B7, C7, D7, E7, F7, G7, H7, A8, B8, C8, D8, E8, F8, G8, H8
    for i in range(len(moves)):
        board.push(moves[i])
    z = 3
