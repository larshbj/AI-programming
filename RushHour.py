from AStar import BestFirstSearch, SearchState, SearchNode
from copy import deepcopy

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
        self.board_size = board_size
        self.board = self.createStateBoardFromCars(board_size)
        self.createStateIdentifier()

    def createStateIdentifier(self):
        state_id = ''
        for car in self.cars:
            state_id = state_id + car.toString()
        self.id = state_id

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

    def isOutsideOfBoard(self, x, y, board_size):
        if x > board_size-1 or x < 0 \
        or y > board_size-1 or y < 0:
            return True
        else:
            return False

    def canMoveUp(self, car):
        if car.orientation == 0: return False
        if not self.isOutsideOfBoard(car.x, car.y-1, self.board_size) \
        and self.board[car.y-1][car.x] == '*': return True

    def canMoveDown(self, car):
        if car.orientation == 0: return False
        if not self.isOutsideOfBoard(car.x, car.y+car.size, self.board_size) \
        and self.board[car.y+car.size][car.x] == '*': return True

    def canMoveLeft(self, car):
        if car.orientation == 1: return False
        if not self.isOutsideOfBoard(car.x-1, car.y, self.board_size) \
        and self.board[car.y][car.x-1] == '*': return True

    def canMoveRight(self, car):
        if car.orientation == 1: return False
        if not self.isOutsideOfBoard(car.x+car.size, car.y, self.board_size) \
        and self.board[car.y][car.x+car.size] == '*': return True

    def generateSuccesorStates(self):
        successor_states = []
        for index, car in enumerate(self.cars):
            if self.canMoveUp(car):
                new_cars = deepcopy(self.cars)
                new_cars[index].y -= 1
                new_state = RushHourState(new_cars, board_size)
                successor_states.append(new_state)
            if self.canMoveDown(car):
                new_cars = deepcopy(self.cars)
                new_cars[index].y += 1
                new_state = RushHourState(new_cars, board_size)
                successor_states.append(new_state)
            if self.canMoveLeft(car):
                new_cars = deepcopy(self.cars)
                new_cars[index].x -= 1
                new_state = RushHourState(new_cars, board_size)
                successor_states.append(new_state)
            if self.canMoveRight(car):
                new_cars = deepcopy(self.cars)
                new_cars[index].x += 1
                new_state = RushHourState(new_cars, board_size)
                successor_states.append(new_state)

        return successor_states # or chil_states

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

    def heuristicEvaluation(self):
        # return self.basicHeuristicEvaluation()
        return self.advancedHeuristicEvaluation()

    def basicHeuristicEvaluation(self):
        hero = self.state.cars[0]
        board = self.state.board
        distance_to_goal = self.goal_coords['x'] - (hero.x+hero.size-1)
        number_of_obstacles = 0

        for i in range(distance_to_goal-1):
            x = hero.x + i
            if board[hero.y][x] != '*':
                number_of_obstacles += 1

        return distance_to_goal - (hero.size-1) + number_of_obstacles

    def advancedHeuristicEvaluation(self):
        hero = self.state.cars[0]
        board = self.state.board
        distance_to_goal = self.goal_coords['x'] - (hero.x+hero.size-1)
        number_of_obstacles = self.findNumberOfObstacles(hero, distance_to_goal, '+')
        if number_of_obstacles == -1:
            print ("Obstacles can not move out of the way!")
            return 100000
        return distance_to_goal + number_of_obstacles

    def findNumberOfObstacles(self, car, distance_to_move, direction):
        number_of_obstacles = 0
        for i in range(1, distance_to_move):
            if car.orientation == 0:
                car_x = car.x
                if (direction == '+'):
                    car_x += car.size - 1 # Must add size of car when moving in positive direction
                x = eval('{} {} {}'.format(car_x, direction, i)) # example: car.x + i
                y = car.y
            else: # i.e car.orientation == 1
                car_y = car.y
                if (direction == '+'):
                    car_y += car.size - 1
                x = car.x
                y = eval('{} {} {}'.format(car_y, direction, i))
            cell_symbol = self.state.board[y][x]
            if cell_symbol != '*':
                obstacle_index = int(cell_symbol)
                if obstacle_index == 0:
                    print ("Obstacles meet hero in loop")
                    return 100000
                obstacle = self.state.cars[obstacle_index]
                direction = self.chooseDirection(x,y,obstacle)

                if direction is None:
                    print ("Leaf obstacle can't move")
                    return -1 # One obstacle in end of recursion, which can not move.
                distance_to_move = self.calcDistanceToMove(x,y,obstacle,direction)
                next_obstacles = self.findNumberOfObstacles(obstacle, distance_to_move, 
                    direction)

                if next_obstacles == -1:
                    direction = self.flipDirection(direction)
                    distance_to_move = self.calcDistanceToMove(x,y,obstacle,direction)
                    next_obstacles = self.findNumberOfObstacles(obstacle, distance_to_move, 
                    direction)
                number_of_obstacles += 1 + next_obstacles
        return number_of_obstacles + distance_to_move

    def flipDirection(direction):
        if direction == '-':
            return '+'
        else:
            return '-'

    def chooseDirection(self, x, y, car):
        if car.orientation == 1:
            distance_up = self.calcDistanceToMove(x,y,car,'-')
            y_up = car.y-distance_up

            distance_down = self.calcDistanceToMove(x,y,car,'+')
            y_down = car.y + car.size-1 + distance_down

            if self.state.isOutsideOfBoard(x, y_up, self.board_size):
                distance_up = -1
            elif self.state.isOutsideOfBoard(x, y_down, self.board_size):
                distance_down = -1


            if distance_up == -1 and distance_down == -1:
                return None
            elif distance_up == -1:
                return '+'
            elif distance_down == -1:
                return '-'
            else:
                return '-' if (distance_up < distance_down) else '+'
        else: #is 0
            distance_left = self.calcDistanceToMove(x,y,car,'-')
            x_left = car.x-distance_left

            distance_right = self.calcDistanceToMove(x,y,car,'+')
            x_right = car.x + car.size-1 + distance_right

            if self.state.isOutsideOfBoard(x_left, y, self.board_size):
                distance_left = -1
            elif self.state.isOutsideOfBoard(x_right, y, self.board_size):
                distance_right = -1

            if distance_left == -1 and distance_right == -1:
                return None
            elif distance_left == -1:
                return '+'
            elif distance_right == -1:
                return '-'
            else:
                return '-' if (distance_left < distance_right) else '+'

    def calcDistanceToMove(self, x, y, car, direction):
        if direction == '+':
            car_length_in_direction = x - car.x + y - car.y
        else : # i.e. direction == '-'
            if car.orientation == 0:
                car_length_in_direction = car.x + (car.size-1) - x
            else: # i.e orientation == 1
                car_length_in_direction = car.y + (car.size-1) - y
        return car_length_in_direction + 1 # Add one for car cell currently blocking

    def generateSuccessorNodes(self):
        # expands (parent) node
        # generate successor_states to parent state

        nodes = []
        successor_states = self.state.generateSuccesorStates()

        if successor_states is not None:
            for state in successor_states:
                nodes.append(RushHourNode(state, self.board_size, self.goal_coords, self))
        return nodes

    def arcCost(self, parent):
        # arc-cost between parent node and and self (child node of parent)
        return 1


class RushHourBfs(BestFirstSearch):
    def __init__(self, method, file, board_size, goal_coords, display):
        self.board_size = board_size
        self.goal_coords = goal_coords
        root_node = self.createRootNode(file)
        BestFirstSearch.__init__(self, method, root_node, display)

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
        hero = node.state.cars[0]
        return goal_coords['x'] - (hero.x+hero.size-1) == 0

def runAllBoardsAndMethods(boards, method, goal_coords, board_size):
    for board in boards:
        print ('--------------------------')
        print (boards[board])
        for method in method:
            print (method[method])
            RushHourBfs(method[method], boards[board], 
                board_size, goal_coords)

if __name__ == "__main__":
    boards = {
        'easy': 'boards/easy-3.txt',
        'medium': 'boards/medium-1.txt',
        'hard': 'boards/hard-3.txt',
        'expert': 'boards/expert-2.txt'
    }
    board_size = 6
    goal_coords = {'x': 5, 'y': 2}
    search_methods = {1:'breadth', 2:'depth', 3:'astar'}

    # runAllBoardsAndMethods(boards, search_methods, goal_coords, board_size)
    RushHourBfs(
       method      = 'astar', 
       file        = boards['easy'], 
       board_size  = 6, 
       goal_coords = {'x': 5, 'y': 2},
       display     = False
    )