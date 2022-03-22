import numpy as np
# Below are the starting templates for each pieces movement table
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

KING_SQUARE_TABLE = KING_MID_GAME_SQUARE_TABLE + KING_END_GAME_SQUARE_TABLE
# Square tables from black's perspective
PAWN_SQUARE_TABLE_FLIPPED = -np.flipud(PAWN_SQUARE_TABLE)
KNIGHT_SQUARE_TABLE_FLIPPED = -np.flipud(KNIGHT_SQUARE_TABLE)
BISHOP_SQUARE_TABLE_FLIPPED = -np.flipud(BISHOP_SQUARE_TABLE)
ROOK_SQUARE_TABLE_FLIPPED = -np.flipud(ROOK_SQUARE_TABLE)
QUEEN_SQUARE_TABLE_FLIPPED = -np.flipud(QUEEN_SQUARE_TABLE)
KING_MID_GAME_SQUARE_TABLE_FLIPPED = -np.flipud(KING_MID_GAME_SQUARE_TABLE)
KING_END_GAME_SQUARE_TABLE_FLIPPED = -np.flipud(KING_END_GAME_SQUARE_TABLE)
KING_SQUARE_TABLE_FLIPPED = -np.flipud(KING_SQUARE_TABLE)

templates = np.array([PAWN_SQUARE_TABLE, PAWN_SQUARE_TABLE_FLIPPED, KNIGHT_SQUARE_TABLE, KNIGHT_SQUARE_TABLE_FLIPPED,
                      BISHOP_SQUARE_TABLE, BISHOP_SQUARE_TABLE_FLIPPED, ROOK_SQUARE_TABLE, ROOK_SQUARE_TABLE_FLIPPED,
                      QUEEN_SQUARE_TABLE, QUEEN_SQUARE_TABLE_FLIPPED, KING_MID_GAME_SQUARE_TABLE,
                      KING_MID_GAME_SQUARE_TABLE_FLIPPED, KING_END_GAME_SQUARE_TABLE, KING_END_GAME_SQUARE_TABLE_FLIPPED,
                      KING_SQUARE_TABLE, KING_SQUARE_TABLE_FLIPPED])
templates_GenericKing = np.array([PAWN_SQUARE_TABLE, PAWN_SQUARE_TABLE_FLIPPED, KNIGHT_SQUARE_TABLE, KNIGHT_SQUARE_TABLE_FLIPPED,
                      BISHOP_SQUARE_TABLE, BISHOP_SQUARE_TABLE_FLIPPED, ROOK_SQUARE_TABLE, ROOK_SQUARE_TABLE_FLIPPED,
                      QUEEN_SQUARE_TABLE, QUEEN_SQUARE_TABLE_FLIPPED, KING_SQUARE_TABLE, KING_SQUARE_TABLE_FLIPPED])
templates_midGameEndGameKing = np.array([PAWN_SQUARE_TABLE, PAWN_SQUARE_TABLE_FLIPPED, KNIGHT_SQUARE_TABLE, KNIGHT_SQUARE_TABLE_FLIPPED,
                      BISHOP_SQUARE_TABLE, BISHOP_SQUARE_TABLE_FLIPPED, ROOK_SQUARE_TABLE, ROOK_SQUARE_TABLE_FLIPPED,
                      QUEEN_SQUARE_TABLE, QUEEN_SQUARE_TABLE_FLIPPED, KING_MID_GAME_SQUARE_TABLE,
                      KING_MID_GAME_SQUARE_TABLE_FLIPPED, KING_END_GAME_SQUARE_TABLE, KING_END_GAME_SQUARE_TABLE_FLIPPED,
                      ])


if __name__ == '__main__':
    pass