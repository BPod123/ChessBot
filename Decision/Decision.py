import chess
import Evaluation.Evaluation as eval
from time import time, sleep
from multiprocessing import Pool, cpu_count


class ChessNodeData(object):
    board: chess.Board
    move: chess.Move

    def __init__(self, chessBoard: chess.Board, move=None, value=None, simpleScore=None,
                 tableScore=None):
        """
        :param chessBoard:
        :param move: chess.Move, Defaults to None (for root node).
            All non root nodes should have a move.
        :param value: sum of the simple and table scores, will be overridden if game is over
        :param simpleScore:
        :param tableScore:
        """
        self.board = chessBoard
        self.move = move
        self._children = None
        self.isLeaf = self.board.is_game_over()
        if self.isLeaf:
            outcome = self.board.outcome()
            if outcome.winner is not None:
                if outcome.winner == chess.WHITE:
                    # White is the maximizing player and wants the highest score
                    self.value = float("inf")
                else:
                    # Black is the minimizing player and wants the lowest score
                    self.value = -float("inf")
            else:
                # It is a draw. Give white a low score and black a high score
                if self.board.turn == chess.WHITE:
                    self.value = -999999
                else:
                    self.value = 999999
            self.simpleScore, self.tableScore = self.value, self.value
        elif value is not None:
            self.value = value
            self.simpleScore, self.tableScore = simpleScore, tableScore
        else:
            self.simpleScore = eval.SimplifiedEvaluation(self.board)
            self.tableScore = eval.TableScoreEvaluate(self.board)
            self.value = self.simpleScore + self.tableScore
    def __repr__(self):
        if self.move is not None:
            return str(self.move)
        return str(self.board)

    @property
    def children(self):
        if self._children is None:
            if self.board.is_game_over():
                return None
            self._children = []
            for move in self.board.legal_moves:
                newSimpleScore = eval.SimplifiedEvaluationMoveScore(self.board, move, self.simpleScore)
                newTableScore = eval.TableMoveScore(self.board, move, self.tableScore)
                cpy = self.board.copy(stack=False)
                cpy.push(move)
                self._children.append(
                    ChessNodeData(cpy, move, newSimpleScore + newTableScore, newSimpleScore, newTableScore))
            self._children.sort(key=lambda x: x.value)
        return self._children


def IDDFS(root: ChessNodeData, allowedTime, skipMoves: list, failSoft: bool):
    """
    Iterative Deepening DFS
    :param failSoft: If true, will do fail-soft alpha beta pruning. otherwise will do fail-hard alpha beta pruning.
    :param skipMoves: List of moves to not consider
    Defaults to fail-soft alpha beta pruning.
    :param root: ChessNodeData - The current board
    :param allowedTime: The time allowed for evaluating moves
    :return: The best move to make
    """

    stopTime = time() + allowedTime
    depth = 0
    maximizing = root.board.turn == chess.WHITE
    bestMoves, bestScore = set(), -float('inf') if maximizing else float('inf')

    if root.children is None:
        return None
    func = FailSoftAlphaBeta if failSoft else FailHardAlphaBeta
    while stopTime - time() > 0:
        newBestMoves, bestScore = set(), -float('inf') if maximizing else float('inf')
        stoppedEarly = False
        for child in root.children:
            if child.move in skipMoves:
                continue
            score, stoppedEarly = func(child, depth, time() + allowedTime / len(root.children))

            if stoppedEarly:
                break
            if score == bestScore:
                newBestMoves.add(child.move)
            elif (maximizing and score > bestScore) or (not maximizing and score < bestScore):
                newBestMoves.clear()
                newBestMoves.add(child.move)
                bestScore = score
        if not stoppedEarly:
            bestMoves = newBestMoves
        else:
            break
        depth += 1
    return bestMoves, bestScore


def IDDFSParallel(root: ChessNodeData, allowedTime, numCores: int, skipMoves: list, failSoft: bool):
    """
    Iterative Deepening DFS
    :param numCores: The maximum number of cpu cores to use
    :param skipMoves: List of moves to not consider
    :param failSoft: If true, will do fail-soft alpha beta pruning. otherwise will do fail-hard alpha beta pruning.
    Defaults to fail-soft alpha beta pruning.
    :param root: ChessNodeData - The current board
    :param allowedTime: The time allowed for evaluating moves
    :return: The best move to make
    """
    startTime = time()
    stopTime = startTime + allowedTime
    # stopTime = time() + allowedTime
    depth = 0
    maximizing = root.board.turn == chess.WHITE
    bestMoves, bestScore = set(), None

    if root.children is None:
        return None
    func = FailSoftAlphaBeta if failSoft else FailHardAlphaBeta
    pool = Pool(numCores)
    while stopTime - time() > 0:
        newBestMoves, bestScore = set(), -float('inf') if maximizing else float('inf')
        stoppedEarly = False

        childResults = []
        for child in root.children:
            if child.move in skipMoves:
                continue
            childResults.append((child, pool.apply_async(func, args=(child, depth, stopTime))))
            for child, scoreStoppedEarly in childResults:
                score, stoppedEarly = scoreStoppedEarly.get()
                if stoppedEarly:
                    break
                if score == bestScore:
                    newBestMoves.add(child.move)
                elif (maximizing and score > bestScore) or (not maximizing and score < bestScore):
                    newBestMoves.clear()
                    newBestMoves.add(child.move)
                    bestScore = score
        if not stoppedEarly:
            bestMoves = newBestMoves
        else:
            break
        depth += 1
    retTime = time()
    pool.close()
    pool.join()
    return bestMoves, bestScore


def FailSoftAlphaBeta(node: ChessNodeData, depth: int, stopTime: float, alpha=-float('inf'), beta=float('inf')):
    if node.isLeaf or depth == 0:
        return node.value, False
    else:
        stopEarly = False
        stoppedEarly = False
        if node.board.turn == chess.WHITE:
            # Maximizing
            value = -float('inf')
            for child in node.children:
                if stopEarly:
                    stoppedEarly = True
                    break
                newValue, stoppedEarly = FailSoftAlphaBeta(child, depth - 1, stopTime, alpha, beta)
                value = max(value, newValue)
                # fail-soft: update before if-statement
                alpha = max(alpha, value)
                if value >= beta:
                    break
                if stopTime - time() < 0:
                    stopEarly = True
        else:
            # Minimizing
            value = float('inf')
            for child in node.children:
                if stopEarly:
                    stoppedEarly = True
                    break
                newValue, stoppedEarly = FailSoftAlphaBeta(child, depth - 1, stopTime, alpha, beta)
                value = min(value, newValue)

                # fail-soft: update before if-statement
                beta = min(beta, value)

                if value <= alpha:
                    break

                if stopTime - time() < 0:
                    stopEarly = True
        return value, stoppedEarly


def FailHardAlphaBeta(node: ChessNodeData, depth: int, stopTime: float, alpha=-float('inf'), beta=float('inf')):
    if node.isLeaf or depth == 0:
        return node.value, False
    else:
        stopEarly = False
        stoppedEarly = False
        if node.board.turn == chess.WHITE:
            # Maximizing
            value = -float('inf')
            for child in node.children:
                if stopEarly:
                    stoppedEarly = True
                    break
                newValue, stoppedEarly = FailHardAlphaBeta(child, depth - 1, stopTime, alpha, beta)
                value = max(value, newValue)

                if value >= beta:
                    break

                # fail-hard: update before if-statement
                alpha = max(alpha, value)

                if stopTime - time() < 0:
                    stopEarly = True
        else:
            # Minimizing
            value = float('inf')
            for child in node.children:
                if stopEarly:
                    stoppedEarly = True
                    break
                newValue, stoppedEarly = FailHardAlphaBeta(child, depth - 1, stopTime, alpha, beta)
                value = min(value, newValue)

                if value <= alpha:
                    break

                # fail-soft: update before if-statement
                beta = min(beta, value)

                if stopTime - time() < 0:
                    stopEarly = True
        return value, stoppedEarly
