import sys
from random import choice, seed

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
    k, q, b, r, n = list(map(int, data[4][data[4].find(':')+1:].split()))
    
    return rows, cols, obstacles, k, q, b, r, n

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
            knight_deltas = {(2, 1), (1, 2), (-2, 1), (-1, 2), (2, -1), (1, -2), (-2, -1), (-1, -2)}
            return (x1 - x2, y1 - y2) in knight_deltas
    return threatens(k1, p1, p2) or threatens(k2, p2, p1)

def search(dim, obstacles, piece_counts):
    seed(3243)
    rows, cols = dim
    kqbrn = ['King', 'Queen', 'Bishop', 'Rook', 'Knight']
    seq = [5, 1, 3, 2, 4]

    vals = set((x, y) for x in range(rows) for y in range(cols)) - obstacles
    variables, priority = {}, {}
    for i in range(5):
        if piece_counts[i] != 0:
            variables[kqbrn[i]] = piece_counts[i]
            priority[kqbrn[i]] = seq[i]

    def h(var):
        return priority[var]

    def backtrack(variables, vals, assignment):
        if len(assignment) == sum(piece_counts):
            return dict(map(lambda pos: ((chr(pos[1] + 97), pos[0]), assignment[pos]), assignment.keys()))
        # Find the variable that will clear out the most expected number of squares
        var = min(variables, key=h)
        
        # For dense boards, either is fine, but for sparse, sorting it by position might help due to clustering
        for val in choice([vals, sorted(vals)]): # for each (r, c) position
            consistent = True
            for pos, piece in assignment.items():
                if check_conflict(var, piece, val, pos, obstacles):
                    consistent = False
                    break
            if consistent:
                assignment[val] = var
                vals.remove(val)

                # inference
                x, y = val
                new_illegal = set()
                if var == 'King':
                    king_deltas = {(1, 0), (0, 1), (-1, 0), (-1, 1), (1, -1), (1, 1), (-1, -1), (0, -1)}
                    for dx, dy in king_deltas:
                        if valid_range(rows, cols, x + dx, y + dy):
                            new_illegal.add((x + dx, y + dy))
                if var in ['Bishop', 'Queen']:
                    bishop_dirs = {(1, 1), (1, -1), (-1, -1), (-1, 1)}
                    for dx, dy in bishop_dirs:
                        posx, posy = x, y
                        while (posx, posy) not in obstacles and valid_range(rows, cols, posx, posy):
                            posx, posy = posx + dx, posy + dy
                            new_illegal.add((posx, posy))
                if var in ['Rook', 'Queen']:
                    rook_dirs = {(1, 0), (0, -1), (-1, 0), (0, 1)}
                    for dx, dy in rook_dirs:
                        posx, posy = x, y
                        while (posx, posy) not in obstacles and valid_range(rows, cols, posx, posy):
                            posx, posy = posx + dx, posy + dy
                            new_illegal.add((posx, posy))
                if var == 'Knight':
                    knight_deltas = {(2, 1), (1, 2), (-2, 1), (-1, 2), (2, -1), (1, -2), (-2, -1), (-1, -2)}
                    for dx, dy in knight_deltas:
                        if valid_range(rows, cols, x + dx, y + dy):
                            new_illegal.add((x + dx, y + dy))
                new_illegal &= vals # excludes obstacle positions too
                vals -= new_illegal

                variables[var] -= 1
                if variables[var] == 0:
                    del variables[var]

                result = backtrack(variables, vals, assignment)
                if result != {}:
                    return result

                # restore all the data structures
                del assignment[val]
                vals |= new_illegal
                vals.add(val)
                if var not in variables:
                    variables[var] = 1
                else:
                    variables[var] += 1
        return {}

    return backtrack(variables, vals, {})

### DO NOT EDIT/REMOVE THE FUNCTION HEADER BELOW###
# To return: Goal State which is a dictionary containing a mapping of the position of the grid to the chess piece type.
# Chess Pieces: King, Queen, Knight, Bishop, Rook (First letter capitalized)
# Positions: Tuple. (column (String format), row (Int)). Example: ('a', 0)

# Goal State to return example: {('a', 0) : Queen, ('d', 10) : Knight, ('g', 25) : Rook}
def run_CSP():
    # You can code in here but you cannot remove this function or change the return type
    testfile = sys.argv[1] #Do not remove. This is your input testfile.
    rows, cols, obstacles, k, q, b, r, n = parse(testfile)
    goalState = search((rows, cols), obstacles, (k, q, b, r, n))
    return goalState #Format to be returned
