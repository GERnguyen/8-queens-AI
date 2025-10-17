import pygame
import sys
from button import Button
from Menu import Menu
from const import *
from ChessBoard import ChessBoard
from BFS import BFS
from DFS import DFS
from IDS import IDS
from Greedy import Greedy
from AStar import AStar
from UCS import UCS
from HillClimbing import HillClimbing
from SimulatedAnnealing import SimulatedAnnealing
from BeamSearch import BeamSearch

from utils import *



pygame.init()


def main():
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("8 Queens Visualizer")
    
    clock = pygame.time.Clock()
    
    board_size = 480  
    board_x = (WINDOW_WIDTH - board_size) // 2 
    board_y = 50 
    
    chess_board = ChessBoard(board_x, board_y, board_size, screen)
    menu = Menu(screen)
    running = True

    SKIP_BUTTON = Button(WINDOW_WIDTH - 180, chess_board.y + chess_board.size + 40, 100, 40, "SKIP")
    BFS_BUTTON = Button(100, chess_board.y + chess_board.size + 40, 100, 40, "BFS")
    DFS_BUTTON = Button(100, chess_board.y + chess_board.size + 100, 100, 40, "DFS")
    IDS_BUTTON = Button(100, chess_board.y + chess_board.size + 160, 100, 40, "IDS")
    GREEDY_BUTTON = Button(220, chess_board.y + chess_board.size + 40, 100, 40, "Greedy")
    AStar_BUTTON = Button(220, chess_board.y + chess_board.size + 100, 100, 40, "A*")
    UCS_BUTTON = Button(220, chess_board.y + chess_board.size + 160, 100, 40, "UCS")
    HILL_BUTTON = Button(340, chess_board.y + chess_board.size + 40, 100, 40, "Hill")
    SIMULATED_BUTTON = Button(340, chess_board.y + chess_board.size + 100, 100, 40, "Anneal")
    BEAM_BUTTON = Button(340, chess_board.y + chess_board.size + 160, 100, 40, "Beam")
    menu.buttons = [SKIP_BUTTON, BFS_BUTTON, DFS_BUTTON, IDS_BUTTON, GREEDY_BUTTON, AStar_BUTTON, UCS_BUTTON, HILL_BUTTON, SIMULATED_BUTTON, BEAM_BUTTON]
    queens = chess_board.board
    result = []

    wait = 0
    while running:
        menu.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False         
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1: 
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    square = chess_board.get_square_from_mouse(mouse_x, mouse_y)

        if SKIP_BUTTON.is_Selected():
            chess_board.skip = True

        if BFS_BUTTON.is_Selected():
            result = BFS(chess_board)
            wait = 0
        if DFS_BUTTON.is_Selected():
            result = DFS(chess_board)
            wait = 0
        if GREEDY_BUTTON.is_Selected():
            result = Greedy(chess_board)
            wait = 0
        if IDS_BUTTON.is_Selected():
            result = IDS(chess_board)
            wait = 0
        if AStar_BUTTON.is_Selected():
            result = AStar(chess_board)
            wait = 0
        if UCS_BUTTON.is_Selected():
            result = UCS(chess_board)
            wait = 0
        if HILL_BUTTON.is_Selected():
            result = HillClimbing(chess_board)
            wait = 500
        if SIMULATED_BUTTON.is_Selected():
            result = SimulatedAnnealing(chess_board)
            wait = 100
        if BEAM_BUTTON.is_Selected():
            result = BeamSearch(chess_board)
            wait = 100
        
        screen.fill(MEDIUM_BLUE)
        chess_board.draw(screen)
        menu.draw()        

        if result:
            if chess_board.skip == True:
                while result:
                    queens = result.pop(0)
                chess_board.skip = False
            else:
                pygame.time.wait(wait)
                queens = result.pop(0)
        chess_board.draw_queens(queens)

        pygame.display.flip()
        
        clock.tick(FPS)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()