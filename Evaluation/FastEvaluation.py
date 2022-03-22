from FastChess import Board
def SimplifiedEvaluation(board: Board):
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
