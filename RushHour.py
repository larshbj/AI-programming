from AStar import BestFirstSearch, SearchState, SearchNode

class Car(Object):
    def __init__(self, index, car_params):
        self.orientation = car_params[0]
        self.horizontal_coord = car_params[1]
        self.vertical_coord = car_params[2]
        self.size = car_params[3]
        self.is_hero = index === 0

class RushHourState(SearchState):
    def __init__(self, car_params_list):
        SearchState.__init__(self)
        self.id = createStateIdentifier(car_params_list)
        self.hero = Car(car_params_list.pop(0))
        self.obstacles = []
        for car_params in car_params_list:
            cars.append(Car(index, car_params))

    def createStateIdentifier(self, car_params_list):
        # Creates state id from car parameters
        return ''.join(str(item) for row in car_params_list for item in row)

class RushHourNode(SearchNode):
    def __init__(self, car_params_list):
        SearchNode.__init__(self)
        self.state = RushHourState(self.car_params_list)
        self.id = self.state.id
        self.board
        self.children
        self.parent


        # calculates g, h for problem specific rules
        # Handles parent/children connection
    def getChildrenIds(self):
        children = []
        for car in self.state.cars:
            x = car.horizontal_coord
            y = car.vertical_coord
            orientation = car.orientation
            size = car.size
            if canMove(orientation, x, y, size):
                # hashID = something
                # children.append(hashID)
        return children

    def canMove(self, orientation, x, y):


    def canMoveUp(self, orientation, x, y):
        if orientation is 0 return false
        # trenger logikk for out of bounds exception
        if self.board[x][y-1] == '*' return true

    def canMoveDown(self, orientation, x, y, size):
        if orientation is 0 return false
        # trenger logikk for out of bounds exception
        if self.board[x][y+size] == '*' return true

    def canMoveLeft(self, orientation, x, y):
        if orientation is 1 return false
        # trenger logikk for out of bounds exception
        if self.board[x-1][y] == '*' return true

    def canMoveRight(self, orientation, x, y, size):
        if orientation is 1 return false
        # trenger logikk for out of bounds exception
        if self.board[x+size][y] == '*' return true



class RushHourBfs(BestFirstSearch):
    def __init__(self, car_params_list_file, goal_state):
        BestFirstSearch.__init__(self)
        self.goal_state = goal_state

        self.nodes = {}
        self.open_nodes_id = []
        self.closed_nodes_id = []

        self.car_params_list = []

        with open(car_params_list_file) as f:
            rows = f.readlines()
            rows = [row.replace('\n', '') for row in rows]
            for row in rows:
                self.car_params_list.append([int(x) for x in row.split(",")])

    def createRootNode(self):
        root_node = RushHourNode(self.car_params_list)
        nodes[root_node.id] = root_node
        open_nodes.append(root_node.id)

    def generateSuccesorStates(self, node):
        # expands (parent) node
        # generate children to parent state
        closed_nodes.append(node.id)
        open_nodes.append(node.getChildrenIds())


    def isSolution(self, node):
        # compares state of node to goal_state

    def heuristicEvaluation(self, node):
        # estimaed distance-to-goal from nodes state

    def arcCost(self, parent_node, child_node):
        # arc-cost between parent node and child node

goal_state = (5,2)
rh = RushHourBfs("car_params_lists/easy-3.txt", goal_state)
