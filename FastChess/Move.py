from numba.experimental import jitclass
from numba import none
from FastChess import Square, PromotionType, NO_PROMO, KNIGHT_PROMO, BISHOP_PROMO, ROOK_PROMO, QUEEN_PROMO
from FastChess import KNIGHT, BISHOP, ROOK, QUEEN
@jitclass([('from_square', Square), ('to_square', Square), ('promotion', PromotionType)])
class Move(object):
    def init(self, from_square, to_square, promotion):
        self.from_square = from_square
        self.to_square = to_square
        self.promotion = promotion
    @property
    def isPromotion(self):
        return self.promotion != NO_PROMO
    @property
    def promotedPiece(self):
        if self.promotion == QUEEN_PROMO:
            return QUEEN
        elif self.promotion == ROOK_PROMO:
            return ROOK
        elif self.promotion == BISHOP_PROMO:
            return BISHOP
        elif self.promotion == KNIGHT_PROMO:
            return KNIGHT
        else:
            return none
    def __repr__(self):
        row, col =





