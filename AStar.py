class SearchState():
    def __init__(self):
    # the board
        return

class SearchNode():
    def __init__(self, parent):
        self.parent = parent
        self.successors = []
        self.g = 0
        if parent is not None:
            self.g = self.parent.g + 1
        self.h = self.heuristicEvaluation()
        self.f = self.g + self.h

    def heuristicEvaluation(self):
        # estimaed distance-to-goal from nodes state
        raise NotImplementedError

    def calculateCost(self, node):
        node.f = node.g + node.h

    # In general, a search-node class and its methods for handling
        # a) parent-child node connections, and
        # b) general search-graph creation and maintenance
    # should be sufficient for most A* applications.

class BestFirstSearch():
    def __init__(self, root_node):
        self.nodes = {}
        self.closed_node_ids = []
        self.open_node_ids = []

        self.nodes[root_node.id]= root_node
        self.open_node_ids.append(root_node.id)

        node = root_node
        while not self.isSolution(node):
            node_id = self.open_node_ids.pop()
            node = self.nodes[node_id]
            self.closed_node_ids.push(node_id)
            self.succesors = self.generateSuccesorStates()

        # closed_node_ids.append(node.id)
        # open_node_ids.pop(0)
        # open_node_ids.append(node.children)

    def generateSuccesorStates(self):
        raise NotImplementedError

    def attachAndEval(self, C ,P):
        return

    def propagatePathImprovements(self, P):
        return

    def isGenerated(self, node_id):
        if node_id in nodes:
            return True
        return False