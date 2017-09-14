open_states = {}
board = []

with open("boards/easy-3.txt") as f:
    rows = f.readlines()
    rows = [row.replace('\n', '') for row in rows]
    for row in rows:
        board.append([int(x) for x in row.split(",")])

def openState (board):
	state_key = ''.join(str(item) for row in board for item in row)
	open_states[state_key] = board
	print(open_states)

openState(board)
