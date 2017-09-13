# Generic classes
class BestFirstSearch():
    def __init__(self):
    # manages the overall operation of A*

class SearchState():
    def __init__(self):
    # the board

class SearchNode():
    def __init__(self, state):
        state
        g
        h
        f
        status
        parent
        kids

    def calculateCost(self, g, h):
        f = g + h

# ---------------------------------------------


# Rush-hour specific classes
class Car(Object):
    def __init__(self, car_parameters, is_hero):
        self.orientation = car_parameters[0]
        self.horizontal_coord = car_parameters[1]
        self.vertical_coord = car_parameters[2]
        self.size = car_parameters[3]
        self.is_hero = is_hero

class RushHourState(SearchState):
    def __init__(self, board):
        SearchState.__init__(self)
        self.board = board

    def createStateIdentifier(self):
        # generate hashID

class RushHourBfs(BestFirstSearch):
    def __init__(self, goal_state):
        BestFirstSearch.__init__(self)
        self.goal_state = goal_state

        open_states = {}
        board = []

        with open(board_file) as f:
            rows = f.readlines()
            rows = [row.replace('\n', '') for row in rows]
            for row in rows:
                board.append([int(x) for x in row.split(",")])
        print (board)

    def createRootNode(self):
        # creates initial search state

    def generateSuccesorStates(self, node):
        # expands (parent) node
        # generate children to parent state

    def isSolution(self, node):
        # compares state of node to goal_state

    def heuristicEvaluation(self, node):
        # estimaed distance-to-goal from nodes state

    def arcCost(self, parent_node, child_node):
        # arc-cost between parent node and child node

class RushHourNode(SearchNode):
    def __init__(self):
        SearchNode.__init__(self)


rh = RushHourBfs(board)
