from numba.experimental import jitclass
from FastChess import PieceType, Color
@jitclass([('color', Color), ('pieceType', PieceType)])
class Piece(object):
    def __init__(self, color:Color, pieceType: PieceType):
        self.color = color
        self.pieceType = pieceType


