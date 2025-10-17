from utils import *

def HillClimbing(chessboard):
    node = random_8x8_board()   # random initial board
    path = [node]
    
    while True:
        current_h = count_conflicts(node)
        next_node = None
        min_local = current_h

        # Duyệt tất cả neighbor
        for state in chessboard.next_states_2(node):
            h = count_conflicts(state)
            if h < min_local:
                next_node = state
                min_local = h

        # Nếu không có neighbor nào tốt hơn → local minimum
        if next_node is None or min_local >= current_h:
            path.append(node)
            chessboard.running = False
            return path
        
        # Cập nhật node hiện tại
        node = next_node
        path.append(node)