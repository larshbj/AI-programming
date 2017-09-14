from AStar import BestFirstSearch, SearchState, SearchNode

class Car(object):
    def __init__(self, car_params):
        self.orientation = car_params[0]
        self.x = car_params[1]
        self.y = car_params[2]
        self.size = car_params[3]

class RushHourState(SearchState):
    def __init__(self, car_params_list, board_size):
        SearchState.__init__(self)
        self.board_size = board_size
        self.cars = []
        for car_params in car_params_list:
            self.cars.append(Car(car_params))
        self.board = self.createStateBoardFromCarParams()


    def createStateIdentifier(self, board):
        # Creates state id from car parameters
        # return ''.join(str(item) for row in car_params_list for item in row)
        return ''.join(str(item) for row in board for item in row)

    def createStateBoardFromCarParams(self):
        size = self.board_size
        board = [['*']*size for i in range(size)]
        for index, car in enumerate(self.cars):
            x = car.x
            y = car.y
            for i in range(car.size):
                board[y][x] = str(index)
                if car.orientation == 0:
                    x += 1
                elif car.orientation == 1:
                    y += 1
        print (board)
        return board

class RushHourNode(SearchNode):
    def __init__(self, car_params_list, board_size, parent):
        SearchNode.__init__(self)
        self.state = RushHourState(car_params_list, board_size)
        self.board_size = board_size
        self.board = self.state.board
        self.id = self.state.createStateIdentifier(self.board)
        self.children = self.getChildrenIds()
        print (self.children)
        self.parent = parent
        self.g = self.parent.g + 1 if parent else 0
        print (self.g)


        # calculates g, h for problem specific rules
        # Handles parent/children connection

    # TODO: rydde/endre denne koden - gjøre den mer sexy
    def getChildrenIds(self):
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
        return children

    def createNodeIdentifier(self, board):
        return ''.join(str(item) for row in board for item in row)


    # def legalMoves(self, car_nr, orientation, x, y, size):
    #     legal_moves = []
    #     if self.canMoveUp(orientation, x, y):
    #         legal_moves.append(self.createNodeIdentifier(car_nr, x, y-1, x, y+size-1))
    #         print ("up")
    #         return
    #         #  make and add hashID to legal_moves
    #     if self.canMoveDown(orientation, x, y, size):
    #         legal_moves.append(self.createNodeIdentifier(car_nr, x, y+1, x, y))
    #         print ("down")
    #         return
    #         #  make and add hashID to legal_moves
    #     if self.canMoveLeft(orientation, x, y):
    #         legal_moves.append(self.createNodeIdentifier(car_nr, x-1, y, x+size-1, y))
    #         print ("left")
    #         return
    #         #   make and add hashID to legal_moves
    #     if self.canMoveRight(orientation, x, y, size):
    #         legal_moves.append(self.createNodeIdentifier(car_nr, x-1, y, x+1, y))
    #         print ("right")
    #         return
    #         #  make and add hashID to legal_moves
    #     return legal_moves
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

        node = self.createRootNode()
        # while True:
        #     if not self.open_node_ids:
        #         print("fail")
        #         break;
        #     successors = self.generateSuccesorStates(node)
        #     for s in successors:
        #         if isGenerated(s):





    def printStateBoard(self, node):
        print (node.state.board)

    def createRootNode(self):
        root_node = RushHourNode(self.car_params_list, self.board_size, None)
        self.nodes[root_node.id] = root_node
        self.open_node_ids.append(root_node.id)
        return root_node

    def generateSuccesorStates(self, node):
        # expands (parent) node
        # generate children to parent state

        # Kan flyttes til AStar ?
        closed_node_ids.append(node.id)
        open_node_ids.pop(0)
        open_node_ids.append(node.children)

    def isGenerated(self, node):
        if node in open_node_ids \
        or node in closed_node_ids:
            return True
        return False

    def isSolution(self, node):
        # compares state of node to goal_state
        return

    def heuristicEvaluation(self, node):
        # estimaed distance-to-goal from nodes state
        return

    def arcCost(self, parent_node, child_node):
        # arc-cost between parent node and child node
        return 1

board_size = 6
goal_state = (5,2)
rh = RushHourBfs("boards/easy-3.txt", board_size, goal_state)
# node = rh.nodes[rh.open_node_ids.pop(0)]
