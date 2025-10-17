from queue import deque

def DFS(chessboard):
    init_state = chessboard.board
    queue = deque()
    queue.append(init_state)
    visited = set()
    result = [init_state]

    while queue:
        node = queue.pop()
        node_key = tuple(map(tuple, node))
        if node_key in visited:
            continue
        visited.add(node_key)
        if not chessboard.skip:
            result.append(node)

        for state in chessboard.next_states(node):
            if chessboard.is_goal_state(state):
                node = state
                if not chessboard.skip:
                    result.append(node)
                return result
            queue.append(state)
    
    chessboard.running = False
    return result