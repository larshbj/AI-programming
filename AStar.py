from operator import itemgetter
import time 

class SearchState():
    def __init__(self):
    # the board
        return

class SearchNode():
    def __init__(self, parent):
        self.parent = parent
        self.successors = []
        self. g = 0
        if not parent is None:
            self.g = parent.g + self.arcCost(parent)
        self.h = self.heuristicEvaluation()
        self.f = self.g + self.h

    def heuristicEvaluation(self):
        # estimaed distance-to-goal from nodes state
        raise NotImplementedError

    def generateSuccesorNodes(self):
        raise NotImplementedError

    def arcCost(self, parent):
        raise NotImplementedError

    # In general, a search-node class and its methods for handling
        # a) parent-child node connections, and
        # b) general search-graph creation and maintenance
    # should be sufficient for most A* applications.

class BestFirstSearch():
    def __init__(self, search_method, root_node, display):
        self.nodes = {}
        self.closed_node_ids = []
        self.open_node_ids = []

        self.nodes[root_node.id] = root_node
        self.open_node_ids.append(root_node.id)

        node = root_node
        while not self.isSolution(node):
            if not self.open_node_ids:
                print ("Failure")
                return False
            node_id = self.open_node_ids.pop(0)
            node = self.nodes[node_id]
            if display:
                self.printBoard(node.state.board, "Showing popped nodes")
            self.closed_node_ids.append(node_id)

            if self.isSolution(node):
                ans = raw_input('Do you want to visualise the final solution? (y/n): ')
                if ans == "y":
                    self.printSolution(node)
                return
            
            successors = node.generateSuccessorNodes()

            if successors:
                successors = self.sortSuccessors(successors)
                for successor in successors:
                    # State exists from before
                    if successor.id in self.nodes:
                        successor = self.nodes[successor.id]
                    # State is new
                    node.successors.append(successor)
                    if successor.id not in self.nodes:
                        self.attachAndEval(successor, node)
                        self.nodes[successor.id] = successor
                        if search_method == 'breadth':
                            self.open_node_ids.append(successor.id)
                        elif search_method == 'depth':
                            self.open_node_ids.insert(0, successor.id)
                        elif search_method == 'astar':
                            self.open_node_ids.append(successor.id)
                            self.sortIds()
                        else:
                            print ("Search method not recognized")
                            return

                    # Is the new parent better than the old one?
                    elif node.g + successor.arcCost(node) < successor.g:
                        self.attachAndEval(successor, node)
                        if successor.id in self.closed_node_ids:
                            self.propagatePathImprovements(successor)

    def sortSuccessors(self, successors):
        successors.sort(key=lambda x: x.f, reverse=True)
        return successors

    def printSolution(self, node):
        boards = [node.state.board]
        while node.parent is not None:
            boards.append(node.parent.state.board)
            node = node.parent
        solution = reversed(boards)
        action_number = 0
        for board in solution:
            self.printBoard(board, "SOLUTION")
            action_number += 1
        print ('Number of actions: {}'.format(action_number))
        print ('Number of nodes generated: {}'.format(len(self.nodes)))

    def printBoard(self, board, message):
        print(chr(27) + "[2J")
        print (message)
        print ("-------------------------------")
        for row in board:
            print (row)
        time.sleep(0.5)

    def sortIds(self):
        temp = {}
        for node_id in self.open_node_ids:
            temp[node_id] = self.nodes[node_id].f
        tempSorted = sorted(temp.items(), key=itemgetter(1))
        self.open_node_ids = [i[0] for i in tempSorted]

    def attachAndEval(self, successor, parent):
            successor.parent = parent
            successor.g = parent.g + successor.arcCost(parent)
            # h is already computed in init function
            successor.f = successor.g + successor.h

    def propagatePathImprovements(self, parent):
        for successor in parent.successors:
            if parent.g + successor.arcCost(parent) < successor.g:
                successor.parent = parent
                successor.g = parent.g + successor.arcCost(parent)
                successor.f = successor.g + successor.h
                self.propagatePathImprovements(successor)
