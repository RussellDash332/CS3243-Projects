import sys
from random import choice, seed
from copy import deepcopy

### IMPORTANT: Remove any print() functions or rename any print functions/variables/string when submitting on CodePost
### The autograder will not run if it detects any print function.

# Helper functions to aid in your implementation. Can edit/remove
def valid_range(r, c, i, j):
    return i in range(r) and j in range(c)

def parse(filename):
    data = []
    with open(filename) as f:
        for line in f:
            data.append(line.strip())

    rows = int(data[0][data[0].find(':')+1:])
    cols = int(data[1][data[1].find(':')+1:])
    try:
        obstacles = set(map(lambda x: (int(x[1:]), ord(x[0])-97), data[3][data[3].find(':')+1:].split()))
    except:
        obstacles = set()
    K = int(data[4][data[4].find(':')+1:])
    k, q, b, r, n = list(map(int, data[5][data[5].find(':')+1:].split()))

    pieces = {}
    for pp in data[7:]:
        piece, pos = pp[1:-1].split(',')
        row, col = int(pos[1:]), ord(pos[0])-97
        pieces[piece] = pieces.get(piece, []) + [(row, col)]
    
    return rows, cols, obstacles, k, q, b, r, n, pieces, K

class Graph:
    def __init__(self):
        self.adj_list = {}
        self.num_edges = 0

    # Connect one at a time
    def connect(self, u, v):
        if u in self.adj_list:
            if v not in self.adj_list[u]:
                self.num_edges += 1
            self.adj_list[u].add(v)
        else:
            self.adj_list[u] = {v}
            self.num_edges += 1

    # Remove two at a time
    def remove(self, u):
        if u in self.adj_list:
            for v in self.adj_list[u]:
                self.adj_list[v].remove(u)
                self.num_edges -= 2
            del self.adj_list[u]

    def num_conflicts(self, u):
        return len(self.adj_list[u])

    def num_conflicts_all(self):
        return self.num_edges // 2

    def clone(self):
        new = Graph()
        new.num_edges = self.num_edges
        new.adj_list = deepcopy(self.adj_list)
        return new

class State:
    def __init__(self, graph):
        self.graph = graph

    def value(self):
        return -self.graph.num_conflicts_all()

    def clone(self):
        return State(self.graph.clone())

def check_conflict(k1, k2, p1, p2, obstacles):
    # Assumption: p1 != p2 and both p1 and p2 are valid positions
    def threatens(k1, p1, p2):
        x1, y1, x2, y2 = *p1, *p2
        if k1 == 'King':
            # Obstacles don't matter
            return abs(x1 - x2) <= 1 and abs(y1 - y2) <= 1
        elif k1 == 'Bishop':
            if (x1 + y1) == (x2 + y2) or (x1 - y1) == (x2 - y2):
                if (x1 + y1) == (x2 + y2): # negative slope
                    for x in range(min(x1, x2) + 1, max(x1, x2)):
                        if (x, x1 + y1 - x) in obstacles:
                            return False
                    return True
                else: # positive slope
                    for x in range(min(x1, x2) + 1, max(x1, x2)):
                        if (x, x - x1 + y1) in obstacles:
                            return False
                    return True
            return False
        elif k1 == 'Rook':
            if x1 == x2 or y1 == y2:
                if x1 == x2:
                    for y in range(min(y1, y2) + 1, max(y1, y2)):
                        if (x1, y) in obstacles:
                            return False
                    return True
                else: # y1 == y2
                    for x in range(min(x1, x2) + 1, max(x1, x2)):
                        if (x, y1) in obstacles:
                            return False
                    return True
            return False
        elif k1 == 'Queen':
            # Bishop-ish part
            if (x1 + y1) == (x2 + y2) or (x1 - y1) == (x2 - y2):
                if (x1 + y1) == (x2 + y2): # negative slope
                    for x in range(min(x1, x2) + 1, max(x1, x2)):
                        if (x, x1 + y1 - x) in obstacles:
                            return False
                    return True
                else: # positive slope
                    for x in range(min(x1, x2) + 1, max(x1, x2)):
                        if (x, x - x1 + y1) in obstacles:
                            return False
                    return True
            # Rook-ish part
            if x1 == x2 or y1 == y2:
                if x1 == x2:
                    for y in range(min(y1, y2) + 1, max(y1, y2)):
                        if (x1, y) in obstacles:
                            return False
                    return True
                else: # y1 == y2
                    for x in range(min(x1, x2) + 1, max(x1, x2)):
                        if (x, y1) in obstacles:
                            return False
                    return True
            return False
        else: # k1 == 'Knight'
            # Obstacles don't matter because can leap over
            knight_deltas = [(2, 1), (1, 2), (-2, 1), (-1, 2), (2, -1), (1, -2), (-2, -1), (-1, -2)]
            return (x1 - x2, y1 - y2) in knight_deltas
    return threatens(k1, p1, p2) or threatens(k2, p2, p1)

def search(dim, obstacles, pieces, piece_counts, threshold):
    seed(3243)
    rows, cols = dim
    k, q, b, r, n = piece_counts

    initial_graph = Graph()
    for k1 in pieces:
        for k2 in pieces:
            for p1 in pieces[k1]:
                for p2 in pieces[k2]:
                    if p1 != p2 and check_conflict(k1, k2, p1, p2, obstacles):
                        initial_graph.connect(p1, p2)

    # Process pieces dictionary
    pieces2 = {}
    for p in pieces:
        for pos in pieces[p]:
            pieces2[pos] = p

    initial_state = State(initial_graph)
    it = 0
    # Repeat for it iterations
    while it <= max(rows, cols):
        # Fixed restart from initial state
        current = initial_state
        while len(current.graph.adj_list) >= threshold:
            # Generate all successors
            neighbours = []
            pieces_to_check = sorted(current.graph.adj_list.keys(), key=lambda x: len(current.graph.adj_list[x]), reverse=True)
            # Keep checking the top max(rows, cols) successors
            for piece in pieces_to_check[:max(rows, cols)]:
                new_graph = current.graph.clone()
                new_graph.remove(piece)
                neighbours.append(State(new_graph))
            max_val = max(neighbours, key=lambda state: state.value()).value()
            # Pick randomly among the best
            neighbour = choice(list(filter(lambda state: state.value() == max_val, neighbours)))
            if max_val <= current.value():
                return dict(map(lambda pos: ((chr(pos[1] + 97), pos[0]), pieces2[pos]), current.graph.adj_list.keys()))
            current = neighbour
        it += 1
    return {} # probably unused but good to have

### DO NOT EDIT/REMOVE THE FUNCTION HEADER BELOW###
# To return: Goal State which is a dictionary containing a mapping of the position of the grid to the chess piece type.
# Chess Pieces: King, Queen, Knight, Bishop, Rook (First letter capitalized)
# Positions: Tuple. (column (String format), row (Int)). Example: ('a', 0)

# Goal State to return example: {('a', 0) : Queen, ('d', 10) : Knight, ('g', 25) : Rook}
def run_local():
    # You can code in here but you cannot remove this function or change the return type
    testfile = sys.argv[1] #Do not remove. This is your input testfile.
    rows, cols, obstacles, k, q, b, r, n, pieces, K = parse(testfile)
    goalState = search((rows, cols), obstacles, pieces, (k, q, b, r, n), K)
    return goalState #Format to be returned