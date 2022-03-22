import chess
from multiprocessing import Pool, cpu_count
from random import randint


class GameHandler(object):
    def __init__(self, lookAhead: int, maxCores=10):
        self.board = chess.Board()
        self.lookAhead = lookAhead
        self.maxCores = maxCores
        self.boardDict = {}

    def pickMove(self):
        # boardDict = {}
        move, score = bestMove(self.board, self.lookAhead, -float('inf'))
        return move

    # def pickMoveSingleThread(self):
    #     topMove, topMoveScore = None, -float("inf")
    #     numCores = int(min(min(cpu_count(), len(list(self.board.legal_moves))), self.maxCores))
    #     # pool = Pool(numCores)
    #     # asyncResults = []
    #     results = []
    #     for move in self.board.legal_moves:
    #         cpy = self.board.copy(stack=False)
    #         cpy.push(move)
    #         # asyncResults.append((move, pool.apply_async(bestMove, args=(cpy, self.lookAhead))))
    #         results.append((move, bestMove(cpy, self.lookAhead)))
    #
    #     # pool.close()
    #     # pool.join()
    #     # for move, asyncRes in asyncResults:
    #     for move, result in results:
    #         #     result = asyncRes.get()
    #         score = result if self.lookAhead == 1 else result[1]
    #         if score > topMoveScore:
    #             topMoveScore = score
    #             topMove = move
    #     return topMove

    def pickMoveParallel(self, caching=False):
        try:
            numCores = int(min(min(cpu_count(), len(list(self.board.legal_moves))), self.maxCores))
            pool = Pool(numCores)
            asyncResults = []
            dicts = []
            for move in self.board.legal_moves:
                cpy = self.board.copy(stack=False)
                cpy.push(move)
                dicts.append(dict())
                if caching:
                    asyncResults.append((move, pool.apply_async(bestMoveCaching, args=(cpy, self.lookAhead, -float('inf'), self.boardDict, dicts[-1]))))
                else:
                    asyncResults.append((move, pool.apply_async(bestMove, args=(
                    cpy, self.lookAhead, -float('inf')))))
            pool.close()
            pool.join()
            topMoves, topMoveScore = [], -float("inf")
            for move, asyncRes in asyncResults:
                result = asyncRes.get()
                if isinstance(result, tuple):
                    score = result[-1]
                else:
                    score = result
                # score = result if self.lookAhead == 1 else result[1]
                if score > topMoveScore:
                    topMoves.clear()
                    topMoveScore = score
                if score >= topMoveScore:
                    topMoves.append(move)
            for d in dicts:
                for key in d:
                    self.boardDict[key] = d[key]
            if len(topMoves) == 0:
                return list(self.board.legal_moves)[randint(0, len(list(self.board.legal_moves)) - 1)]
            return topMoves[randint(0, len(topMoves) - 1)]
        except:
            self.boardDict.clear()
            return self.pickMoveParallel()
        #
        # #
        # #     if self.lookAhead == 1:
        # #         score = bestMove(cpy, self.lookAhead - 1)
        # #     else:
        # #         topSubMove, score = bestMove(cpy, self.lookAhead - 1)
        # #     if score > topMoveScore or topMove is None:
        # #         topMoveScore = score
        # #         topMove = move
        # # return topMove, topMoveScore
        # # move, score = bestMove(self.board, self.lookAhead)
        # return move

    def makeMove(self, move):
        self.board.push(move)


def boardHash(board: chess.Board):
    return (str(board), board.castling_rights).__hash__()


def boardScore(board: chess.Board):
    if board.is_checkmate():
        return -float("inf")

    if board.turn == chess.WHITE:
        score1 = sum([
            1 if x == 'P' else 3 if x == 'N' or x == 'B' else 5 if x == 'R' else 9 if x == 'Q' else 900 if x == 'K' else 0
            for x in str(board)])
        score2 = sum([
            1 if x == 'p' else 3 if x == 'n' or x == 'b' else 5 if x == 'r' else 9 if x == 'q' else 900 if x == 'k' else 0
            for x in str(board)])
    else:
        score2 = sum([
            1 if x == 'P' else 3 if x == 'N' or x == 'B' else 5 if x == 'R' else 9 if x == 'Q' else 900 if x == 'K' else 0
            for x in str(board)])
        score1 = sum([
            1 if x == 'p' else 3 if x == 'n' or x == 'b' else 5 if x == 'r' else 9 if x == 'q' else 900 if x == 'k' else 0
            for x in str(board)])
    return score1 - score2


def subBoard(board: chess.Board, move):
    cpy = board.copy(stack=False)
    cpy.push(move)
    return cpy

def bestMove(board: chess.Board, lookAhead: int, minimax):
    """
        :param minimax: The lowest score of a parent move - used for pruning

        :param board: Chess Board
        :param lookAhead: Number of turns to look ahead when considering score. If 0,
        will return  score1 - score2 where score1 is the sum of the point values for whoever's turn it is and
        score2 is the sum of the point values for whoever's turn it is not.
        :return: The move with the highest score and the score for that
        """


    if board.is_checkmate():
        return -float("inf")
    if lookAhead == 0:
        return boardScore(board)
    else:
        expandMoves, expandMoveScore = [], -float('inf')
        moves = list(board.legal_moves)
        moves.sort(key=lambda move: boardScore(subBoard(board, move)))
        for move in moves:
            cpyScore = boardScore(subBoard(board, move))
            if cpyScore > minimax:
                expandMoves.clear()
                expandMoves.append(move)
                expandMoveScore = cpyScore
            elif cpyScore == minimax:
                expandMoves.append(move)
            del move
        topMoves = []
        topMoveScore = expandMoveScore
        for move in expandMoves:
            cpy = subBoard(board, move)

            score = bestMove(cpy, lookAhead - 1, expandMoveScore)

            if isinstance(score, tuple):
                score = score[-1]

            if score > topMoveScore:
                topMoves.clear()
                topMoveScore = score
            if score >= topMoveScore:
                topMoves.append(move)
        if len(topMoves) == 0:
            if len(expandMoves) == 0:
                return minimax
            topMove = expandMoves[randint(0, len(expandMoves) - 1)]
        else:
            topMove = topMoves[randint(0, len(topMoves) - 1)]
        # del expandMoves, topMoves
        return topMove, topMoveScore

def bestMoveCaching(board: chess.Board, lookAhead: int, minimax, boardDict, newDict):
    """
        :param newDict: A dict that can be edited
        :param boardDict: A dictionary mapping viewed board states to their best moves. Will not be edited during function
        :param minimax: The lowest score of a parent move - used for pruning

        :param board: Chess Board
        :param lookAhead: Number of turns to look ahead when considering score. If 0,
        will return  score1 - score2 where score1 is the sum of the point values for whoever's turn it is and
        score2 is the sum of the point values for whoever's turn it is not.
        :return: The move with the highest score and the score for that
        """

    if boardHash(board) in boardDict:
        return boardDict[boardHash(board)]
    elif boardHash(board) in newDict:
        return newDict[boardHash(board)]
    if board.is_checkmate():
        return -float("inf")
    if lookAhead == 0:
        return boardScore(board)
    else:
        expandMoves, expandMoveScore = [], -float('inf')
        moves = list(board.legal_moves)
        moves.sort(key=lambda move: boardScore(subBoard(board, move)))
        for move in moves:
            cpyScore = boardScore(subBoard(board, move))
            if cpyScore > minimax:
                expandMoves.clear()
                expandMoves.append(move)
                expandMoveScore = cpyScore
            elif cpyScore == minimax:
                expandMoves.append(move)
            del move
        topMoves = []
        topMoveScore = expandMoveScore
        for move in expandMoves:
            cpy = subBoard(board, move)

            score = bestMoveCaching(cpy, lookAhead - 1, expandMoveScore, boardDict, newDict)

            if isinstance(score, tuple):
                score = score[-1]

            if score > topMoveScore:
                topMoves.clear()
                topMoveScore = score
            if score >= topMoveScore:
                topMoves.append(move)
        if len(topMoves) == 0:
            if len(expandMoves) == 0:
                return minimax
            topMove = expandMoves[randint(0, len(expandMoves) - 1)]
        else:
            topMove = topMoves[randint(0, len(topMoves) - 1)]
        del expandMoves, topMoves
        newDict[boardHash(board)] = topMove, topMoveScore
        return topMove, topMoveScore
def moveScore(board: chess.Board, move: chess.Move, lookahead: int):
    cpy = board.copy(stack=False)
    cpy.push(move)
    moveScore = boardScore(cpy)
    if lookahead == 0:
        return moveScore


