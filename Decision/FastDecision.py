import chess
import Evaluation.Evaluation as eval
from time import time
from multiprocessing import Pool, cpu_count, Queue as MPQueue
from queue import Queue
from collections import defaultdict
import numpy as np

class ChessNode(object):
    board: chess.Board
    move: chess.Move
    superMove: chess.Move
    depth: int
    value: float

    def __init__(self, board: chess.Board, move, superMove, depth, value, evalFunc):
        """

        :param board:
        :param move: The last move made on the board to caused it to be in its current state
        :param superMove: The move at the top of the tree that is an ancestor of this node
        :param depth: How far from the current board in the game this node is
        :param value: The score of the board based on an evaluation function
        :param evalFunc: A function that takes a chess board as a parameter and returns a numerical
        score for the board.
        """
        self.board = board
        self.move = move

        self.depth = depth
        if self.depth == 1 and superMove is None:
            self.superMove = self.move
        else:
            self.superMove = superMove
        self.value = value
        self.evalFunc = evalFunc
        self._children = None
        # isTerminating and finalValue are for when alphabeta pruning determines there is no further use in
        # expanding this node
        self.isTerminating = False
        self.finalValue = None

    @property
    def isSuperMove(self):
        """
        :return: True if the this node is the immediate child of the root
        """
        return self.depth == 1

    @property
    def children(self):
        if self._children is None:
            self._children = []
            if not self.board.is_game_over():
                for move in self.board.legal_moves:
                    cpy = self.board.copy(stack=False)
                    cpy.push(move)
                    newValue = self.evalFunc(cpy)
                    self._children.append(
                        ChessNode(cpy, move, self.superMove, self.depth + 1, newValue, self.evalFunc))

        return self._children


    def __lt__(self, other):
        return self.depth < other.depth #or (self.depth == other.depth and self.value < other.value)

    def __le__(self, other):
        return self.depth < other.depth #or (self.depth == other.depth and self.value <= other.value)

    def __gt__(self, other):
        return self.depth > other.depth #or (self.depth == other.depth and self.value > other.value)

    def __ge__(self, other):
        return self.depth > other.depth #or (self.depth == other.depth and self.value >= other.value)

    def __eq__(self, other):
        return self.depth == other.depth #and self.value == other.value

    def __ne__(self, other):
        return self.depth != other.depth #or self.value != other.value
    def __hash__(self):
        return (str(self.board), self.move, self.superMove, self.value, self.depth).__hash__()














def IDDFS(board:chess.Board, drawBoards: set, failSoft: bool, allowedTime, maxDepth, evalFunc):
    """

    :param board: The starting board to do evaluations on
    :param drawBoards: A set of tuples (board string, turn) that have appeared twice already in the game.
    If a board in this set appears with the same persons turn, then there will be a draw by repetition.
    :param failSoft: If true, will do fail-soft alpha-beta pruning. If false,
    will do fail-hard alpha-beta pruning.
    :param allowedTime: The maximum amount of time to spend searching for the best move. If infinity,
    and depth is infinity, then will search forever.
    :param maxDepth: The depth of moves to search. If none or infinity and allowedTime is infinity, then
    will search forever.
    :param evalFunc: A function that takes a board as a parameter and returns a numerical score
    :return: A list of the best moves that can be made
    """
    queue = Queue()
    root = ChessNode(board, None, None, 0, evalFunc(board), evalFunc)
    for child in root.children:
        if (str(child.board), child.board.turn) not in drawBoards:
            queue.put((child, -float('inf'), float('inf')))
    maximizing = board.turn
    stopTime = time() + allowedTime
    depth = 1
    maxDepthSearched = -1
    depthBestNodes = defaultdict(list)
    depthValue = {}
    terminatingQueue = Queue()
    while queue.not_empty and depth < maxDepth and stopTime - time() > 0:
        node, alpha, beta = queue.get()
        if node.depth > depth:
            # An entire depth layer of the decision tree has been evaluated.
            # Can now clear depthMaxNodes and depthMinNodes for any depths less than current
            # and can increment depth
            keys = set(depthBestNodes.keys())
            for key in keys:
                if key < depth:
                    depthBestNodes.pop(key)
                maxDepthSearched = depth
                depth = node.depth

        value = FailSoftAlphaBeta(node, depth + 1, terminatingQueue, alpha, beta) if failSoft else FailHardAlphaBeta(
            node, depth + 1, terminatingQueue, alpha, beta)
        # Add to best nodes dict if necessary.
        if len(depthBestNodes[depth]) == 0:
            depthBestNodes[depth].append((value, node))
            depthValue[depth] = value

        elif (maximizing and depthBestNodes[depth][0][0] < value) or (not maximizing and depthBestNodes[depth][0][0] > value):
            depthBestNodes[depth].pop()
            depthBestNodes[depth].append((value, node))
            depthValue[depth] = value

        queue.task_done()
        if queue.empty() and terminatingQueue.not_empty:
            queue = terminatingQueue
            terminatingQueue = Queue()

    return np.unique([x[-1].superMove for x in depthBestNodes[maxDepthSearched]]), depthValue[maxDepthSearched]

def IDDFSParallel(board:chess.Board, drawBoards:set, failSoft: bool, allowedTime, maxDepth, evalFunc, numCores:int):
    """

    :param board: The starting board to do evaluations on
    :param drawBoards: A set of tuples (board string, turn) that have appeared twice already in the game.
    If a board in this set appears with the same persons turn, then there will be a draw by repetition.
    :param failSoft: If true, will do fail-soft alpha-beta pruning. If false,
    will do fail-hard alpha-beta pruning.
    :param allowedTime: The maximum amount of time to spend searching for the best move. If infinity,
    and depth is infinity, then will search forever.
    :param maxDepth: The depth of moves to search. If none or infinity and allowedTime is infinity, then
    will search forever.
    :param evalFunc: A function that takes a board as a parameter and returns a numerical score
    :param numCores: The number cpu of cores to use
    :return: A list of the best moves that can be made
    """

    # allowedTime = float('inf')
    # maxDepth = 5
    pool = Pool(numCores)

    root = ChessNode(board, None, None, 0, evalFunc(board), evalFunc)
    # asyncResults = [pool.apply_async(IDDFS, args=(child.board, set(), failSoft, allowedTime, maxDepth, evalFunc)) for child in root.children if child.move not in skipMoves]
    childAsyncRes = {child: pool.apply_async(IDDFS, args=(child.board, drawBoards, failSoft, allowedTime, maxDepth, evalFunc)) for child in root.children if (str(child.board), child.board.turn) not in drawBoards}
    pool.close()
    pool.join()
    moveScore = {}
    bestMoves = []
    bestScore = None
    for child in childAsyncRes:
        value = child.value
        subMoves, score = childAsyncRes[child].get()
        if board.turn:
            value = min(value, score)
        else:
            value = max(value, score)
        moveScore[child.move] = value
        if bestScore is None or (board.turn and value > bestScore) or (not board.turn and value < bestScore):
            bestScore = value
            bestMoves.clear()
            bestMoves.append(child.move)
        elif value == bestScore:
            bestMoves.append(child.move)
    return bestMoves, bestScore





    # for child in root.children:
    #     if child.move not in skipMoves:
    #
    #         queue.put((child, -float('inf'), float('inf')))
    # maximizing = board.turn
    #
    # stopTime = time() + allowedTime
    # depth = 1
    # maxDepthSearched = -1
    # depthBestNodes = defaultdict(list)
    # terminatingQueue = MPQueue()
    # nodes = []
    # asyncResults = []
    # pool = Pool(numCores)
    #
    #
    # while not queue.empty() and depth < maxDepth and stopTime - time() > 0:
    #
    #     while not queue.empty():
    #         node, alpha, beta = queue.get()
    #         if node.depth > depth:
    #             # An entire depth layer of the decision tree has been evaluated.
    #             # Can now clear depthMaxNodes and depthMinNodes for any depths less than current
    #             # and can increment depth
    #             keys = set(depthBestNodes.keys())
    #             for key in keys:
    #                 if key < depth:
    #                     depthBestNodes.pop(key)
    #                 maxDepthSearched = depth
    #                 depth = node.depth
    #         nodes.append(node)
    #         if failSoft:
    #             asyncResults.append(
    #                 pool.apply_async(FailSoftAlphaBeta, args=(node, depth + 1, terminatingQueue, alpha, beta)))
    #         else:
    #             asyncResults.append(
    #                 pool.apply_async(FailHardAlphaBeta, args=(node, depth + 1, terminatingQueue, alpha, beta)))
    #         queue.task_done()
    #
    #     for node, asyncValue in zip(nodes, asyncResults):
    #         # Note to self: Make a separate terminating queue for each process
    #         value = asyncValue.get()
    #         # Add to best nodes dict if necessary.
    #         if len(depthBestNodes[depth]) == 0:
    #             depthBestNodes[depth].append((value, node))
    #         elif (maximizing and depthBestNodes[depth][0][0] < value) or (
    #                 not maximizing and depthBestNodes[depth][0][0] > value):
    #             depthBestNodes[depth].pop()
    #             depthBestNodes[depth].append((value, node))
    #     nodes.clear()
    #     asyncResults.clear()
    #
    #     if queue.empty() and not terminatingQueue.empty():
    #         while not terminatingQueue.empty():
    #             queue.put(terminatingQueue.get())
    #             terminatingQueue.task_done()
    #         pool = Pool(numCores)
    #
    # return np.unique([x[-1].superMove for x in depthBestNodes[maxDepthSearched]])


def FailSoftAlphaBeta(node: ChessNode, stopDepth, terminatingNodes, alpha=-float('inf'), beta=float('inf')):
    """
    :param node: Chess Node Data
    :param stopDepth: Maximum depth to expand nodes to
    :param terminatingNodes: Queue to add terminating nodes too to continue searching deeper depths
    :param alpha:
    :param beta:
    :return: The score of this node
    """
    if node.isTerminating:
        # Node has been explored to the furthest necessary
        return node.value
    elif node.depth == stopDepth:
        # Terminating Condition
        terminatingNodes.put((node, alpha, beta))
        return node.value
    else:
        if node.board.turn == chess.WHITE:
            # Maximizing
            value = -float('inf')
            for child in node.children:
                newValue = FailSoftAlphaBeta(child, stopDepth, terminatingNodes, alpha, beta)
                value = max(value, newValue)
                # fail-soft: update before if-statement
                alpha = max(alpha, value)
                if value >= beta:
                    break
        else:
            # Minimizing
            value = float('inf')
            for child in node.children:
                newValue = FailSoftAlphaBeta(child, stopDepth, terminatingNodes, alpha, beta)
                value = min(value, newValue)
                # fail-soft: update before if-statement
                beta = min(beta, value)
                if value <= alpha:
                    break
        return value

def FailHardAlphaBeta(node: ChessNode, stopDepth, terminatingNodes, alpha=-float('inf'), beta=float('inf')):
    """
    :param node: Chess Node Data
    :param stopDepth: Maximum depth to expand nodes to
    :param terminatingNodes: Queue to add terminating nodes too to continue searching deeper depths
    :param alpha:
    :param beta:
    :return: The score of this node
    """
    if node.isTerminating:
        # Node has been explored to the furthest necessary
        return node.value
    elif node.depth == stopDepth:
        # Terminating Condition
        terminatingNodes.put((node, alpha, beta))
        return node.value
    else:
        if node.board.turn == chess.WHITE:
            # Maximizing
            value = -float('inf')
            for child in node.children:
                newValue = FailHardAlphaBeta(child, stopDepth, terminatingNodes, alpha, beta)
                value = max(value, newValue)
                # fail-soft: update before if-statement
                alpha = max(alpha, value)
                if value >= beta:
                    break
        else:
            # Minimizing
            value = float('inf')
            for child in node.children:
                newValue = FailHardAlphaBeta(child, stopDepth, terminatingNodes, alpha, beta)
                value = min(value, newValue)
                if value <= alpha:
                    break
                # fail-hard: update after if-statement
                beta = min(beta, value)
        return value
