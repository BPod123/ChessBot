from abc import ABCMeta, abstractmethod
import numpy as np

class Node(object, ABCMeta):
    def __init__(self, data, depth, highestParentValue):
        self.data = data
        self.depth = None
        self.highestParentValue = highestParentValue
    @abstractmethod
    @property
    def value(self):
        pass

    @abstractmethod
    @property
    def children(self):
        pass

    def __le__(self, other):
        return self.value <= other

    def __lt__(self, other):
        return self.value < other

    def __gt__(self, other):
        return self.value > other

    def __ge__(self, other):
        return self.value >= other

    def __eq__(self, other):
        return self.value == other

    def __hash__(self):
        return self.data.__hash__()

    def __repr__(self):
        return str(self.data)



class Tree(object):
    def __init__(self, root: Node):
        self.root = root




