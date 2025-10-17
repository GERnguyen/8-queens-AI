
import numpy as np
import random


def heuristic(board):
    n = len(board)
    queens = [(r, c) for r in range(n) for c in range(n) if board[r][c] == 1]
    damage = [[0 for _ in range(n)] for _ in range(n)]

    for r, c in queens:
        for i in range(n):
            damage[r][i] = 1
            damage[i][c] = 1
        for i in range(n):
            if 0 <= r+i < n and 0 <= c+i < n:
                damage[r+i][c+i] = 1
            if 0 <= r-i < n and 0 <= c+i < n:
                damage[r-i][c+i] = 1
            if 0 <= r+i < n and 0 <= c-i < n:
                damage[r+i][c-i] = 1
            if 0 <= r-i < n and 0 <= c-i < n:
                damage[r-i][c-i] = 1

    placed_cols = [c for _, c in queens]
    remaining_cols = [c for c in range(n) if c not in placed_cols]

    damaged_remaining = 0
    for r in range(n):
        for c in remaining_cols:
            if damage[r][c]:
                damaged_remaining += 1

    return damaged_remaining


def g_func(board):
    n = len(board)
    queens = [(r, c) for r in range(n) for c in range(n) if board[r][c] == 1]
    damage = [[0 for _ in range(n)] for _ in range(n)]

    for r, c in queens:
        for i in range(n):
            damage[r][i] = 1
            damage[i][c] = 1
        for i in range(n):
            if 0 <= r+i < n and 0 <= c+i < n:
                damage[r+i][c+i] = 1
            if 0 <= r-i < n and 0 <= c+i < n:
                damage[r-i][c+i] = 1
            if 0 <= r+i < n and 0 <= c-i < n:
                damage[r+i][c-i] = 1
            if 0 <= r-i < n and 0 <= c-i < n:
                damage[r-i][c-i] = 1

    placed_cols = [c for _, c in queens]
    damaged_current = 0
    for r in range(n):
        for c in placed_cols:
            if damage[r][c]:
                damaged_current += 1

    return damaged_current



def random_8x8_board():
    board = np.zeros((8, 8), dtype=int)
    for row in range(8):
        col = random.randint(0, 7)
        board[row][col] = 1
    return board


def count_conflicts(board):
    n = 8
    queens = [(r, c) for r in range(n) for c in range(n) if board[r][c] == 1]
    conflicts = 0

    for i in range(len(queens)):
        for j in range(i + 1, len(queens)):
            r1, c1 = queens[i]
            r2, c2 = queens[j]
            if r1 == r2 or c1 == c2:
                conflicts += 1
            elif abs(r1 - r2) == abs(c1 - c2):
                conflicts += 1

    return conflicts
