import random

matrix = [[0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0]]

# to find location of the first empty cell in the matrix
def find_empty(matrix):
    for i in range(9):
        for j in range(9):
            if matrix[i][j] == 0:
                return (i, j)
    return False

find_empty(matrix)

def check(n, r, c): # 1-9, 0-8, 0-8
    # row check matrix[r][c]
    for i in range(9):
        if n == matrix[r][i]:
            return False
    # column check
    for i in range(9):
        if n == matrix[i][c]:
            return False
    # cell check
    rs = (r // 3) * 3
    cs = (c // 3) * 3 # gives us submatrix location
    for i in range(rs, rs + 3): # 0 1 2 -> 0
        for j in range(cs, cs + 3): # 0 1 2 -> 0
            if n == matrix[i][j]: # 6 7 8 -> 2
                return False
    return True

# to prepare a random order of nos from 1-9
def listn():
    l = []
    while len(l) < 9:
        a = random.randint(1, 9)
        if a not in l:
            l.append(a)
    return l

def solve_sudoku():
    find = find_empty(matrix)
    if not find:
        return True
    else:
        # unpacking
        row, col = find
    # assigning values
    listnum = listn()
    for i in listnum:
        if check(i, row, col):
            matrix[row][col] = i
            if solve_sudoku():
                return True
            matrix[row][col] = 0
    return False

# method to ask diffiulty level
def asktype():
    print('choose difficulty level: \n a) NORMAL \n b) MEDIUM \n c) HARD ')
    a = input()
    return a

# method to empty cells using the difficulty level
def remove_nos(difftype):
    print(matrix)
    global x
    x = list(matrix)
    print(x)
    if difftype in ['a', 'A', 'NORMAL', 'normal']:
        rem = 0 # rem= number of removed cells


    emptycells = []
    while rem <= 40:
        r, c = random.randint(0, 8), random.randint(0, 8)
        if [r, c] not in emptycells:
            matrix[r][c] = 0
            rem += 1
            emptycells += [[r, c]]
        elif difftype in ['b', 'B', 'MEDIUM', 'medium']:
            rem = 0
            emptycells = []
            while rem <= 55:
                r, c = random.randint(0, 8), random.randint(0, 8)
                if [r, c] not in emptycells:
                    matrix[r][c] = 0
                    rem += 1
                    emptycells += [[r, c]]
        elif difftype in ['c', 'C', 'HARD', 'hard']:
            rem = 0
            emptycells = []
            while rem <= 65:
                r, c = random.randint(0, 8), random.randint(0, 8)
                if [r, c] not in emptycells:
                    matrix[r][c] = 0
                    rem += 1
                    emptycells += [[r, c]]

def print_sudoku():
    print('question:')
    print()
    for i in range(1, 10):
        for j in range(1, 10):
            if j % 3 == 0:
                print(matrix[i - 1][j - 1], end=' ')
            else:
                print(matrix[i - 1][j - 1], end=' ')
        if i % 3 == 0:
            print()
            print()
            print()
        else:
            print()