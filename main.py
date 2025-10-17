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
from CSP import run_algorithm

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
    
    # CSP Buttons
    BT_BUTTON = Button(460, chess_board.y + chess_board.size + 40, 100, 40, "BT")
    FC_BUTTON = Button(460, chess_board.y + chess_board.size + 100, 100, 40, "FC")
    AC3_BUTTON = Button(460, chess_board.y + chess_board.size + 160, 100, 40, "AC-3")
    
    menu.buttons = [SKIP_BUTTON, BFS_BUTTON, DFS_BUTTON, IDS_BUTTON, GREEDY_BUTTON, 
                    AStar_BUTTON, UCS_BUTTON, HILL_BUTTON, SIMULATED_BUTTON, BEAM_BUTTON,
                    BT_BUTTON, FC_BUTTON, AC3_BUTTON]
    
    queens = chess_board.board
    result = []
    csp_generator = None

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

        # Reset done khi bắt đầu thuật toán mới
        if BFS_BUTTON.is_Selected():
            chess_board.done = False
            result = BFS(chess_board)
            csp_generator = None
            wait = 0
        if DFS_BUTTON.is_Selected():
            chess_board.done = False
            result = DFS(chess_board)
            csp_generator = None
            wait = 0
        if GREEDY_BUTTON.is_Selected():
            chess_board.done = False
            result = Greedy(chess_board)
            csp_generator = None
            wait = 0
        if IDS_BUTTON.is_Selected():
            chess_board.done = False
            result = IDS(chess_board)
            csp_generator = None
            wait = 0
        if AStar_BUTTON.is_Selected():
            chess_board.done = False
            result = AStar(chess_board)
            csp_generator = None
            wait = 0
        if UCS_BUTTON.is_Selected():
            chess_board.done = False
            result = UCS(chess_board)
            csp_generator = None
            wait = 0
        if HILL_BUTTON.is_Selected():
            chess_board.done = False
            result = HillClimbing(chess_board)
            csp_generator = None
            wait = 500
        if SIMULATED_BUTTON.is_Selected():
            chess_board.done = False
            result = SimulatedAnnealing(chess_board)
            csp_generator = None
            wait = 100
        if BEAM_BUTTON.is_Selected():
            chess_board.done = False
            result = BeamSearch(chess_board)
            csp_generator = None
            wait = 100
            
        # CSP Algorithms
        if BT_BUTTON.is_Selected():
            chess_board.done = False
            result = []
            csp_generator = run_algorithm("bt", visualize=True)
            wait = 50
        if FC_BUTTON.is_Selected():
            chess_board.done = False
            result = []
            csp_generator = run_algorithm("fc", visualize=True)
            wait = 50
        if AC3_BUTTON.is_Selected():
            chess_board.done = False
            result = []
            csp_generator = run_algorithm("ac3", visualize=True)
            wait = 100
        
        screen.fill(MEDIUM_BLUE)
        chess_board.draw(screen)
        menu.draw()        

        # Handle CSP visualization
        if csp_generator is not None:
            try:
                if chess_board.skip:
                    # Skip to end
                    last_state = None
                    last_path = None
                    for state, path in csp_generator:
                        last_state = state
                        last_path = path
                        if len(path) == 8:
                            break
                    
                    if last_state is not None:
                        queens = last_state
                        # Kiểm tra xem có phải nghiệm đầy đủ không
                        if last_path and len(last_path) == 8:
                            chess_board.done = True
                    
                    csp_generator = None
                    chess_board.skip = False
                else:
                    # Step by step
                    pygame.time.wait(wait)
                    state, path = next(csp_generator)
                    queens = state
                    
                    # Kiểm tra xem đã hoàn thành chưa
                    if len(path) == 8:
                        chess_board.done = True
                        csp_generator = None
                        
            except StopIteration:
                csp_generator = None

        # Handle normal search results
        if result:
            if chess_board.skip:
                while result:
                    queens = result.pop(0)
                    if not result and chess_board.is_goal_state(queens):
                        chess_board.done = True
                chess_board.skip = False
            else:
                pygame.time.wait(wait)
                queens = result.pop(0)
                
                if not result and chess_board.is_goal_state(queens):
                    chess_board.done = True
                
        chess_board.draw_queens(queens)

        pygame.display.flip()
        
        clock.tick(FPS)
    
    pygame.quit()
    sys.exit()

main()