##ifndef CHESS
##define CHESS

struct BOARD_STATE {
// 64 bits
unsigned long long whites;
// 64 bits
// first and last 8 bits are the white and black king positions.
// The middle 48 bits are a bitmap of all pawn locations.
unsigned long long kingsAndPawns;
// arrays of uint8's representing the square that a piece is on.
unsigned char* knights;
unsigned char* bishops;
unsigned char* rooks;
unsigned char* queens;
// The first 4 bits for castling: wk, wq, bk, bq; the last four bits are a number representing what column, if any,
// an en passent is legal. 0 is none, 1 is a, 2 is b, ...
unsigned char enPassantAndCastlingRights;
// true if white, false if black
bool turn;
} Board;
uint8 NOPIECE = 0;
uint8 PAWN = 1;
uint8 KNIGHT = 2;
uint8 BISHOP = 3;
uint8 ROOK = 4;
uint8 QUEEN = 5;
uint8 KING = 6;
bool WHITE = true;
bool BLACK = false;
struct MOVE{
uint8 from_square;
uint8 to_square;
uint8 promotion;
};
bool isGameOver(Board);
MOVE* legalMoves(Board);
int winner(Board); // Returns 0 if draw or game is not over, -1 if black won, 1 if white won


