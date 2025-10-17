import heapq
from utils import *

def AStar(chessboard):
    init_state = chessboard.board
    pq = []
    counter = 0 
    heapq.heappush(pq, (heuristic(init_state) + g_func(init_state), counter, init_state))
    visited = set()
    path = []

    while pq:
        h, _, node = heapq.heappop(pq)
        node_key = tuple(map(tuple, node))  
        if node_key in visited:
            continue
        visited.add(node_key)
        path.append(node)

        if chessboard.is_goal_state(node):
            return path

        for state in chessboard.next_states(node):
            counter += 1
            heapq.heappush(pq, (heuristic(state) + g_func(state), counter, state))

    chessboard.running = False

    return path