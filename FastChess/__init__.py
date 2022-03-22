import numpy as np
from numba import jit, uint8, none, int8, typed, types

Square = int8
SQUARES = [
    A1, B1, C1, D1, E1, F1, G1, H1,
    A2, B2, C2, D2, E2, F2, G2, H2,
    A3, B3, C3, D3, E3, F3, G3, H3,
    A4, B4, C4, D4, E4, F4, G4, H4,
    A5, B5, C5, D5, E5, F5, G5, H5,
    A6, B6, C6, D6, E6, F6, G6, H6,
    A7, B7, C7, D7, E7, F7, G7, H7,
    A8, B8, C8, D8, E8, F8, G8, H8
] = np.array([Square(i) for i in range(64)], dtype=Square)
PROMOTIONS = [
    A1N, A1B, A1R, A1Q,
    B1N, B1B, B1R, B1Q,
    C1N, C1B, C1R, C1Q,
    D1N, D1B, D1R, D1Q,
    E1N, E1B, E1R, E1Q,
    F1N, F1B, F1R, F1Q,
    G1N, G1B, G1R, G1Q,
    H1N, H1B, H1R, H1Q,
    A8N, A8B, A8R, A8Q,
    B8N, B8B, B8R, B8Q,
    C8N, C8B, C8R, C8Q,
    D8N, D8B, D8R, D8Q,
    E8N, E8B, E8R, E8Q,
    F8N, F8B, F8R, F8Q,
    G8N, G8B, G8R, G8Q,
    H8N, H8B, H8R, H8Q
] = np.array([Square(i) for i in range(-32, 0)] + [Square(i) for i in range(64, 96)], dtype=Square)

Color = bool
PieceType = int8
PromotionType = int8

COLORS = [WHITE, BLACK] = np.array([True, False], dtype=bool)
COLOR_NAMES = ["black", "white"]


PIECE_TYPES = [PAWN, KNIGHT, BISHOP, ROOK, QUEEN, KING] = np.array(range(1, 7), dtype=PieceType)

PROMOTION_TYPES = [NO_PROMO, KNIGHT_PROMO, BISHOP_PROMO, ROOK_PROMO, QUEEN_PROMO] = np.array(range(5), dtype=PromotionType)

