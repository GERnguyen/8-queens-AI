import numpy as np

def get_neighbors(board):
    neighbors = []
    for row in range(8):
        # Find the column where the queen currently is
        current_col = np.argmax(board[row])
        for col in range(8):
            if col != current_col:
                # Copy board and move the queen in this row
                new_board = board.copy()
                new_board[row][current_col] = 0
                new_board[row][col] = 1
                neighbors.append(new_board)
    return neighbors

# Example
board = np.zeros((8, 8), dtype=int)
for i in range(8):
    board[i][i] = 1  # Queens on the diagonal

neighbors = get_neighbors(board)
print(f"Total neighbors: {len(neighbors)}")
print(neighbors[0])
