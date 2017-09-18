from operator import itemgetter

class SearchState():
    def __init__(self):
    # the board
        return

class SearchNode():
    def __init__(self, parent):
        self.parent = parent
        self.successors = []
        self.g = 0
        self.h = self.heuristicEvaluation()
        self.f = self.g + self.h

    def heuristicEvaluation(self):
        # estimaed distance-to-goal from nodes state
        raise NotImplementedError

    def generateSuccesorNodes(self):
        raise NotImplementedError

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
        num_actions = 0
        while not self.isSolution(node):
            num_actions += 1
            if not self.open_node_ids:
                print ("Failure")
                return False
            node_id = self.open_node_ids.pop()
            node = self.nodes[node_id]
            self.closed_node_ids.append(node_id)

            if self.isSolution(node):
                self.printSolution(node)
            
            successors = node.generateSuccessorNodes()

            if successors:
                for successor in successors:
                    # State exists from before
                    if successor.id in self.nodes:
                        successor = self.nodes[successor.id]
                    # State is new
                    node.successors.append(successor)
                    if successor.id not in self.nodes:
                        self.attachAndEval(successor, node)
                        self.nodes[successor.id] = successor
                        self.open_node_ids.append(successor.id)
                        self.sortIds()

                    # Is the new parent better than the old one?
                    elif node.g + self.arcCost(successor, node) < successor.g:
                        print ("was greater")
                        self.attachAndEval(successor, node)
                        if self.closed_node_ids[successor.id]:
                            self.propagatePathImprovements(successor)

    def printSolution(self, node):
        print (node.state.board)
        actions = 0
        while node.parent is not None:
            actions += 1
            print (actions)
            print (node.parent.state.board)
            node = node.parent

    def sortIds(self):
        temp = {}
        for node_id in self.open_node_ids:
            temp[node_id] = self.nodes[node_id].f
        tempSorted = sorted(temp.items(), key=itemgetter(1))
        self.open_node_ids = [i[0] for i in tempSorted]

    def arcCost(self, successor, parent):
        raise NotImplementedError

    def attachAndEval(self, successor, parent):
            successor.parent = parent
            successor.g = parent.g + self.arcCost(successor, parent)
            # h is already computed in init function
            successor.f = successor.g + successor.h

    def propagatePathImprovements(self, parent):
        for successor in parent.successors:
            if parent.g + self.arcCost(successor, parent) < successor.g:
                successor.parent = parent
                successor.g = parent.g + self.arcCost(successor,parent)
                successor.f = successor.g + successor.h
                self.propagatePathImprovements(successor)
