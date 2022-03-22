from Tree import Tree, Node
from time import time
class ChessNode(Node):
    @property
    def children(self):
        res = []
        for move in self.data.legal_moves:
            cpy = self.data.copy(stack=False)
            cpy.push(move)
            child = ChessNode(cpy, self.depth + 1, max(self.highestParentValue, self.value))
            if child.value < self.highestParentValue:
                continue
            else:
                res.append(child)
        return res
    @property
    def value(self):
        res = 0
        for x in str(self.data):
            if x in 'P p'.split(" "):
                res += 1 * (1 if x.upper() == x else -1)
            elif x in 'N n B b'.split(" "):
                res += 3 * (1 if x.upper() == x else -1)
            elif x in 'r R'.split(" "):
                res += 5 * (1 if x.upper() == x else -1)
            elif x in 'q Q'.split(' '):
                res += 9 * (1 if x.upper() == x else -1)
            elif x in 'k K'.split(' '):
                res += 900 * (1 if x.upper() == x else -1)
            if self.depth % 2 != 0:
                res *= -1
        if res < self.highestParentValue:
            return -float('inf')
        return res

# class ChessDecisionTree(Tree):
#     def findBestMove(self, maxDepth):
#





