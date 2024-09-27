import sys
import pygame
import random


BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)

BLUE  = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
CYAN = (0, 255, 255)

class Board:
    StartX = 100
    StartY = 100
    colors = [BLUE, GREEN, RED, CYAN]
    def __init__(self):
        # element = [ exist, color, marking]        
        self.element = []
        for i in range(10):
            line = []
            for j in range(20):
                line.append([1, random.randrange(4), 0])
            self.element.append(line)
    
    def draw(self, screen):
        for i in range(10):
            for j in range(20):
                if self.element[i][j][0] != 0:
                    if self.element[i][j][2]:
                        color = YELLOW
                    else:
                        color = Board.colors[self.element[i][j][1]]
                        
                    rect = pygame.Rect(Board.StartX + 40*j, Board.StartY + 40*i, 40, 40)
                    pygame.draw.rect(screen, color, rect )
                
    def neighbor(self, elim):
        list = []
        if not elim:
            return list
        
        #left
        if elim[1] - 1 >= 0 and \
                self.element[elim[0]][elim[1] -1][0] and \
                self.element[elim[0]][elim[1] -1][2] != 1 and \
                self.element[elim[0]][elim[1] -1][1] == elim[2]:
            tuple = (elim[0], elim[1]-1, elim[2])
            list.append(tuple)
            #print('left OK', tuple)
            # mark 
            self.element[elim[0]][elim[1]][2] = 1
            self.element[elim[0]][elim[1]-1][2] = 1
            list.append(self.neighbor(tuple))
            
        #right
        if elim[1] + 1 <= 19 and \
                self.element[elim[0]][elim[1] +1][0] and \
                self.element[elim[0]][elim[1] +1][2] != 1 and \
                self.element[elim[0]][elim[1] +1][1] == elim[2]:
            tuple = (elim[0], elim[1]+1, elim[2])
            list.append(tuple)
            #print('right OK', tuple)
            # mark self
            self.element[elim[0]][elim[1]][2] = 1
            self.element[elim[0]][elim[1]+1][2] = 1
            list.append(self.neighbor(tuple))
        
        #up
        if elim[0] - 1 >= 0 and \
                self.element[elim[0] -1][elim[1]][0] and \
                self.element[elim[0] -1][elim[1]][2] != 1 and \
                self.element[elim[0] -1][elim[1]][1] == elim[2]:
            tuple = (elim[0] -1, elim[1], elim[2])
            list.append(tuple)
            #print('up OK', tuple)
            # mark self
            self.element[elim[0]][elim[1]][2] = 1
            self.element[elim[0]-1][elim[1]][2] = 1
            list.append(self.neighbor(tuple))
        
        #down
        if elim[0] + 1 <= 9 and \
                self.element[elim[0] +1][elim[1]][0] and \
                self.element[elim[0] +1][elim[1]][2] != 1 and \
                self.element[elim[0] +1][elim[1]][1] == elim[2]:
            tuple = (elim[0] +1, elim[1], elim[2])
            list.append(tuple)
            #print('down OK', tuple)
            # mark self
            self.element[elim[0]][elim[1]][2] = 1
            self.element[elim[0]+1][elim[1]][2] = 1
            list.append(self.neighbor(tuple))
            
        return list
    
    def clear_mark(self):
        for i in range(10):            
            for j in range(20):
                self.element[i][j][2] = 0            
    
    def remove_oneblock(self, row, col):
        for i in range(row, 0, -1):
            self.element[i][col][0] = self.element[i-1][col][0]
            self.element[i][col][1] = self.element[i-1][col][1]
            self.element[i][col][2] = self.element[i-1][col][2]
        self.element[0][col][0] = 0
        self.element[0][col][1] = 0
        self.element[0][col][2] = 0
        
    def remove_column(self, col):
        for j in range(col, 19):
            for i in range(10):
                self.element[i][j][0] = self.element[i][j+1][0]
                self.element[i][j][1] = self.element[i][j+1][1]
                self.element[i][j][2] = self.element[i][j+1][2]
            
            for i in range(10):
                self.element[i][19][0] = 0
                self.element[i][19][1] = 0
                self.element[i][19][2] = 0
        
    def remove_blocks(self):
        for i in range(10):
            for j in range(20):
                if( self.element[i][j][2] == 1):
                    #print('(',i, j,')')
                    self.remove_oneblock(i,j)
        
        # check null column and shift
        for j in range(19):
            sum = 0
            for i in range(10):
                sum += self.element[i][j][0]
                
            if sum == 0:
                self.remove_column(j)
                
    def handleMouseDown(self):
        mouseX, mouseY = pygame.mouse.get_pos()
        col = int((mouseX - Board.StartX) / 40)
        row = int((mouseY - Board.StartY) / 40)
        
        if row >= 0 and row <= 9 and col >=0 and col <= 19 and self.element[row][col][0] != 0:
            #print(row, col, self.element[row][col][1])
            mark = self.neighbor((row, col, self.element[row][col][1]))
            #print(mark)
            #self.clear_mark()
        
        self.remove_blocks()
        
    def handleMouseMove(self):
        mouseX, mouseY = pygame.mouse.get_pos()
        col = int((mouseX - Board.StartX) / 40)
        row = int((mouseY - Board.StartY) / 40)
        
        if row >= 0 and row <= 9 and col >=0 and col <= 19 and self.element[row][col][0] != 0:
            self.clear_mark()
            #print(row, col, self.element[row][col][1])
            mark = self.neighbor((row, col, self.element[row][col][1]))
            #print(mark)
            #self.clear_mark()
                       

def main():
    # initialise pygame modules
    pygame.init()
    pygame.display.set_caption("same same")
    
    screenSize = width, height = 1200, 800
    

    # set screen and clock
    screen = pygame.display.set_mode(screenSize)
    clock = pygame.time.Clock()
    
    board = Board()
    #print(board.element)
    #board.draw(screen)
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                board.handleMouseDown()
                
            if event.type == pygame.MOUSEMOTION:
                board.handleMouseMove()
        
        screen.fill(BLACK)
        board.draw(screen)
        pygame.display.flip()
        #pygame.display.update()
    
        clock.tick(30)
        
    
        
if __name__ == '__main__':
    main()