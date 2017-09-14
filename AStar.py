class BestFirstSearch():
    def __init__(self):
        # manages the overall operation of A*
        return

    def attachAndEval(self, C ,P):
        return

    def propagatePathImprovements(self, P):
        return

class SearchState():
    def __init__(self):
    # the board
        return

class SearchNode():
    def __init__(self):
        return
        # state
        # g
        # h
        # f
        # status
        # parent
        # kids

    def calculateCost(self, node):
        node.f = node.g + node.h

    # In general, a search-node class and its methods for handling
        # a) parent-child node connections, and
        # b) general search-graph creation and maintenance
    # should be sufficient for most A* applications.
