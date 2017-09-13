from AStar import BestFirstSearch, SearchState, SearchNode

class Car(object):
    def __init__(self, car_params):
        self.orientation = car_params[0]
        self.horizontal_coord = car_params[1]
        self.vertical_coord = car_params[2]
        self.size = car_params[3]

class RushHourState(SearchState):
    def __init__(self, car_params_list):
        SearchState.__init__(self)
        self.hero = Car(car_params_list.pop(0))
        self.obstacles = []
        for car_params in car_params_list:
            self.obstacles.append(Car(car_params))

    def createStateIdentifier(self, car_params_list):
        # Creates state id from car parameters
        return ''.join(str(item) for row in car_params_list for item in row)

class RushHourNode(SearchNode):
    def __init__(self, car_params_list):
        SearchNode.__init__(self)
        self.state = RushHourState(car_params_list)
        self.id = self.state.createStateIdentifier(car_params_list)
        # self.children
        # self.parent

        # calculates g, h for problem specific rules
        # Handles parent/children connection
    def getChildrenIds(self):
        return []

class RushHourBfs(BestFirstSearch):
    def __init__(self, car_params_list_file, board_size, goal_state):
        BestFirstSearch.__init__(self)
        self.board_size = board_size
        self.goal_state = goal_state

        self.nodes = {}
        self.open_node_ids = []
        self.closed_node_ids = []

        self.car_params_list = []

        with open(car_params_list_file) as f:
            rows = f.readlines()
            rows = [row.replace('\n', '') for row in rows]
            for row in rows:
                self.car_params_list.append([int(x) for x in row.split(",")])

        self.createRootNode()
        print (self.nodes)
        print (self.open_node_ids)
        print (self.closed_node_ids)


    def createBoard(self, node):
        board = []
        board_row = ['*'] * self.board_size
        column = 0
        while (column < self.board_size):
            board.append(board_row)
            column += 1
        print (board)

    def createRootNode(self):

        root_node = RushHourNode(self.car_params_list)
        self.nodes[root_node.id] = root_node
        self.open_node_ids.append(root_node.id)

    def generateSuccesorStates(self, node):
        # expands (parent) node
        # generate children to parent state
        closed_node_ids.append(node.id)
        open_node_ids.append(node.getChildrenIds())


    def isSolution(self, node):
        # compares state of node to goal_state
        return

    def heuristicEvaluation(self, node):
        # estimaed distance-to-goal from nodes state
        return

    def arcCost(self, parent_node, child_node):
        # arc-cost between parent node and child node
        return

board_size = 6
goal_state = (5,2)
rh = RushHourBfs("boards/easy-3.txt", board_size, goal_state)
