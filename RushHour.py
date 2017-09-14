from AStar import BestFirstSearch, SearchState, SearchNode

class Car(object):
    def __init__(self, car_params):
        self.orientation = car_params[0]
        self.horizontal_coord = car_params[1]
        self.vertical_coord = car_params[2]
        self.size = car_params[3]

class RushHourState(SearchState):
    def __init__(self, car_params_list, board_size):
        SearchState.__init__(self)
        self.board_size = board_size
        self.cars = []
        for car_params in car_params_list:
            self.cars.append(Car(car_params))
        self.board = self.createStateBoardFromCarParams()


    def createStateIdentifier(self, car_params_list):
        # Creates state id from car parameters
        return ''.join(str(item) for row in car_params_list for item in row)

    def createStateBoardFromCarParams(self):
        size = self.board_size
        board = [['*']*size for i in range(size)]
        for index, car in enumerate(self.cars):
            x = car.horizontal_coord
            y = car.vertical_coord
            for i in range(car.size):
                board[y][x] = str(index)
                if car.orientation == 0:
                    x += 1
                elif car.orientation == 1:
                    y += 1
        return board

class RushHourNode(SearchNode):
    def __init__(self, car_params_list, board_size):
        SearchNode.__init__(self)
        self.state = RushHourState(car_params_list, board_size)
        self.id = self.state.createStateIdentifier(car_params_list)
        # self.children
        # self.parent
        # self.board

        # calculates g, h for problem specific rules
        # Handles parent/children connection

    # TODO: rydde/endre denne koden
    def getChildrenIds(self):
        children = []
        for car in self.state.cars:
            x = car.horizontal_coord
            y = car.vertical_coord
            orientation = car.orientation
            size = car.size
            for move in legalMoves[orientation, x, y, size]:
                children.append(move)
        return children

    def legalMoves(self, orientation, x, y, size):
        legal_moves = []
        if canMoveUp(orientation, x, y):
            return
            #  make and add hashID to legal_moves
        if canMoveDown(orientation, x, y, size):
            return
            #  make and add hashID to legal_moves
        if canMoveLeft(orientation, x, y):
            return
            #   make and add hashID to legal_moves
        if canMoveRight(orientation, x, y):
            return
            #  make and add hashID to legal_moves
        return legal_moves

    def isOutsideOfBoard(x, y, board_size):
        if x > board_size or x < 0 \
        or y > board_size or y < 0:
            return false
        else:
            return true


    def canMoveUp(self, orientation, x, y):
        if orientation == 0: return false
        if not isOutsideOfBoard(x, y-1, self.board_size) \
        and self.board[x][y-1] == '*': return true

    def canMoveDown(self, orientation, x, y, size):
        if orientation == 0: return false
        if not isOutsideOfBoard(x, y+size, self.board_size) \
        and self.board[x][y+size] == '*': return true

    def canMoveLeft(self, orientation, x, y):
        if orientation == 1: return false
        if not isOutsideOfBoard(x-1, y, self.board_size) \
        and self.board[x-1][y] == '*': return true

    def canMoveRight(self, orientation, x, y, size):
        if orientation == 1: return false
        if not isOutsideOfBoard(x+size, y, self.board_size) \
        and self.board[x+size][y] == '*': return true



class RushHourBfs(BestFirstSearch):
    def __init__(self, car_params_list_file, board_size, goal_state):
        BestFirstSearch.__init__(self)
        self.board_size = board_size
        self.goal_state = goal_state

        self.nodes = {}
        self.open_node_ids = []
        self.closed_node_ids = []

        self.car_params_list = []

        # Read from file
        with open(car_params_list_file) as f:
            rows = f.readlines()
            rows = [row.replace('\n', '') for row in rows]
            for row in rows:
                self.car_params_list.append([int(x) for x in row.split(",")])

        self.createRootNode()

    def printStateBoard(self, node):
        print (node.state.board)

    def createRootNode(self):
        root_node = RushHourNode(self.car_params_list, board_size)
        self.nodes[root_node.id] = root_node
        self.open_node_ids.append(root_node.id)

    def generateSuccesorStates(self, node):
        # expands (parent) node
        # generate children to parent state

        # Kan flyttes til AStar ?
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
# node = rh.nodes[rh.open_node_ids.pop(0)]

