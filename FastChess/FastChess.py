from numba import jit, uint8, none, int8
import numpy as np
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
PIECE_SYMBOLS = [None, "p", "n", "b", "r", "q", "k"]
PIECE_NAMES = [None, "pawn", "knight", "bishop", "rook", "queen", "king"]
PIECES = [EMPTY, WP, WN, WB, WR, WQ, WK, BP, BN, BB, BR, BQ, BK] = np.array(range(12), dtype=PieceType)


@jit(int8(Square))
def getRow(position: Square):
    """
    :param position: The int value of a square
    :return: The row of the position
    """
    return int8(position // 8)


@jit(int8(Square))
def getCol(position: Square):
    """
    :param position: The int value of a square
    :return: The column of the position
    """
    return int8(position % 8)


@jit(Square(int8, int8))
def getPosition(row: int8, col: int8):
    """
    :return: Square at row and col
    """
    return Square(row * 8 + col)
@jit(PieceType(Square))
def pieceAtSquare(board:np.ndarray, square:Square):
    """
    :return: A PieceType
    """
    if square in PROMOTIONS:
        # If the square is a promo
        pass
    else:
        row, col = getRow(square), getCol(square)
        return board[row, col]


@jit
def getUp(color: Color, position: Square, numSpaces: int8):
    """
    :return:  The square of the position amount up, or none if it is out of bounds
    """
    row = getRow(position)
    if color:
        if row + numSpaces <= 7:
            return Square(position + numSpaces * 8)
        return none
    elif row - numSpaces >= 0:
        return Square(position - numSpaces * 8)
    return none


@jit
def getDown(color: Color, position: Square, numSpaces: int8):
    """
    :return:  The square of the position amount down, or none if it is out of bounds
    """
    return getUp(not color, position, numSpaces)


@jit
def getLeft(color: Color, position: Square, numSpaces: int8):
    """
    :return:  The square of the position amount left, or none if it is out of bounds
    """
    col = getCol(position)
    if color:
        if col >= numSpaces:
            return int8(position - numSpaces)
    elif col + numSpaces <= 7:
        return int8(position + numSpaces)
    return none


@jit
def getRight(color: Color, position: Square, numSpaces: int8):
    """
    :return:  The square of the position amount up, or none if it is out of bounds
    """
    return getRight(not color, position, numSpaces)


@jit
def getDiagUL(color: Color, position: Square, numSpaces: int8):
    """
    :return:  The square of the position amount diagonal left and up, or none if it is out of bounds
    """
    left = getLeft(color, position, numSpaces)
    if left is not none:
        return getUp(color, left, numSpaces)
    return none


@jit
def getDiagDR(color: Color, position: Square, numSpaces: int8):
    """
    :return:  The square of the position amount diagonal right and down, or none if it is out of bounds
    """
    return getDiagUL(not color, position, numSpaces)


@jit
def getDiagUR(color: Color, position: Square, numSpaces: int8):
    """
    :return:  The square of the position amount diagonal right and up, or none if it is out of bounds
    """
    up = getUp(color, position, numSpaces)
    if up is not none:
        return getRight(color, position, numSpaces)
    return none


@jit
def getDiagDL(color: Color, position: Square, numSpaces: int8):
    """
    :return:  The square of the position amount diagonal right and down, or none if it is out of bounds
    """
    return getDiagUR(not color, position, numSpaces)


@jit
def IsPromotion(position: Square):
    return -32 <= position < 0 or 64 <= position < 96


@jit
def PromotionType(position: Square):
    return PieceType((position % 4) + 1)


@jit
def PromotionSquaresAt(position: Square):
    """
    :return: Any promotions that can take place at the square, none if there are none
    """
    if 8 <= position < 56:
        return none
    add = 0 if position < 8 else 32
    addCol4 = add + getCol(position) * 4
    return PROMOTIONS[addCol4: addCol4 + 4]


@jit
def PawnNormalMoves(color: Color, position: Square):
    """
    :return: A list of normal legal moves a pawn has from position.
    Takes promotions gained from moving forward into account.
    """
    moves = [getUp(color, position, 1)]
    row = getRow(position)
    if (color and row == 1) or (not color and row == 6):
        return np.array(moves + [getUp(color, position, 2)])
    elif IsPromotion(moves[0]):
        return PromotionSquaresAt(moves[0])


@jit
def KnightNormalMoves(position: Square):
    """
    :return: A list of normal legal moves a knight has from position
    """
    up1 = getUp(True, position, 1)
    uul = getDiagUL(True, up1, 1) if up1 is not none else none
    uur = getDiagUR(True, up1, 1) if up1 is not none else none
    down1 = getUp(True, position, 1)
    ddl = getDiagDL(True, down1, 1) if up1 is not none else none
    ddr = getDiagDR(True, down1, 1) if up1 is not none else none
    left1 = getLeft(True, position, 1)
    llu = getDiagUL(True, left1, 1) if left1 is not none else none
    lld = getDiagDL(True, left1, 1) if left1 is not none else none
    right1 = getRight(True, position, 1)
    rru = getDiagUR(True, right1, 1) if right1 is not none else none
    rrd = getDiagDR(True, right1, 1) if right1 is not none else none
    return np.array([x for x in [uul, uur, ddl, ddr, llu, lld, rru, rrd] if x is not none])


@jit
def BishopNormalMoves(position: Square):
    """
    :return: A list of normal legal moves a bishop has from position
    """
    maxDown, maxLeft = getRow(position), getCol(position)
    dl = [getDiagDL(True, position, i) for i in range(min(maxDown, maxLeft))]
    dr = [getDiagDR(True, position, i) for i in range(min(maxDown, 7 - maxLeft))]
    ul = [getDiagDL(True, position, i) for i in range(min(7 - maxDown, maxLeft))]
    ur = [getDiagDR(True, position, i) for i in range(min(7 - maxDown, 7 - maxLeft))]
    return ur + ul + dr + dl


@jit
def RookNormalMoves(position: Square):
    """
    :return: A list of normal legal moves a rook has from position
    """
    row, col = getRow(position), getCol(position)
    return [getPosition(i, col) for i in range(8)] + [getPosition(row, i) for i in range(8)]


@jit
def QueenNormalMoves(position: Square):
    """
    :return: A list of normal legal moves a queen has from position
    """
    return RookNormalMoves(position) + BishopNormalMoves(position)


@jit
def KingNormalMoves(position: Square):
    """
    :return: A list of normal legal moves a king has from position
    """
    return [x for x in [func(True, position, 1) for func in
                        [getUp, getDown, getLeft, getRight, getDiagUL, getDiagUR, getDiagDL, getDiagDR]] if
            x is not none]


class Board(object):
    turn = WHITE
    board = np.array([
        [WR, WN, WB, WQ, WK, WB, WN, WR],
        [WP, WP, WP, WP, WP, WP, WP, WP],
        [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
        [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
        [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
        [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
        [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
        [BP, BP, BP, BP, BP, BP, BP, BP],
        [BR, BN, BB, BQ, BK, BB, BN, BR]
    ], dtype=PieceType)
    moveStack = []

    def __init__(self, turn: Color, matrix=None, moveStack=None, castlingRights=uint8(15)):
        self.turn = turn
        if matrix is None:
            self.board = np.array([
                [WR, WN, WB, WQ, WK, WB, WN, WR],
                [WP, WP, WP, WP, WP, WP, WP, WP],
                [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
                [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
                [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
                [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
                [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
                [BP, BP, BP, BP, BP, BP, BP, BP],
                [BR, BN, BB, BQ, BK, BB, BN, BR]
            ], dtype=PieceType)
        else:
            self.board = matrix
        self.moveStack = moveStack if moveStack is not None else []
        if moveStack is None:
            self.moveStack = []
        # 2^0 = White King side castle, 2^1 = White Queen side castle,
        # 2^2 = Black King side casle, 2^3 = Black Queen side castle
        self.castlingRights = castlingRights

    def __copy__(self):
        """
        :return: A shallow copy of the Board, with only the last move made remaining in the moveStack (for en passant)
        """
        if len(self.moveStack) > 0:
            return Board(self.turn, self.board.copy(), [self.moveStack[-1]], self.castlingRights)

    def deepCopy(self):
        return Board(self.turn, self.board.copy(), self.moveStack.copy(), self.castlingRights)


@jit
def PsudoLegalMovesFromPosition(position:Square, turn:Color, board:np.ndarray, lastPieceMoved:PieceType, lastMoveFromSquare:Square, lastMoveToSquare:Square):
    """
    :pa
    :param turn: Whose turn it is
    :param board: The current state of a board
    :param lastPieceMoved: Used for determining if an en passant can happen
    :param lastMoveFromSquare: Used for determining if an en passant can happen
    :param lastMoveToSquare: Used for determining if an en passant can happen
    :return: An array of psuedo legal moves that can be made from the piece in this position. That is to say,
     that being in check is not accounted for.
     If no moves can be made, an empty list will be returned
    """
    moves = []
    piece = pieceAtSquare(position)
    if position == EMPTY:
        return []
    # if white turn and piece is black, return an empty list
    elif turn and piece in [BP, BN, BB, BR, BQ, BK]:
        return []
    # if black turn and piece is white, return an empty list
    elif not turn and piece in [WP, WN, WB, WR, WQ, WK]:
        return []


