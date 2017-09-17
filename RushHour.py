from AStar import BestFirstSearch, SearchState, SearchNode

class Car(object):
    def __init__(self, car_params):
        self.orientation = car_params[0]
        self.x = car_params[1]
        self.y = car_params[2]
        self.size = car_params[3]

    def toString(self):
        return ("{}{}{}{}".format(self.orientation, self.x, self.y, self.size))

class RushHourState(SearchState):
    def __init__(self, cars, board_size):
        self.cars = cars
        self.board = self.createStateBoardFromCars(board_size)
        self.id = self.createStateIdentifier()


    def createStateIdentifier(self):
        state_id = ''
        for car in self.cars:
            state_id = state_id + car.toString()
        return state_id

    def createStateBoardFromCars(self, board_size):
        board = [['*']*board_size for i in range(board_size)]
        for index, car in enumerate(self.cars):
            x = car.x
            y = car.y
            for i in range(car.size):
                board[y][x] = str(index)
                if car.orientation == 0:
                    x += 1
                elif car.orientation == 1:
                    y += 1
        return board

    def legalMoves(self, car_nr, car):
        legal_moves = []
        new_board = self.board
        if self.canMoveUp(car):
            #  make and add hashID to legal_moves
            new_board[car.y-1][car.x] = car_nr
            new_board[car.y+car.size-1][car.x] = '*'
            print ("up")
            legal_moves.append(self.createNodeIdentifier(new_board))
        if self.canMoveDown(car):
            #  make and add hashID to legal_moves
            new_board[car.y+1][car.x] = car_nr
            new_board[car.y][car.x] = '*'
            print ("down")
            legal_moves.append(self.createNodeIdentifier(new_board))
        if self.canMoveLeft(car):
            #   make and add hashID to legal_moves
            new_board[car.y][car.x-1] = car_nr
            new_board[car.y][car.x+car.size-1] = '*'
            print ("left")
            legal_moves.append(self.createNodeIdentifier(new_board))
        if self.canMoveRight(car):
            #  make and add hashID to legal_moves
            new_board[car.y][car.x+1] = car_nr
            new_board[car.y][car.x] = '*'
            print ("right")
            legal_moves.append(self.createNodeIdentifier(new_board))
        return legal_moves

    def isOutsideOfBoard(self, x, y, board_size):
        if x > board_size-1 or x < 0 \
        or y > board_size-1 or y < 0:
            return False
        else:
            return True


    def canMoveUp(self, car):
        if car.orientation == 0: return False
        if self.isOutsideOfBoard(car.x, car.y-1, self.board_size) \
        and self.board[car.y-1][car.x] == '*': return True

    def canMoveDown(self, car):
        if car.orientation == 0: return False
        if self.isOutsideOfBoard(car.x, car.y+car.size, self.board_size) \
        and self.board[car.y+car.size][car.x] == '*': return True

    def canMoveLeft(self, car):
        if car.orientation == 1: return False
        if self.isOutsideOfBoard(car.x-1, car.y, self.board_size) \
        and self.board[car.y][car.x-1] == '*': return True

    def canMoveRight(self, car):
        if car.orientation == 1: return False
        if self.isOutsideOfBoard(car.x+car.size, car.y, self.board_size) \
        and self.board[car.y][car.x+car.size] == '*': return True

    def getChildCarParams(self):
        child_states = []

        children = []
        for index, car in enumerate(self.state.cars):
            x = car.x
            y = car.y
            orientation = car.orientation
            size = car.size
            print (orientation, x, y, size)
            # legal_moves = self.legalMoves(str(index), orientation, x, y, size)
            legal_moves = self.legalMoves(str(index), car)
            if legal_moves:
                for move in legal_moves:
                    children.append(move)
        return children # or chil_states

class RushHourNode(SearchNode):
    # In general, a search-node class and its methods for handling
        # a) parent-child node connections, and
        # b) general search-graph creation and maintenance
    # should be sufficient for most A* applications.
    def __init__(self, state, board_size, goal_coords, parent=None):
        self.state = state
        self.id = state.id
        self.board_size = board_size
        self.goal_coords = goal_coords
        SearchNode.__init__(self, parent)

        # calculates g, h for problem specific rules

    # TODO: rydde/endre denne koden - gjøre den mer sexy

    def heuristicEvaluation(self):
        hero = self.state.cars[0]
        board = self.state.board
        distance_to_goal = goal_coords['x'] - (hero.x+hero.size-1)
        number_of_obstacles = 0
        for i in range(distance_to_goal-1):
            x = hero.x + i
            if board[hero.y][x] != '*':
                number_of_obstacles += 1
        return distance_to_goal + number_of_obstacles

    def generateSuccesorStates(self):
        # expands (parent) node
        # generate children to parent state

        nodes = []
        successor_states = self.state.getChildStates()

        for state in successor_states:
            nodes.append(RushHourNode(state))
        return nodes


class RushHourBfs(BestFirstSearch):
    def __init__(self, file, board_size, goal_coords):
        self.board_size = board_size
        self.goal_coords = goal_coords
        root_node = self.createRootNode(file)
        BestFirstSearch.__init__(self, root_node)

    def createRootNode(self, file):
        cars = []
        with open(file) as f:
            rows = f.readlines()
            rows = [row.replace('\n', '') for row in rows]
            for row in rows:
                cars.append(Car([int(x) for x in row.split(",")]))

        root_state = RushHourState(cars, board_size)
        return RushHourNode(root_state, board_size, goal_coords)

    def isSolution(self, node):
        return goal_coords['x'] - (hero.x+hero.size-1) == 0

    def arcCost(self, parent_node, child_node):
        # arc-cost between parent node and child node
        return 1

board_size = 6
goal_coords = {'x': 5, 'y': 2}
rh = RushHourBfs("boards/easy-3.txt", board_size, goal_coords)
# solution = BestFirstSearch(rh)


# car1 = [0,2,2,2]
# car2 = [0,0,4,3]
# car3 = [0,3,4,2]
# car4 = [0,4,1,2]
# car5 = [1,2,0,2]
# car6 = [1,4,2,2]

# cars = [car1,car2,car3,car4,car5,car6]

# state = RushHourState(cars, board_size)
# node = RushHourNode(state, board_size)
# print (node.id)
# print (node.state.board)










