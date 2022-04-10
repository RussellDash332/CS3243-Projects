import sys
from collections import deque

def valid_range(r, c, i, j):
    return i in range(r) and j in range(c)

data = []
with open(sys.argv[1]) as f:
    for line in f:
        data.append(line.strip())

rows = int(data[0][data[0].find(':')+1:])
cols = int(data[1][data[1].find(':')+1:])
illegal = set(map(lambda x: (int(x[1:]), ord(x[0])-97), data[3][data[3].find(':')+1:].split()))
costs, enemy, own = {}, {}, {}

ptr = 5
while not data[ptr].startswith('Number'):
    pos, cost = data[ptr][1:-1].split(',')
    costs[(int(pos[1:]), ord(pos[0])-97)] = int(cost)
    ptr += 1
enemy_k, enemy_q, enemy_b, enemy_r, enemy_n = list(map(int, data[ptr][data[ptr].find(':')+1:].split()))
ptr += 2
ep = illegal.copy()
while not data[ptr].startswith('Number'):
    piece, pos = data[ptr][1:-1].split(',')
    r, c = int(pos[1:]), ord(pos[0])-97
    enemy[piece] = enemy.get(piece, []) + [(r, c)]
    ep.add((r, c))
    ptr += 1

for piece in enemy:
    for r, c in enemy[piece]:
        if piece in ['King', 'Queen']:
            # Add 8 neighbouring cells
            for i in range(-1, 2):
                for j in range(-1, 2):
                    if valid_range(rows, cols, r + i, c + j):
                        illegal.add((r + i, c + j))
        if piece in ['Bishop', 'Queen']:
            # Add same diagonal cells
            illegal.add((r, c))
            # Go down left
            dr = 1
            while valid_range(rows, cols, r + dr, c - dr) and (r + dr, c - dr) not in ep:
                illegal.add((r + dr, c - dr))
                dr += 1
            # Go down right
            dr = 1
            while valid_range(rows, cols, r + dr, c + dr) and (r + dr, c + dr) not in ep:
                illegal.add((r + dr, c + dr))
                dr += 1
            # Go up left
            dr = 1
            while valid_range(rows, cols, r - dr, c - dr) and (r - dr, c - dr) not in ep:
                illegal.add((r - dr, c - dr))
                dr += 1
            # Go up right
            dr = 1
            while valid_range(rows, cols, r - dr, c + dr) and (r - dr, c + dr) not in ep:
                illegal.add((r - dr, c + dr))
                dr += 1
        if piece in ['Rook', 'Queen']:
            # Add same row and column cells
            illegal.add((r, c))
            # Down
            dr = 1
            while valid_range(rows, cols, r + dr, c) and (r + dr, c) not in ep:
                illegal.add((r + dr, c))
                dr += 1
            # Up
            dr = 1
            while valid_range(rows, cols, r - dr, c) and (r - dr, c) not in ep:
                illegal.add((r - dr, c))
                dr += 1
            # Right
            dc = 1
            while valid_range(rows, cols, r, c + dc) and (r, c + dc) not in ep:
                illegal.add((r, c + dc))
                dc += 1
            # Left
            dc = 1
            while valid_range(rows, cols, r, c - dc) and (r, c - dc) not in ep:
                illegal.add((r, c - dc))
                dc += 1
        if piece == 'Knight':
            for i in [-2, -1, 0, 1, 2]:
                for j in [-2, -1, 0, 1, 2]:
                    if abs(i) + abs(j) in [0, 3] and valid_range(rows, cols, r + i, c + j):
                        illegal.add((r + i, c + j))

own_k, own_q, own_b, own_r, own_n = list(map(int, data[ptr][data[ptr].find(':')+1:].split()))
ptr += 2
while not data[ptr].startswith('Goal'):
    piece, pos = data[ptr][1:-1].split(',')
    own[piece] = own.get(piece, []) + [(int(pos[1:]), ord(pos[0])-97)]
    ptr += 1
goals = set(map(lambda x: (int(x[1:]), ord(x[0])-97), data[ptr][data[ptr].find(':')+1:].split()))

class State:
    def __init__(self, position, history):
        self.position = position
        self.history = history

    def is_goal_state(self):
        return self.position in goals

def search():
    moves, nodesExplored = [], 0
    initial_state = State(own['King'][0], [])
    reached = set()
    
    frontier = deque()
    frontier.append(initial_state)

    while len(frontier) != 0:
        state = frontier.popleft()
        nodesExplored += 1
        if state.is_goal_state():
            moves = state.history + [state.position]
            break
        else:
            r, c = state.position
            for i in range(-1, 2):
                for j in range(-1, 2):
                    if abs(i) + abs(j) != 0:
                        if valid_range(rows, cols, r + i, c + j):
                            if (r + i, c + j) not in illegal | reached:
                                reached.add((r + i, c + j))
                                frontier.append(State((r + i, c + j), state.history + [state.position]))

    finalMoves = []
    for i in range(len(moves) - 1):
        ra, ca = moves[i]
        rb, cb = moves[i + 1]
        finalMoves.append([(chr(ca + 97), ra), (chr(cb + 97), rb)])
    return finalMoves, nodesExplored

### DO NOT EDIT/REMOVE THE FUNCTION HEADER BELOW###
# To return: List of moves and nodes explored
def run_BFS():
    # You can code in here but you cannot remove this function or change the return type
        
    moves, nodesExplored = search() #For reference
    return moves, nodesExplored #Format to be returned
