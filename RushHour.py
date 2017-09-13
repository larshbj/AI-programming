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
        self.children
        self.parent

        # calculates g, h for problem specific rules
        # Handles parent/children connection
    def getChildrenIds(self):
        return []

class RushHourBfs(BestFirstSearch):
    def __init__(self, car_params_list_file, goal_state):
        BestFirstSearch.__init__(self)
        self.goal_state = goal_state

        self.open_nodes = []
        self.closed_nodes = []

        self.car_params_list = []

        with open(car_params_list_file) as f:
            rows = f.readlines()
            rows = [row.replace('\n', '') for row in rows]
            for row in rows:
                self.car_params_list.append([int(x) for x in row.split(",")])

    def createRootNode(self):
        self.initial_state = RushHourNode(self.car_params_list)
        # creates initial search state

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
