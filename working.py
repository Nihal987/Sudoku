import random
board = [
    [0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0]
]

def generate_board(bo):
    find = find_empty(bo)
    if not find:
        #If there are no empty cubes the board is done
        return True
    else:
        row,col = find
        val = random.randint(1,9)
        for i in range(1,10):
            if valid(bo,val,row,col):
                bo[row][col] = val
                #Recursivly check if the board is solvable with that new value
                # if not it'll return False and pop out of the stack
                if generate_board(bo):
                    return True
                bo[row][col] = 0
        return False

def whitespaces(bo):
    # Set level = 64 for highest possible difficulty
    level = 64
    while level>0:
        r = random.randint(0,8)
        c = random.randint(0,8)
        if bo[r][c] != 0:
            bo[r][c] = 0
            level -= 1

def solve(bo):
    find = find_empty(bo)
    if not find:
        return True
    else:
        row,col = find
        for i in range(1,10):
            if valid(bo,i,row,col):
                bo[row][col] = i

                if solve(bo):
                    return True
                bo[row][col] = 0
        return False


def valid(bo,value,r,c):
   
    #Check along the row
    for j in range(len(bo[r])):
        if bo[r][j] == value and j!=c:
            return False
    
    #Check along the column
    for i in range(len(bo)):
        if bo[i][c] == value and i!=r:
            return False
    
    #Check within the same quadrant
    box_r = (r//3)*3
    box_c = (c//3)*3
    for y in range(box_r,box_r+3):
        for x in range(box_c,box_c+3):
            if bo[y][x]==value and (y,x)!=(r,c):
                return False
    return True

def print_board(bo):
    #Function to print the board
    for i in range(len(bo)):
        if i%3==0 and i!= 0:
            print("- - - - - - - - - - - - -")
        for j in range(len(bo[0])):
            if j%3==0 and j!=0:
                print(" | ", end="")
            if j==len(bo[0])-1:
                print(bo[i][j])
            else:
                print(str(bo[i][j])+" ",end="")

def find_empty(bo):
    #Function to find empty cell
    for i in range(len(bo)):
        for j in range(len(bo[0])):
            if(bo[i][j]==0):
                return i,j
    return None
   

# generate_board(board)
# whitespaces(board)
# print_board(board)
# print(solve(board))