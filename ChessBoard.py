import pygame
from const import *
import numpy as np

class ChessBoard:
    def __init__(self, x, y, size, screen):
        self.x = x
        self.y = y
        self.size = size
        self.square_size = size // 8 
 
        self.board = np.full((8,8), 0)  
        self.screen = screen
        self.skip = False
        self.speed = 0.05
        self.running = False
        self.pause = False
        
    def draw(self, screen):
        for row in range(8):
            for col in range(8):
                square_x = self.x + col * self.square_size
                square_y = self.y + row * self.square_size

                if (row + col) % 2 == 0:
                    color = LIGHTEST_BLUE
                else:
                    color = LIGHT_BLUE
                
                pygame.draw.rect(screen, color, 
                               (square_x, square_y, self.square_size, self.square_size))

                pygame.draw.rect(screen, MEDIUM_BLUE, 
                               (square_x, square_y, self.square_size, self.square_size), 2)
    
    def draw_queens(self, board):
        self.clear_board()
        for row in range(8):
            for col in range(8):
                if board[row][col] == 1:
                    center_x = self.x + col * self.square_size + self.square_size // 2
                    center_y = self.y + row * self.square_size + self.square_size // 2
                    
                    pygame.draw.circle(self.screen, DARK_BLUE, (center_x, center_y), self.square_size // 3)

                    pygame.draw.circle(self.screen, WHITE, (center_x, center_y), self.square_size // 4)
        
    def add_queen(self, row, col):
        if self.board[row][col] != 1:
            self.board[row][col] = 1
    
    def remove_queen(self, row, col):
        if self.board[row][col] == 1:
            self.board[row][col] = 0
    
    def clear_board(self):
        self.board[:] = 0
    
    def get_square_from_mouse(self, mouse_x, mouse_y):
        if (self.x <= mouse_x < self.x + self.size and 
            self.y <= mouse_y < self.y + self.size):
            
            col = (mouse_x - self.x) // self.square_size
            row = (mouse_y - self.y) // self.square_size
            return row, col
        return None
    
    def is_safe(self, board, row, col):
        for r in range(row):
            for c in range(8):
                if board[r][c] == 1:
                    if c == col:
                        return False
                    if abs(r - row) == abs(c - col):
                        return False
        return True
    
    def is_goal_state(self, curr_state):
        queens_count = np.sum(curr_state == 1)
        return queens_count == 8
    
    def next_states(self, curr_state):
        row = np.sum(curr_state == 1) 
        next_states = []
        for col in range(8):
            if self.is_safe(curr_state, row, col):
                possible = curr_state.copy()
                possible[row][col] = 1
                next_states.append(possible)
        return next_states

    def next_states_2(self, board):
        n = 8
        neighbors = []
        for r in range(n):
            board_r = board[r].tolist()
            c = board_r.index(1)

            if c - 1 >= 0 and board[r][c - 1] == 0:
                new_board = board.copy()
                new_board[r][c] = 0
                new_board[r][c - 1] = 1
                neighbors.append(new_board)
            if c + 1 < n and board[r][c + 1] == 0:
                new_board = board.copy()
                new_board[r][c] = 0
                new_board[r][c + 1] = 1
                neighbors.append(new_board)

        return neighbors

    def reset_board(self):
        self.clear_board()
        self.skip = False
        self.running = True
        self.pause = False



