from working import solve,find_empty,generate_board,whitespaces
import pygame
import time
pygame.font.init()
restart = False

class Grid:
    #Initial Board
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

    def __init__(self,rows,cols,width,height,win):
        self.rows = rows
        self.cols = cols
        self.width = width
        self.height = height
        #Create the board
        generate_board(self.board)
        whitespaces(self.board)
        #Cube is an inner class
        self.cubes = [[Cube(self.board[i][j],i,j,self.width,self.height) for j in range(cols)]for i in range(rows)]
        self.selected = None
        self.model = None
        self.update_model()
        self.win = win
        #Text is an inner class
        self.text = Text()

    def update_model(self):
        self.model = [[self.cubes[i][j].getValue() for j in range(self.cols)]for i in range(self.rows)]
        solve(self.model)

    def draw(self):
        gap = self.width/9
        for i in range(self.rows+1):
            if i%3==0:
                thick = 4
            else:
                thick = 1
            pygame.draw.line(self.win, (0,0,0), (0, i*gap), (self.width, i*gap), thick)
            pygame.draw.line(self.win,(0,0,0),(i*gap,0),(i*gap,self.height),thick)

        for i in range(self.rows):
            for j in range(self.cols):
                self.cubes[i][j].draw(self.win)

    def getCoordinates(self,pos):
        if pos[0]<self.width and pos[1]<self.height:
            gap = self.width/9
            x = pos[0]//gap
            y = pos[1]//gap
            return (int(y),int(x))
        else:
            return False
    
    def select(self,row,col):
        for i in range(self.rows):
            for j in range(self.cols):
                self.cubes[i][j].setSelected(False)
        self.cubes[row][col].setSelected(True)
        self.selected = (row,col)

    def sketch(self,key):
        if self.selected and key:
            row, col = self.selected
            self.cubes[row][col].setTemp(key)

    def clear(self):
        row, col = self.selected
        if self.cubes[row][col].value == 0:
            self.cubes[row][col].setTemp(0)


    def place(self,val):
        i,j = self.selected
        if self.cubes[i][j].getValue() == 0:
            self.cubes[i][j].setValue(val)

            if val == self.model[i][j]:
                return True
            else:
                self.cubes[i][j].setValue(0)
                self.cubes[i][j].setTemp(0)
                return False

    def solve_board(self):
        for i in range(self.rows):
            for j in range(self.cols):
                self.cubes[i][j].setValue(self.model[i][j])
                
    
class Cube:
    
    def __init__(self,value,row,col,width,height):
        self.value = value
        self.row = row
        self.col = col
        self.width = width
        self.height = height
        self.temp = 0
        self.selected = False

    def draw(self,win):
        fnt = pygame.font.SysFont("comicsans",40)

        gap = self.width/9
        x = self.col * gap
        y = self.row * gap

        if self.temp != 0 and self.value == 0:
            text = fnt.render(str(self.temp), 1, (128,128,128))
            win.blit(text, (x+5, y+5))
        
        elif not(self.value == 0):
            text = fnt.render(str(self.value),1,(0,0,0))
            win.blit(text,(x + (gap/2 - text.get_width()/2),y + (gap/2 - text.get_height()/2) ) )
        
        if self.selected:
            pygame.draw.rect(win,(255,0,0),(x,y,gap,gap),3)

    def setTemp(self,val):
        self.temp = val
    
    def getTemp(self):
        return self.temp

    def setValue(self,val):
        self.value = val

    def getValue(self):
        return self.value
    
    def setSelected(self,select):
        self.selected = select

class Text:

    def __init__(self):
        self.default()

    def default(self):
        self.str = "Press SPACE for solution"
        self.colour = (0,0,0)

    def Wrong(self):
        self.str = "Wrong"
        self.colour = (0,0,0)

    def Correct(self):
        self.str = "Correct"
        self.colour = (0,0,0)

    def Solved(self):
        self.str = "Solved"
        self.colour = (0,0,0)

def redraw(win,board,strikes,play_time):
    win.fill((255,255,255))
    fntInstr = pygame.font.SysFont("comicsans", 25)
    fnt = pygame.font.SysFont("comicsans", 40)
    #Draw Instructions
    text = fntInstr.render(board.text.str,1,board.text.colour)
    win.blit(text,(10,575))
    #Draw Strikes
    text = fnt.render("X " * strikes, 1, (255, 0, 0))
    win.blit(text, (10, 545))
    #Draw Time
    text = fnt.render("Time: " + formatTime(play_time), 1, (0,0,0))
    win.blit(text, (540 - 160, 560))
    board.draw()

def formatTime(val):
    secs = val%60
    min = val//60
    min = min%60
    hour = min//60
    seconds = ""
    minutes = "0"+str(min) if secs<10 else str(min)
    seconds = "0"+str(secs) if secs<10 else str(secs)
    if hour == 0:
        string = minutes+":"+seconds
    else:
        string = str(hour)+":"+minutes+":"+seconds
    return string

def main():
    win = pygame.display.set_mode((540,600))
    pygame.display.set_caption("Sudoku")
    board = Grid(9,9,540,540,win)
    strikes = 0
    start = time.time()
    key = None
    run = True
    while run:

        play_time = round(time.time() - start)
        
        for event in pygame.event.get():
            # Quit Game
            if event.type == pygame.QUIT:
                return False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    key = 1
                if event.key == pygame.K_2:
                    key = 2
                if event.key == pygame.K_3:
                    key = 3
                if event.key == pygame.K_4:
                    key = 4
                if event.key == pygame.K_5:
                    key = 5
                if event.key == pygame.K_6:
                    key = 6
                if event.key == pygame.K_7:
                    key = 7
                if event.key == pygame.K_8:
                    key = 8
                if event.key == pygame.K_9:
                    key = 9
                if event.key == pygame.K_KP1:
                    key = 1
                if event.key == pygame.K_KP2:
                    key = 2
                if event.key == pygame.K_KP3:
                    key = 3
                if event.key == pygame.K_KP4:
                    key = 4
                if event.key == pygame.K_KP5:
                    key = 5
                if event.key == pygame.K_KP6:
                    key = 6
                if event.key == pygame.K_KP7:
                    key = 7
                if event.key == pygame.K_KP8:
                    key = 8
                if event.key == pygame.K_KP9:
                    key = 9
                
                # Arrow Key controls 
                if event.key == pygame.K_UP:
                    if board.selected:
                        row,col = board.selected
                        if row > 0:
                            board.select(row-1,col)
                            key = 0

                if event.key == pygame.K_DOWN:
                    if board.selected:
                        row,col = board.selected
                        if row < 8:
                            board.select(row+1,col)
                            key = 0

                if event.key == pygame.K_LEFT:
                    if board.selected:
                        row,col = board.selected
                        if col > 0:
                            board.select(row,col-1)
                            key = 0

                if event.key == pygame.K_RIGHT:
                    if board.selected:
                        row,col = board.selected
                        if col < 8:
                            board.select(row,col+1)
                            key = 0

                # Delete Value
                if event.key == pygame.K_DELETE or event.key == pygame.K_BACKSPACE :
                    key = 0
                    board.clear()
                
                # Confirm Value
                if event.key == pygame.K_RETURN:
                    i,j = board.selected
                    if board.cubes[i][j].getTemp() != 0:
                        if board.place(board.cubes[i][j].getTemp()):
                            board.text.Correct()
                        else:
                            board.text.Wrong()
                            strikes += 1
                    key = None

                # Solve GUI Board
                if event.key == pygame.K_SPACE:
                    board.solve_board()            
                
                # Restart Game
                if event.key == pygame.K_r and event.mod & pygame.KMOD_CTRL:
                    print("Restart")
                    return True

                # Shortcut to Quit Game
                if event.key == pygame.K_q and event.mod & pygame.KMOD_CTRL:
                    return False
                
                board.sketch(key)     

            # Mouse Click
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                coordinates = board.getCoordinates(pos)
                if coordinates:
                    board.select(coordinates[0],coordinates[1])
                    board.text.default()

        # To check if the board is solved
        temp = [[board.cubes[i][j].getValue() for j in range(board.cols)] for i in range(board.rows)]
        if not find_empty(temp):
            board.text.Solved()
        redraw(win,board,strikes,play_time)
        pygame.display.update()

if main():
    main()
pygame.quit()