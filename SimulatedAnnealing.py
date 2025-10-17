import math
import random
import pygame
from utils import *

def SimulatedAnnealing(chessboard, T_start=100, T_end=1e-3, cooling_rate=0.95):
    node = random_8x8_board()  # random initial state
    path = [node]
    T = T_start  # starting temperature

    while T > T_end:
        current_h = count_conflicts(node)
        neighbors = chessboard.next_states_2(node)
        if not neighbors:
            break

        # Chọn ngẫu nhiên 1 neighbor
        next_node = random.choice(neighbors)
        next_h = count_conflicts(next_node)

        if next_h < current_h:
            node = next_node
        else:
            delta = next_h - current_h
            probability = math.exp(-delta / T)
            if random.random() < probability:
                node = next_node

        path.append(node)

        T *= cooling_rate

        if count_conflicts(node) == 0:
            chessboard.running = False
            return path

    chessboard.running = False
    return path
